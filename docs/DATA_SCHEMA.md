# Result data schema

Each `results/final/*.jsonl` file has 487 UTF-8 JSON records with unique IDs aligned across all eight runs.

| Field | Meaning |
|---|---|
| `index`, `question`, `answer` | Sample ID, original question, and ground truth. |
| `prompt` | Question plus the exact fixed suffix. |
| `model`, `mode` | Model identifier and `think`/`nothink`. |
| `prediction_raw` | Complete original output: special-token-preserving BF16 decode or untouched AWQ assistant content. |
| `prediction_text` | Complete clean generated text, including reasoning when present. |
| `think_text`, `has_think` | Separated reasoning and its presence flag. |
| `answer_text` | Final answer only; the sole scoring input. |
| `prediction_count` | Optional parsed integer for inspection, not used in scoring. |
| `correct_vlmevalkit_substring` | `str(answer) in answer_text`. |
| `finish_reason` | `stop` for every archived final record. |
| `generated_tokens` | Completion tokens, including reasoning and final answer. |
| `seconds` | Recorded generation time where available. |
| `max_new_tokens` | Per-sample output budget. |
| `seed`, `presence_penalty` | Run-specific seed and penalty. BF16 uses 0/1/2 and 0.0; AWQ uses null/1/2 and 1.5 as documented. |
| `raw_response` | Complete captured AWQ completion JSON; absent for local BF16 generation. |

Summary files under `results/summary/` are derived from the final JSONL files, which are authoritative. `run_level_summary.csv` contains eight runs; `final_summary.csv` contains the four displayed configurations and nothink three-run aggregation.
