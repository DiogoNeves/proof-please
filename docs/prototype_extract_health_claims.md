# Prototype: Extract Health Claims

This document explains what `scripts/prototype_extract_health_claims.py` currently does.

## Purpose

The script is a local prototype for:

1. Extracting health-related claims from normalized transcript segments.
2. Generating validation search queries for those claims.

It uses a local Ollama model and writes JSONL artifacts in `data/`.

## Inputs

- Transcript input (default):
  - `data/transcripts/norm/web__the-ready-state__layne-norton__2022-10-20__v1.json`
- Or existing claims input:
  - `--claims-input data/claims.jsonl` (skips claim extraction stage)
- Ollama endpoint:
  - `--ollama-url` (default: `http://127.0.0.1:11434`)
- Model selection:
  - `--models` for extraction
  - `--query-model` for query generation

## Outputs

- Claims JSONL:
  - `data/claims.jsonl`
- Query JSONL:
  - `data/claim_queries.jsonl`

## Stage 1: Claim Extraction

The script:

1. Loads transcript `segments`.
2. Splits transcript into overlapping chunks (`--chunk-size`, `--chunk-overlap`).
3. Prompts Ollama to extract factual health claims in strict JSON.
4. Normalizes each claim row and writes:
   - `claim_id`
   - `doc_id`
   - `speaker`
   - `claim_text`
   - `evidence` (`seg_id` + quote)
   - `time_range_s`
   - `claim_type`
   - `boldness_rating` (1-3)
   - `model`
5. Deduplicates repeated chunk outputs.

### Claim Type Set

- `medical_risk`
- `treatment_effect`
- `nutrition_claim`
- `exercise_claim`
- `epidemiology`
- `other`

### Boldness Rating

- `1`: mainstream / unsurprising
- `2`: moderately strong / somewhat surprising
- `3`: bold / counter-intuitive / highly surprising

## Stage 2: Query Generation

The script can generate validation queries from claims:

1. Uses extracted claims or `--claims-input`.
2. Chunks claim rows (`--query-chunk-size`, `--query-chunk-overlap`).
3. Prompts Ollama to produce concise, natural question-form queries.
4. Allows one query to represent multiple similar claims.
5. Normalizes and deduplicates queries.
6. Fallback logic creates heuristic queries for uncovered claims.

Each query row includes:

- `claim_id`
- `query`
- `why_this_query`
- `preferred_sources`

## Useful Run Modes

### Extract claims only

```bash
uv run python scripts/prototype_extract_health_claims.py \
  --models qwen3:4b \
  --no-generate-queries \
  --no-list-claims \
  --output data/claims.jsonl
```

### Generate queries only (from existing claims)

```bash
uv run python scripts/prototype_extract_health_claims.py \
  --claims-input data/claims.jsonl \
  --models qwen3:4b \
  --query-model qwen3:4b \
  --no-list-claims \
  --queries-output data/claim_queries.jsonl
```

### List local Ollama models

```bash
uv run python scripts/prototype_extract_health_claims.py --list-models
```

## Current Prototype Characteristics

- Local, model-prompt based extraction (not deterministic).
- Recall-first behavior (can include noisy claims).
- Query generation includes fallback heuristics for coverage.
- Designed for quick iteration, not final production quality.

