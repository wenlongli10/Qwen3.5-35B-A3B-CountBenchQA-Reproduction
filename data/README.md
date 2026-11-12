# CountBenchQA data

Download the revised TSV with:

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

License and source references are listed in [`THIRD_PARTY.md`](../THIRD_PARTY.md).
