# Proof, Please

Proof, Please is an experimental lab for checking health claims made in podcast transcripts and grounding those claims in peer-reviewed evidence.

The core idea is simple: extract concrete claims from transcript text, query scientific literature, and summarize where research consensus appears to be strong, mixed, or unclear.

## Current Status

- Transcript ingestion/normalization prototype:
  - `skills/get-transcript-from-url/scripts/extract_web_transcript.py`
  - `scripts/normalize_raw_transcript_segments.py`
- Claim extraction and query-generation prototype:
  - CLI entrypoint: `scripts/prototype_extract_health_claims.py`
  - Implementation modules: `src/proof_please/pipeline/`
- Core app scaffolding:
  - `uv run proof-please config`
  - `uv run proof-please init-db`
  - `uv run proof-please extract-claims ...` (currently placeholder/not implemented)
- Local DuckDB schema bootstrap in `data/proof_please.duckdb`.

## Documentation

- `docs/README.md`: docs index
- `docs/transcript_formats.md`: raw + normalized transcript formats and file layout
- `docs/prototype_extract_health_claims.md`: command-level walkthrough for the claims prototype

## Consensus API

This project is designed to use the Consensus API to fetch relevant papers and metadata for each claim:

- Product page: `https://consensus.app/home/api/`
- API docs: `https://docs.consensus.app/reference/v1_quick_search`
- Current reference endpoint: `GET https://api.consensus.app/v1/quick_search`

Note: Consensus API access is application-based, so you may need approved access before live calls are possible.
Current prototype code does not yet call the Consensus API directly.

## Setup

```bash
uv sync
```

## Core App Commands

```bash
just sync
just init-db
just run config
just extract-claims path/to/transcript.txt
uv run proof-please --help
```

Note: `just extract-claims` currently calls a placeholder command in `src/proof_please/cli.py`.

## Prototype Pipeline Commands

Use the prototype script for actual transcript claim extraction/query generation:

```bash
uv run python scripts/prototype_extract_health_claims.py --help
uv run python scripts/prototype_extract_health_claims.py extract-claims --help
uv run python scripts/prototype_extract_health_claims.py generate-queries --help
uv run python scripts/prototype_extract_health_claims.py run-pipeline --help
```

Normalize raw transcript JSON into segmented transcript JSON:

```bash
uv run python scripts/normalize_raw_transcript_segments.py --help
```

## Configuration

- Environment variables use the `PP_` prefix.
- Default database path is `data/proof_please.duckdb`.

## Development Approach

This repository is intentionally iterative and experimental. Expect small, reversible changes as the problem definition improves with real transcripts and evidence-review feedback.
