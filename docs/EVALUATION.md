# Evaluation protocol

All eight runs use VLMEvalKit CountBenchQA's final-answer substring rule:

```python
for pred, ans in zip(predictions, answers):
    if ans in pred:
        correct_count += 1
accuracy = correct_count / total_count
```

Here `pred` is `answer_text`, and `ans` is the ground-truth answer converted to a string.

## Aggregation

Each nothink run is scored independently. The reported accuracy is the arithmetic mean of the three run accuracies, equivalent to correct predictions divided by 1,461 pooled predictions. Mean output tokens are computed over the same outputs.

Run:

```bash
python3 scripts/evaluate.py
python3 scripts/verify_results.py
```

The verifier checks 487 aligned unique IDs per run, complete raw outputs, separate non-empty final answers, natural-stop finish reasons, exact prompt construction, run-specific seed settings, scores, token statistics, and final aggregation.

Reference: [open-compass/VLMEvalKit](https://github.com/open-compass/VLMEvalKit).
