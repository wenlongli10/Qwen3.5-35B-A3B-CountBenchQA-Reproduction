# Experiment protocol

## Final design

The repository reports four final configurations from eight complete runs. AWQ 4-bit and unquantized 16-bit (BF16) each have one think run and three independent nothink runs. Each run contains the same 487 CountBenchQA samples, complete raw outputs, and final records with `finish_reason="stop"`.

Think results are single-run results. Nothink results are arithmetic means of three independently scored runs. No majority voting, per-sample best selection, or best-of-N is used.

## Input and exact prompt

The revised CountBenchQA TSV has MD5 `fc73c8d4ffa665431448753f094d56ff`. Images use the original TSV base64 bytes without manual resizing, compression, or cropping. There is no system message, few-shot prompting, or answer metadata.

The user text for every sample is exactly:

```text
{question} Note that: answer with a number directly e.g. 3. Do not include any additional text.
```

`{question}` is the unedited TSV question. The leading space before `Note` belongs to the suffix. The full prompt is stored in every JSONL record. The official chat template controls thinking with `enable_thinking=true` or `false`.

## Generation and randomness

Shared sampling settings are `temperature=1.0`, `top_p=0.95`, `top_k=20`, and `repetition_penalty=1.0`.

| Model and mode | Run | Seed policy | Output budget |
|---|---|---|---:|
| AWQ think | single | Seed omitted; not fixed | 32,768 |
| AWQ nothink | original | Seed omitted; not fixed | 2,048 |
| AWQ nothink | seed 1 | Request `seed=1` | 32,768 |
| AWQ nothink | seed 2 | Request `seed=2` | 32,768 |
| BF16 think | single | `torch.manual_seed(0)` per sample | 32,768 or 65,536 as recorded |
| BF16 nothink | seed 0 | `torch.manual_seed(0)` per sample | 32,768 |
| BF16 nothink | seed 1 | `torch.manual_seed(1)` per sample | 32,768 |
| BF16 nothink | seed 2 | `torch.manual_seed(2)` per sample | 32,768 |

AWQ uses vLLM 0.32.0 and `presence_penalty=1.5`. BF16 uses Transformers 5.22.1, SDPA, and `presence_penalty=0.0`. The portable BF16 script accepts output budgets up to 65,536 through `--max-new-tokens`.

## Complete outputs

BF16 stores a special-token-preserving decode in `prediction_raw`, a clean decode in `prediction_text`, and separate reasoning/final-answer fields. AWQ stores untouched assistant content in `prediction_raw` and `prediction_text`, plus the complete captured server response in `raw_response`. All runs use the same final-answer scoring rule. Generated tokens include reasoning and final-answer tokens.
