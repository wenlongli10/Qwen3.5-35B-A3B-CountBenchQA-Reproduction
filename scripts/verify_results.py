#!/usr/bin/env python3
import json, math, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUFFIX = " Note that: answer with a number directly e.g. 3. Do not include any additional text."
RUNS = [
    ("AWQ think", "single", "awq_think.jsonl", None, 472, 463651, 341, 30627),
    ("AWQ nothink", "original", "awq_nothink.jsonl", None, 438, 1018, 2, 3),
    ("AWQ nothink", "seed_1", "awq_nothink_seed1.jsonl", 1, 438, 1023, 2, 3),
    ("AWQ nothink", "seed_2", "awq_nothink_seed2.jsonl", 2, 443, 1022, 2, 3),
    ("BF16 think", "single", "bf16_think.jsonl", 0, 468, 449513, 313, 39865),
    ("BF16 nothink", "seed_0", "bf16_nothink.jsonl", 0, 449, 1037, 2, 3),
    ("BF16 nothink", "seed_1", "bf16_nothink_seed1.jsonl", 1, 435, 1034, 2, 3),
    ("BF16 nothink", "seed_2", "bf16_nothink_seed2.jsonl", 2, 450, 1024, 2, 3),
]
EXPECTED_FINAL = {"AWQ think": 472/487, "AWQ nothink": 1319/1461,
                  "BF16 think": 468/487, "BF16 nothink": 1334/1461}

def load(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def main():
    common_ids = None; grouped = {}
    for configuration, run, filename, seed, correct, total_tokens, median, maximum in RUNS:
        rows = load(ROOT / "results" / "final" / filename)
        assert len(rows) == 487
        ids = {r["index"] for r in rows}; assert len(ids) == 487
        common_ids = ids if common_ids is None else common_ids
        assert ids == common_ids
        for r in rows:
            assert isinstance(r.get("prediction_raw"), str) and r["prediction_raw"]
            assert isinstance(r.get("prediction_text"), str) and r["prediction_text"]
            assert isinstance(r.get("answer_text"), str) and r["answer_text"]
            assert r["finish_reason"] == "stop"
            assert isinstance(r["generated_tokens"], int) and r["generated_tokens"] > 0
            assert r["prompt"] == r["question"] + SUFFIX
            assert r["seed"] == seed
            is_correct = str(r["answer"]) in r["answer_text"]
            assert r["correct_vlmevalkit_substring"] is is_correct
            if configuration.startswith("AWQ"):
                assert r["presence_penalty"] == 1.5
                response = r["raw_response"]
                assert response["usage"]["completion_tokens"] == r["generated_tokens"]
                assert response["choices"][0]["message"]["content"] == r["prediction_raw"]
            else:
                assert r["presence_penalty"] == 0.0
        tokens = [r["generated_tokens"] for r in rows]
        actual_correct = sum(str(r["answer"]) in r["answer_text"] for r in rows)
        assert (actual_correct, sum(tokens), statistics.median(tokens), max(tokens)) == (correct, total_tokens, median, maximum)
        grouped.setdefault(configuration, []).append(rows)
        print(f"OK {configuration} {run}: 487 complete raw outputs; {correct}/487 = {correct/487:.2%}; tokens={total_tokens}")
    for configuration, runs in grouped.items():
        accuracy = statistics.mean(sum(str(r["answer"]) in r["answer_text"] for r in rows) / 487 for rows in runs)
        assert math.isclose(accuracy, EXPECTED_FINAL[configuration], rel_tol=0, abs_tol=1e-12)
        print(f"FINAL {configuration}: runs={len(runs)}; accuracy={accuracy:.2%}")
    print("ALL EIGHT RUNS AND FOUR FINAL CONFIGURATIONS VERIFIED")

if __name__ == "__main__":
    main()
