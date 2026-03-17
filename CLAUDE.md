# Proof, Please

Health claim extraction and scientific validation for podcast transcripts.

## Key Data Locations

- **Normalized transcript**: `data/transcripts/norm/web__the-ready-state__layne-norton__2022-10-20__v1.json`
- **Raw transcript**: `data/transcripts/raw/web__the-ready-state__layne-norton__2022-10-20__v1.json`
- **Python pipeline outputs**: `data/claims.jsonl`, `data/claim_queries.jsonl`
- **Skill outputs**: `data/outputs/` (claims-report.md, claims.jsonl, queries-report.md, queries.jsonl)

## Transcript Format

The normalized transcript JSON has this structure:

```json
{
  "doc_id": "web__the-ready-state__layne-norton__2022-10-20__v1",
  "source": { "type": "web_transcript", "url": "...", "retrieved_at": "..." },
  "episode": { "podcast_name": "...", "title": "...", "published_date": "..." },
  "segments": [
    { "seg_id": "seg_000001", "speaker": "Kelly", "start_time_s": 4, "text": "..." }
  ]
}
```

Approximately 400 segments (~1034 lines of JSON). Fits comfortably in context without chunking.

## Claim Types

Valid claim types: `medical_risk`, `treatment_effect`, `nutrition_claim`, `exercise_claim`, `epidemiology`, `other`.

## Architecture Note

The Python pipeline in `src/proof_please/pipeline/` is the original implementation using local LLMs via Ollama. The Claude Code skills in `.claude/skills/` are an alternative interface that uses Claude directly. Both coexist — the skills do not modify or depend on the Python code.

See `AGENTS.md` for coding conventions, testing guidelines, and development expectations.
