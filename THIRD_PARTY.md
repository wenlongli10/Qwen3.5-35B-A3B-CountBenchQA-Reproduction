# Third-party notices

This repository is an evaluation record. It does not grant rights to third-party models, datasets, or frameworks.

## Qwen3.5-35B-A3B

- Project: Qwen
- Model: https://huggingface.co/Qwen/Qwen3.5-35B-A3B
- Archived revision: `59d61f3ce65a6d9863b86d2e96597125219dc754`
- License: Apache-2.0 according to the model distribution; consult the model card and license at the exact revision.
- Model weights are not included.

## Qwen3.5-35B-A3B-AWQ

- Archived configuration names `QuantTrio/Qwen3.5-35B-A3B-AWQ`.
- The quantized checkpoint is a third-party derivative; its model card, base-model license, and redistribution terms apply.
- Model weights are not included.
- Selected model and preprocessor configuration snapshots are included for reproducibility and retain their upstream terms.

## CountBench / CountBenchQA

- Revised TSV download: https://opencompass.openxlab.space/utils/VLMEval/CountBenchQA.tsv
- CountBench upstream: https://github.com/google-research/google-research/tree/master/countbench
- CountBench upstream is listed as CC-BY-4.0. Users must also review the provenance and terms of the revised CountBenchQA artifact and any upstream image sources.
- The revised TSV is not redistributed by this repository; `data/download.sh` retrieves it from the upstream URL and verifies the expected MD5.

## VLMEvalKit

- Repository: https://github.com/open-compass/VLMEvalKit
- CountBenchQA reference implementation: `vlmeval/dataset/image_vqa.py`.
- The upstream framework and its license apply to upstream code. This repository implements and documents the equivalent short substring scoring rule for its own archived records.

## PyTorch, Transformers, vLLM, and other dependencies

All dependencies remain subject to their respective licenses. Exact archived versions are listed in `environment/`.
