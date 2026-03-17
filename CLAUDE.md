# Proof, Please

Health claim extraction and scientific validation for podcast transcripts.

## Key Data Locations

- **Normalized transcript**: `data/transcripts/norm/web__the-ready-state__layne-norton__2022-10-20__v1.json`
- **Raw transcript**: `data/transcripts/raw/web__the-ready-state__layne-norton__2022-10-20__v1.json`
- **Skill outputs**: `data/outputs/` (claims-report.md, claims.jsonl, queries-report.md, queries.jsonl, consensus-results.md, consensus-results.jsonl)
- **Whisper transcripts**: `data/transcripts/whisper/` (raw Whisper JSON, intermediate)

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

## Transcript Acquisition

Two skills can generate normalized transcripts from external sources:
- `/get-youtube-transcript <url>` — fetches YouTube captions (no auth needed, uses `youtube-transcript-api`)
- `/transcribe-audio <file>` — local Whisper transcription (uses `openai-whisper`, requires `ffmpeg`)

Both produce normalized JSON in `data/transcripts/norm/`. The `/proof-check` skill can also accept a YouTube URL or audio file directly and will route to the appropriate acquisition skill automatically.

