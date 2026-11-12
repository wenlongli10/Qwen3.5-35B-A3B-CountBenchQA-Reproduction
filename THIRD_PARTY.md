# Third-party notices

## Qwen3.5-35B-A3B

- Project: Qwen
- Model: https://huggingface.co/Qwen/Qwen3.5-35B-A3B
- Archived revision: `59d61f3ce65a6d9863b86d2e96597125219dc754`
- License: Apache-2.0, as listed by the model distribution

## Qwen3.5-35B-A3B-AWQ

- Model: https://huggingface.co/QuantTrio/Qwen3.5-35B-A3B-AWQ
- Base model: Qwen3.5-35B-A3B
- Selected model and preprocessor configuration snapshots are included for reproducibility.

## CountBench / CountBenchQA

- Revised TSV: https://opencompass.openxlab.space/utils/VLMEval/CountBenchQA.tsv
- CountBenchQA: https://huggingface.co/datasets/vikhyatk/CountBenchQA
- CountBench: https://github.com/google-research/google-research/tree/master/countbench
- CountBench license: CC-BY-4.0
- `data/download.sh` retrieves the revised TSV and verifies its MD5.

## VLMEvalKit

- Repository: https://github.com/open-compass/VLMEvalKit
- CountBenchQA reference implementation: `vlmeval/dataset/image_vqa.py`
- The archived results use the same final-answer substring scoring rule.

## Dependencies

PyTorch, Transformers, vLLM, and other dependencies retain their respective licenses. Versions are listed in `environment/`.
