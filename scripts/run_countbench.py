#!/usr/bin/env python3
"""Basic CountBenchQA inference for Qwen3.5 AWQ (vLLM) or BF16 (Transformers)."""
import argparse, base64, csv, json, re, sys, time, urllib.request
from pathlib import Path

csv.field_size_limit(sys.maxsize)
SUFFIX = " Note that: answer with a number directly e.g. 3. Do not include any additional text."


def split_think(text):
    if "</think>" in text:
        think, answer = text.rsplit("</think>", 1)
        return think.replace("<think>", "", 1).strip(), answer.strip(), True
    return text.replace("<think>", "", 1).strip(), "", bool(text.strip())


def extract_count(text):
    text = text.strip()
    if re.fullmatch(r"[+]?\d+", text):
        return int(text)
    numbers = re.findall(r"(?<![\d.])\d+(?![\d.])", text)
    return int(numbers[-1]) if numbers else None


def mime_of(raw):
    if raw.startswith(b"\xff\xd8"): return "image/jpeg"
    if raw.startswith(b"\x89PNG"): return "image/png"
    if raw.startswith((b"GIF87a", b"GIF89a")): return "image/gif"
    if raw.startswith(b"RIFF") and raw[8:12] == b"WEBP": return "image/webp"
    raise ValueError("Unsupported image format")


def make_record(row, raw, clean, finish_reason, tokens, seconds, args, raw_response=None):
    if args.mode == "think":
        think_text, answer_text, has_think = split_think(clean)
    else:
        think_text, answer_text, has_think = "", clean.strip(), False
    answer = str(row["answer"])
    record = {
        "index": row["index"], "question": row["question"],
        "prompt": row["question"] + SUFFIX, "answer": answer,
        "model": args.model_path or args.served_model_name, "mode": args.mode,
        "seed": args.seed, "presence_penalty": 1.5 if args.backend == "awq" else 0.0,
        "max_new_tokens": args.max_new_tokens,
        "prediction_raw": raw, "prediction_text": clean,
        "think_text": think_text, "has_think": has_think, "answer_text": answer_text,
        "prediction_count": extract_count(answer_text),
        "correct_vlmevalkit_substring": answer in answer_text,
        "finish_reason": finish_reason, "generated_tokens": int(tokens),
        "seconds": round(seconds, 3),
    }
    if raw_response is not None:
        record["raw_response"] = raw_response
    return record


def run_awq(rows, args, sink):
    for number, row in enumerate(rows, 1):
        raw_image = base64.b64decode(row["image"])
        payload = {
            "model": args.served_model_name,
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime_of(raw_image)};base64,{row['image']}"}},
                {"type": "text", "text": row["question"] + SUFFIX},
            ]}],
            "temperature": 1.0, "top_p": 0.95, "top_k": 20, "min_p": 0.0,
            "presence_penalty": 1.5, "repetition_penalty": 1.0,
            "max_tokens": args.max_new_tokens,
            "chat_template_kwargs": {"enable_thinking": args.mode == "think"},
        }
        if args.seed is not None:
            payload["seed"] = args.seed
        start = time.time()
        request = urllib.request.Request(args.vllm_url, data=json.dumps(payload).encode(),
                                         headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=7200) as response:
            raw_response = json.load(response)
        choice = raw_response["choices"][0]
        content = choice["message"].get("content") or ""
        tokens = raw_response["usage"]["completion_tokens"]
        record = make_record(row, content, content, choice["finish_reason"], tokens,
                             time.time() - start, args, raw_response)
        sink.write(json.dumps(record, ensure_ascii=False) + "\n"); sink.flush()
        print(f"{number}/{len(rows)} seed={args.seed} answer={record['answer_text']!r} tokens={tokens}", flush=True)


def run_bf16(rows, args, sink):
    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText
    from qwen_vl_utils import process_vision_info

    processor = AutoProcessor.from_pretrained(args.model_path, local_files_only=True)
    model = AutoModelForImageTextToText.from_pretrained(
        args.model_path, dtype=torch.bfloat16, device_map="auto", max_memory={0: "82GiB"},
        attn_implementation="sdpa", local_files_only=True, low_cpu_mem_usage=True)
    model.eval(); model.generation_config.presence_penalty = 0.0
    image_dir = Path(args.output) / "images"; image_dir.mkdir(exist_ok=True)

    for number, row in enumerate(rows, 1):
        image_path = image_dir / f"{row['index']}.jpg"
        if not image_path.exists():
            image_path.write_bytes(base64.b64decode(row["image"]))
        messages = [{"role": "user", "content": [
            {"type": "image", "image": image_path.as_uri()},
            {"type": "text", "text": row["question"] + SUFFIX},
        ]}]
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                             enable_thinking=args.mode == "think")
        images, videos, _ = process_vision_info(messages, image_patch_size=16,
                                                return_video_kwargs=True, return_video_metadata=True)
        inputs = processor(text=[text], images=images, videos=videos,
                           return_tensors="pt", do_resize=False).to("cuda:0")
        if args.seed is not None:
            torch.manual_seed(args.seed)
        start = time.time()
        with torch.inference_mode():
            generated = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                do_sample=True, temperature=1.0, top_p=0.95, top_k=20, repetition_penalty=1.0)
        torch.cuda.synchronize()
        new_ids = generated[0, inputs["input_ids"].shape[1]:]
        raw = processor.decode(new_ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
        clean = processor.decode(new_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        finish = "length" if len(new_ids) >= args.max_new_tokens else "stop"
        record = make_record(row, raw, clean, finish, len(new_ids), time.time() - start, args)
        sink.write(json.dumps(record, ensure_ascii=False) + "\n"); sink.flush()
        print(f"{number}/{len(rows)} seed={args.seed} answer={record['answer_text']!r} tokens={len(new_ids)}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["awq", "bf16"], required=True)
    parser.add_argument("--mode", choices=["think", "nothink"], required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model-path", help="Local BF16 model directory")
    parser.add_argument("--tsv", default="data/CountBenchQA.tsv")
    parser.add_argument("--seed", type=int, default=None, help="Omit for an unseeded run")
    parser.add_argument("--max-new-tokens", type=int, default=32768)
    parser.add_argument("--limit", type=int, default=487)
    parser.add_argument("--vllm-url", default="http://127.0.0.1:8000/v1/chat/completions")
    parser.add_argument("--served-model-name", default="qwen3.5-35b-a3b-awq")
    args = parser.parse_args()
    if args.backend == "bf16" and not args.model_path:
        parser.error("--model-path is required for BF16")

    with open(args.tsv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))[:args.limit]
    output = Path(args.output); output.mkdir(parents=True, exist_ok=True)
    (output / "run_config.json").write_text(json.dumps(vars(args), ensure_ascii=False, indent=2) + "\n")
    with (output / "predictions.jsonl").open("w", encoding="utf-8") as sink:
        if args.backend == "awq": run_awq(rows, args, sink)
        else: run_bf16(rows, args, sink)
    records = [json.loads(line) for line in (output / "predictions.jsonl").read_text().splitlines() if line]
    valid = [r for r in records if not r.get("error")]
    summary = {"total": len(records), "correct": sum(r["correct_vlmevalkit_substring"] for r in valid),
               "accuracy": sum(r["correct_vlmevalkit_substring"] for r in valid) / len(valid),
               "total_tokens": sum(r["generated_tokens"] for r in valid),
               "length": sum(r["finish_reason"] == "length" for r in valid)}
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
