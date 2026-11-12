# Environment

## BF16

Transformers 5.22.1; PyTorch 2.10.0+cu128; torchvision 0.25.0+cu128; bfloat16; SDPA. Model revision `59d61f3ce65a6d9863b86d2e96597125219dc754`.

## AWQ

vLLM 0.32.0; PyTorch 2.13.0+cu130; Transformers 5.19.0; AWQ 4-bit, group size 128, GEMM, zero point. Served name `qwen3.5-35b-a3b-awq`; `VLLM_USE_FLASHINFER_SAMPLER=0`; no reasoning parser.

Requirements files are version snapshots. Use CUDA-compatible builds for the target GPU.
