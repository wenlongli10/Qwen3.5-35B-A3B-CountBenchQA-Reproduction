# Scripts

`run_countbench.py` is the single basic inference entry point. Choose `--backend awq|bf16`, `--mode think|nothink`, an optional `--seed`, and a new output directory for each independent run.

`evaluate.py` recomputes run-level and final metrics. `verify_results.py` checks all eight archived runs, complete raw outputs, scores, seeds, token statistics, and nothink three-run aggregation. See `docs/REPRODUCE.md`.
