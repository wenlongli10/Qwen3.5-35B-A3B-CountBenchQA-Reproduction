# Contributing

This repository archives a CountBenchQA reproduction with complete outputs and a small inference script.

Contributions can focus on:

- documentation corrections;
- portable reproduction improvements;
- result-schema clarifications;
- additional verification checks.

For a new experiment, use a new output directory and record the model revision, dataset MD5, hardware, serving stack, sampling parameters, and seed policy.

Before submitting a change, run:

```bash
python3 scripts/verify_results.py
```
