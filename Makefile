.PHONY: setup ingest eval
setup:
	uv sync

ingest:
	uv run python scripts/ingest.py

eval:
	uv run python scripts/eval.py

process:
	uv run python -m scripts.process

embed:
	uv run python -m scripts.embed