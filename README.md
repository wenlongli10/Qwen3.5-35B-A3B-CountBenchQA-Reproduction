# Qwen3.5-35B-A3B CountBenchQA Reproduction

[中文](README.zh-CN.md) · [Protocol](docs/EXPERIMENT_PROTOCOL.md) · [Evaluation](docs/EVALUATION.md) · [Detailed results](docs/RESULTS.md) · [Reproduce](docs/REPRODUCE.md)

Final **Qwen3.5-35B-A3B** experiments on revised **CountBenchQA**: **AWQ 4-bit / unquantized 16-bit (BF16)** × **think / nothink**. Each model has one complete think run and three independent nothink runs; the headline nothink results are three-run averages. All eight runs provide complete raw outputs, separate final answers, token statistics, and unified scores for 487 samples.

## Final results

VLMEvalKit CountBenchQA final-answer substring scoring: `ans in pred`, where `pred` is final answer text only and excludes reasoning.

| Model | Mode | Runs | Correct / 487 | Accuracy | Mean output tokens | Median | Max |
|---|---|---:|---:|---:|---:|---:|---:|
| AWQ 4-bit | think | 1 | 472/487 | **96.92%** | 952.06 | 341 | 30,627 |
| AWQ 4-bit | nothink | 3 | 439.67/487 (three-run mean) | **90.28%** | 2.10 | 2 | 3 |
| Unquantized 16-bit (BF16) | think | 1 | 468/487 | **96.10%** | 923.02 | 313 | 39,865 |
| Unquantized 16-bit (BF16) | nothink | 3 | 444.67/487 (three-run mean) | **91.31%** | 2.12 | 2 | 3 |

Each nothink run is scored independently before taking the arithmetic mean. Because every run contains 487 samples, this equals the pooled accuracy over 1,461 predictions: AWQ 1,319/1,461 and BF16 1,334/1,461. **No majority voting, per-sample best selection, or best-of-N is used.** See [`results/summary/run_level_summary.csv`](results/summary/run_level_summary.csv) for individual runs.

Output tokens include reasoning and final answers. They measure generated work, not cross-hardware speed. Final nothink medians, percentiles, and maxima are computed over the three runs' pooled outputs.

## Dataset download and source

- **Exact revised TSV used in these experiments:** [Download CountBenchQA.tsv](https://opencompass.openxlab.space/utils/VLMEval/CountBenchQA.tsv) — 487 samples, MD5 `fc73c8d4ffa665431448753f094d56ff`.
- **Evaluation source:** [OpenCompass VLMEvalKit](https://github.com/open-compass/VLMEvalKit).
- **Upstream dataset page:** [CountBenchQA on Hugging Face](https://huggingface.co/datasets/vikhyatk/CountBenchQA).
- Local instructions and checksum verification: [`data/README.md`](data/README.md).

## Shared protocol

- Revised CountBenchQA, 487 samples, MD5 `fc73c8d4ffa665431448753f094d56ff`; original TSV base64 image bytes without manual resize, compression, or crop.
- Original `question` plus this exact suffix, with no system message, few-shot examples, or answer information:

```text
 Note that: answer with a number directly e.g. 3. Do not include any additional text.
```

- Shared sampling: `temperature=1.0`, `top_p=0.95`, `top_k=20`, `repetition_penalty=1.0`.
- Randomness: BF16 think uses seed 0; BF16 nothink uses seeds 0, 1, and 2, set before each sample. AWQ think and the first AWQ nothink run omit `seed`; the two additional AWQ nothink runs use seeds 1 and 2.
- AWQ uses vLLM 0.32.0 and `presence_penalty=1.5`; BF16 uses Transformers 5.22.1, SDPA, and `presence_penalty=0.0`.
- Every run has 487 unique samples with IDs aligned across runs, complete raw output for every sample, and natural-stop final records.

See [`configs/`](configs/) and [`docs/EXPERIMENT_PROTOCOL.md`](docs/EXPERIMENT_PROTOCOL.md) for details.

## Verify and reproduce

```bash
python3 scripts/verify_results.py
bash data/download.sh
```

The verifier needs no GPU. It recomputes every run, checks raw-output completeness, and derives the nothink three-run averages. See [`docs/REPRODUCE.md`](docs/REPRODUCE.md) to regenerate. Model weights, the data TSV, and image caches are not bundled.

## Layout

```text
configs/                 Four final protocols with run-specific seed policies
data/                    Dataset download and checksum
docs/                    Protocol, evaluation, results, schema, reproduction
environment/             Software and dependency snapshots
results/final/           Complete raw outputs and final answers for eight runs
results/summary/         Final, run-level, and per-sample metrics
scripts/                 Inference, scoring, and integrity checks
```

Models: [Qwen/Qwen3.5-35B-A3B](https://huggingface.co/Qwen/Qwen3.5-35B-A3B) and `QuantTrio/Qwen3.5-35B-A3B-AWQ`. Evaluation reference: [VLMEvalKit](https://github.com/open-compass/VLMEvalKit). Original code and documentation use the [MIT License](LICENSE); third-party assets retain their licenses.
