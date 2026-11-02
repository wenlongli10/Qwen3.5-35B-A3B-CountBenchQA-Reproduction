# Results

`final/` contains eight 487-record JSONL files: one think run per model and three nothink runs per model. Every file includes complete raw outputs and separate final answers.

`summary/final_summary.csv` reports the four displayed configurations. `summary/run_level_summary.csv` reports all eight runs. `summary/per_sample_results.csv` contains 3,896 per-sample run results. Run `python3 scripts/verify_results.py` from the repository root.
