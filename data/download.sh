#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
URL="${COUNTBENCH_URL:-https://opencompass.openxlab.space/utils/VLMEval/CountBenchQA.tsv}"
DEST="$ROOT/data/CountBenchQA.tsv"
EXPECTED="fc73c8d4ffa665431448753f094d56ff"
mkdir -p "$ROOT/data"
if [[ ! -f "$DEST" ]]; then
  curl -L --fail --retry 3 --connect-timeout 30 "$URL" -o "$DEST.tmp"
  mv "$DEST.tmp" "$DEST"
fi
if command -v md5sum >/dev/null 2>&1; then
  ACTUAL="$(md5sum "$DEST" | awk '{print $1}')"
else
  ACTUAL="$(python3 -c 'import hashlib,sys; print(hashlib.md5(open(sys.argv[1],"rb").read()).hexdigest())' "$DEST")"
fi
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "MD5 mismatch: expected $EXPECTED, got $ACTUAL" >&2
  exit 1
fi
printf 'Dataset verified: %s\nMD5: %s\n' "$DEST" "$ACTUAL"
