# Evaluation protocol

All eight runs use VLMEvalKit CountBenchQA's final-answer substring rule:

```python
for pred, ans in zip(predictions, answers):
    if ans in pred:
        correct_count += 1
accuracy = correct_count / total_count
```

Here `pred` is only `answer_text`; reasoning and raw output are never concatenated into it. `ans` is the ground-truth answer converted to a string. This is deliberately substring matching, not exact numeric equality or a normalized alternative metric.

## Aggregation

Each nothink run is scored independently. The reported nothink accuracy is the arithmetic mean of the three run accuracies. Since each run has 487 samples, this is identical to correct predictions divided by 1,461 pooled predictions. Mean output tokens are computed over the same pooled outputs. There is no majority voting, per-sample best selection, or best-of-N.

Run:

```bash
python3 scripts/evaluate.py
python3 scripts/verify_results.py
```

The verifier checks 487 aligned unique IDs per run, complete raw outputs, separate non-empty final answers, natural-stop finish reasons, exact prompt construction, run-specific seed settings, scores, token statistics, and final aggregation.

Reference: [open-compass/VLMEvalKit](https://github.com/open-compass/VLMEvalKit).
