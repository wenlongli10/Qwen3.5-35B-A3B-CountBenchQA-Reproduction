# Publishing checklist

Before pushing, update `CITATION.cff` with the maintainer name and add the repository URL if desired.

Create an empty GitHub repository without a README, license, or `.gitignore`, then run from this directory:

```bash
git init
git add .
git commit -m "Initial CountBenchQA reproduction bundle"
git branch -M main
git remote add origin https://github.com/<OWNER>/Qwen3.5-35B-A3B-CountBenchQA-Reproduction.git
git push -u origin main
```

Suggested GitHub description:

```text
Reproduction of Qwen3.5-35B-A3B on CountBenchQA: BF16 vs AWQ, thinking vs non-thinking, with full predictions and token statistics.
```

Suggested topics:

```text
qwen3.5 countbenchqa vlmevalkit vision-language-model awq bf16 reproducibility vllm transformers
```

After pushing:

1. Confirm the Verify archived results GitHub Action passes.
2. Check the English and Chinese README rendering.
3. Confirm no model weights, dataset TSV, credentials, or generated image caches were committed.
4. Add the repository URL to `CITATION.cff`.
5. Create a `v1.0.0` release and optionally attach a ZIP of the archived results.
