# Reproduction guide

## Verify archived results

```bash
python3 scripts/verify_results.py
```

The verifier uses the Python standard library and checks all eight archived runs.

## Dataset

```bash
bash data/download.sh
```

The script creates `data/CountBenchQA.tsv` and verifies MD5 `fc73c8d4ffa665431448753f094d56ff`.

## One basic inference script

`scripts/run_countbench.py` handles either backend and either thinking mode. Set `--seed` explicitly for a seeded run, or omit it for an unseeded run. To perform another independent experiment, change `--seed` and use a new `--output` directory.

### BF16 / Transformers

Install `environment/requirements-bf16.txt` with a CUDA-compatible PyTorch build, then run:

```bash
python3 scripts/run_countbench.py   --backend bf16   --model-path /path/to/Qwen3.5-35B-A3B   --mode nothink   --seed 0   --output outputs/bf16_nothink_seed0
```

For think, change `--mode` to `think`; `--max-new-tokens 65536` selects the larger output budget. Model revision: `59d61f3ce65a6d9863b86d2e96597125219dc754`. The script uses BF16, SDPA, and complete raw decoding.

### AWQ / vLLM

Install `environment/requirements-awq.txt` and start the server without a reasoning parser:

```bash
export VLLM_USE_FLASHINFER_SAMPLER=0
vllm serve /path/to/Qwen3.5-35B-A3B-AWQ   --served-model-name qwen3.5-35b-a3b-awq   --host 127.0.0.1 --port 8000   --tensor-parallel-size 1 --max-num-seqs 4   --max-model-len 65536 --gpu-memory-utilization 0.92
```

In another terminal:

```bash
python3 scripts/run_countbench.py   --backend awq   --mode nothink   --seed 1   --output outputs/awq_nothink_seed1
```

Change `--mode` to `think` for a think run. Omit `--seed` for an unseeded request. Use `--max-new-tokens 2048` to match the original AWQ nothink output budget; the default is 32,768. Score only `answer_text` with `str(answer) in answer_text`.
