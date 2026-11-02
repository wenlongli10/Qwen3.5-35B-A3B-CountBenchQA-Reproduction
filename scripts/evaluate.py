#!/usr/bin/env python3
import json, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = [
    ("AWQ think", "single", "awq_think.jsonl"),
    ("AWQ nothink", "original", "awq_nothink.jsonl"),
    ("AWQ nothink", "seed_1", "awq_nothink_seed1.jsonl"),
    ("AWQ nothink", "seed_2", "awq_nothink_seed2.jsonl"),
    ("BF16 think", "single", "bf16_think.jsonl"),
    ("BF16 nothink", "seed_0", "bf16_nothink.jsonl"),
    ("BF16 nothink", "seed_1", "bf16_nothink_seed1.jsonl"),
    ("BF16 nothink", "seed_2", "bf16_nothink_seed2.jsonl"),
]

def load(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def metrics(rows):
    tokens = [int(r["generated_tokens"]) for r in rows]
    correct = sum(str(r["answer"]) in r["answer_text"] for r in rows)
    return {"correct": correct, "accuracy": correct / len(rows),
            "mean": statistics.mean(tokens), "median": statistics.median(tokens),
            "max": max(tokens), "total": sum(tokens)}

def main():
    grouped = {}
    for configuration, run, filename in RUNS:
        rows = load(ROOT / "results" / "final" / filename)
        assert len(rows) == 487 and len({r["index"] for r in rows}) == 487
        result = metrics(rows); grouped.setdefault(configuration, []).append(result)
        print(f"{configuration} {run}: {result['correct']}/487 = {result['accuracy']:.2%}; "
              f"mean={result['mean']:.2f}; median={result['median']:g}; max={result['max']}")
    print("FINAL CONFIGURATIONS")
    for configuration, runs in grouped.items():
        accuracy = statistics.mean(r["accuracy"] for r in runs)
        mean_tokens = statistics.mean(r["mean"] for r in runs)
        print(f"{configuration}: runs={len(runs)}; accuracy={accuracy:.2%}; mean_tokens={mean_tokens:.2f}")

if __name__ == "__main__":
    main()
