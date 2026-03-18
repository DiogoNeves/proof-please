# Proof, Please

Health claim extraction and scientific validation for podcast transcripts.

## Key Data Locations

- **Normalized transcript**: `data/transcripts/norm/web__the-ready-state__layne-norton__2022-10-20__v1.json`
- **Raw transcript**: `data/transcripts/raw/web__the-ready-state__layne-norton__2022-10-20__v1.json`
- **Skill outputs**: `data/outputs/` (claims-report.md, claims.jsonl, consensus-results.md, consensus-results.jsonl)
- **Whisper transcripts**: `data/transcripts/whisper/` (raw Whisper JSON, intermediate)

## Data Schemas

### Normalized Transcript (`data/transcripts/norm/*.json`)

Produced by `/get-youtube-transcript` and `/transcribe-audio`. Consumed by `/extract-claims`.

```json
{
  "doc_id": "web__the-ready-state__layne-norton__2022-10-20__v1",
  "source": {
    "type": "web_transcript | youtube_captions | local_whisper",
    "url": "...",
    "retrieved_at": "YYYY-MM-DD"
  },
  "episode": {
    "podcast_name": "...",
    "title": "...",
    "published_date": "YYYY-MM-DD | unknown"
  },
  "segments": [
    { "seg_id": "seg_000001", "speaker": "Kelly | Unknown", "start_time_s": 4, "text": "..." }
  ]
}
```

~400 segments per episode. Fits in context without chunking.

### Claims (`data/outputs/claims.jsonl`)

One JSON object per line. Produced by `/extract-claims`, enriched in place by `/check-claims`, consumed by `/get-consensus`.

After `/extract-claims` runs, each record has:

```json
{
  "claim_id": "clm_000001",
  "doc_id": "web__the-ready-state__layne-norton__2022-10-20__v1",
  "speaker": "Layne",
  "claim_text": "LDL particle count is a better predictor of cardiovascular risk than LDL cholesterol.",
  "claim_type": "medical_risk | treatment_effect | nutrition_claim | exercise_claim | epidemiology | other",
  "boldness_rating": 2,
  "evidence": [
    { "seg_id": "seg_000042", "quote": "exact verbatim quote from transcript" }
  ],
  "time_range_s": { "start": 312, "end": 341 }
}
```

After `/check-claims` runs, three query fields are added to each record:

```json
{
  "claim_id": "clm_000001",
  "...": "all fields above preserved",
  "query": "Is LDL particle count a better predictor of cardiovascular risk than LDL cholesterol?",
  "why_this_query": "Tests whether the claim's preferred biomarker has evidentiary support over standard LDL.",
  "preferred_sources": ["systematic review", "meta-analysis", "mendelian randomisation"]
}
```

### Consensus Results (`data/outputs/consensus-results.jsonl`)

One JSON object per line. Produced by `/get-consensus`.

```json
{
  "claim_id": "clm_000001",
  "query": "...",
  "consensus_verdict": "Yes | No | Mixed | Possibly | Likely | Unlikely | Insufficient evidence",
  "consensus_pct": 72,
  "result_count": 12,
  "top_papers": [
    {
      "title": "...",
      "authors": "Smith et al.",
      "year": 2021,
      "journal": "NEJM",
      "conclusion_snippet": "..."
    }
  ],
  "url": "https://consensus.app/results?q=..."
}
```

`consensus_pct` is an integer or `null` if not shown. `top_papers` contains up to 5 entries.

### Whisper Intermediate (`data/transcripts/whisper/*.json`)

Raw output from OpenAI Whisper. Kept for debugging. Not consumed by any skill directly — `/transcribe-audio` normalizes it before saving to `data/transcripts/norm/`.

```json
{
  "text": "full transcript as one string",
  "language": "en",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 4.2,
      "text": "...",
      "words": [{ "word": "Hey", "start": 0.0, "end": 0.3, "probability": 0.98 }]
    }
  ]
}
```

## Claim Types

Valid claim types: `medical_risk`, `treatment_effect`, `nutrition_claim`, `exercise_claim`, `epidemiology`, `other`.

## Transcript Acquisition

Two skills can generate normalized transcripts from external sources:
- `/get-youtube-transcript <url>` — fetches YouTube captions (no auth needed, uses `youtube-transcript-api`)
- `/transcribe-audio <file>` — local Whisper transcription (uses `openai-whisper`, requires `ffmpeg`)

Both produce normalized JSON in `data/transcripts/norm/`. The `/proof-check` skill can also accept a YouTube URL or audio file directly and will route to the appropriate acquisition skill automatically.

