# Contributing

This repository is primarily an archived reproduction bundle rather than a general-purpose evaluation framework.

Appropriate contributions include:

- documentation corrections;
- portable reproduction improvements;
- result-schema clarifications;
- verification checks that do not alter archived evidence.

Do not overwrite final predictions or headline metrics to make results appear better. Any new experiment should use a new output directory and document its model revision, dataset MD5, hardware, serving stack, sampling parameters, seed policy,.

Before submitting a change, run:

```bash
python3 scripts/verify_results.py
```

Changes to third-party data, model weights, credentials, or large generated caches are not accepted in Git.
