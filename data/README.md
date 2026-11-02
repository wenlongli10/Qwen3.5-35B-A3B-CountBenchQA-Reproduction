# CountBenchQA data

This repository does not redistribute the revised TSV. Download it with:

```bash
bash data/download.sh
```

Primary URL: [Download CountBenchQA.tsv](https://opencompass.openxlab.space/utils/VLMEval/CountBenchQA.tsv).

Source references:

- [OpenCompass VLMEvalKit](https://github.com/open-compass/VLMEvalKit)
- [CountBenchQA on Hugging Face](https://huggingface.co/datasets/vikhyatk/CountBenchQA)
- [Original CountBench images on Hugging Face](https://huggingface.co/datasets/nielsr/countbench)

Expected properties:

| Property | Value |
|---|---|
| File | `CountBenchQA.tsv` |
| Samples | 487 |
| MD5 | `fc73c8d4ffa665431448753f094d56ff` |

The TSV contains base64-encoded images, questions, answers, and sample indices. Model inputs use the original image bytes and the question plus the documented suffix. Answer fields are used only after generation for scoring.

CountBench upstream is commonly distributed under CC-BY-4.0, but users must review the terms and attribution requirements of the exact revised CountBenchQA artifact and its upstream sources before reuse or redistribution. See `THIRD_PARTY.md`.
