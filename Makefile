.PHONY: verify data

verify:
	python3 scripts/verify_results.py

data:
	bash data/download.sh
