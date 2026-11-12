# Results

All scores use `answer_text` only. Every run has 487 complete raw outputs and natural-stop final records.

## Final configurations

Think values are from one run. Nothink accuracy and mean token count are arithmetic means of three independent runs; pooled token statistics use all 1,461 nothink outputs.

| Configuration | Runs | Mean correct / 487 | Accuracy | Mean | Median | P95 | P99 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AWQ think | 1 | 472.00 | 96.92% | 952.06 | 341 | 3376.50 | 13064.38 | 30627 |
| AWQ nothink | 3 | 439.67 | 90.28% | 2.10 | 2 | 3 | 3 | 3 |
| BF16 think | 1 | 468.00 | 96.10% | 923.02 | 313 | 2659.90 | 14631.38 | 39865 |
| BF16 nothink | 3 | 444.67 | 91.31% | 2.12 | 2 | 3 | 3 | 3 |

The nothink mean accuracies equal pooled accuracies because all runs have equal size: AWQ 1,319/1,461 and BF16 1,334/1,461.

## Independent runs

| Configuration | Run | Seed | Correct | Accuracy | Mean | Median | Max | Total tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| AWQ think | single | not fixed | 472/487 | 96.92% | 952.06 | 341 | 30627 | 463,651 |
| AWQ nothink | original | not fixed | 438/487 | 89.94% | 2.09 | 2 | 3 | 1,018 |
| AWQ nothink | seed 1 | 1 | 438/487 | 89.94% | 2.10 | 2 | 3 | 1,023 |
| AWQ nothink | seed 2 | 2 | 443/487 | 90.97% | 2.10 | 2 | 3 | 1,022 |
| BF16 think | single | 0 | 468/487 | 96.10% | 923.02 | 313 | 39865 | 449,513 |
| BF16 nothink | original | 0 | 449/487 | 92.20% | 2.13 | 2 | 3 | 1,037 |
| BF16 nothink | seed 1 | 1 | 435/487 | 89.32% | 2.12 | 2 | 3 | 1,034 |
| BF16 nothink | seed 2 | 2 | 450/487 | 92.40% | 2.10 | 2 | 3 | 1,024 |

Tokens include reasoning and final answers. Backend and sampling settings are listed in the experiment protocol.
