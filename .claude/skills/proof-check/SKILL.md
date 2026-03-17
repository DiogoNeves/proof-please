---
name: proof-check
description: Run the full proof-checking pipeline on a podcast transcript end-to-end. Extracts health claims then generates validation queries. Use when asked to proof check, run the pipeline, or analyze a transcript end to end.
---

# Proof Check Pipeline

## Overview

Run the complete proof-checking pipeline: extract health claims from a podcast transcript, then generate scientific validation queries for each claim. This combines the `/extract-claims` and `/check-claims` skills into one end-to-end workflow.

## Input

Accepts a YouTube URL, a local audio/video file path, a transcript JSON file path, or no argument (uses default).

Default transcript: `data/transcripts/norm/web__the-ready-state__layne-norton__2022-10-20__v1.json`

## Process

### Step 0: Route Input

Determine what kind of input was provided and acquire a transcript if needed:

- **YouTube URL** (contains `youtube.com` or `youtu.be`): Follow the `/get-youtube-transcript` workflow from `.claude/skills/get-youtube-transcript/SKILL.md` to fetch and save the transcript first. Then use the resulting normalized JSON file as input.
- **Audio/video file** (extension is `.mp3`, `.mp4`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.webm`, `.avi`, `.mkv`): Follow the `/transcribe-audio` workflow from `.claude/skills/transcribe-audio/SKILL.md` to transcribe and save the transcript first. Then use the resulting normalized JSON file as input.
- **JSON file path**: Use directly as transcript input.
- **No argument**: Use the default Layne Norton transcript.

### Step 1: Extract Claims

Follow the full workflow from `.claude/skills/extract-claims/SKILL.md`:

1. Read the transcript JSON file
2. Extract all health/medical claims using the extraction rules (see that skill for the 8 rules)
3. Write `data/outputs/claims-report.md` and `data/outputs/claims.jsonl`

### Step 2: Generate Validation Queries

Follow the full workflow from `.claude/skills/check-claims/SKILL.md`:

1. Read the claims from `data/outputs/claims.jsonl` (just created in Step 1)
2. Generate validation queries using the query rules (see that skill for the 9 rules)
3. Write `data/outputs/queries-report.md` and `data/outputs/queries.jsonl`

### Step 3: Write Combined Summary

Write to `data/outputs/proof-check-summary.md`:

```markdown
# Proof Check Summary: [Episode Title]

**Date**: [today's date]
**Transcript**: [file path]

## Pipeline Results

- Claims extracted: N
- Validation queries generated: M
- Claims covered by queries: X / N

## Boldest Claims (rating 3)

[For each boldness=3 claim, show the claim text and its validation query]

## All Claims by Type

[Group claims by claim_type with counts]

## Files Generated

- Claims report: data/outputs/claims-report.md
- Claims data: data/outputs/claims.jsonl
- Queries report: data/outputs/queries-report.md
- Queries data: data/outputs/queries.jsonl
- This summary: data/outputs/proof-check-summary.md
```

### Step 4: Print Summary

Print the combined summary to the conversation so the user can see results immediately.
