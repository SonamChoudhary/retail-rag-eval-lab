.PHONY: setup ingest eval
setup:
	uv sync

ingest:
	uv run python scripts/ingest.py

eval:
	uv run python scripts/eval.py