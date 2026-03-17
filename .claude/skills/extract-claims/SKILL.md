---
name: extract-claims
description: Extract health and medical claims from a podcast transcript. Use when asked to extract claims, find claims, analyze a transcript for health claims, or process a transcript.
---

# Extract Health Claims from Transcript

## Overview

Read a normalized podcast transcript and extract all distinct health/medical claims. Produce a readable markdown report and a structured JSONL file.

## Input

Default transcript: `data/transcripts/norm/web__the-ready-state__layne-norton__2022-10-20__v1.json`

If the user provides a file path as an argument, use that instead.

Read the full transcript JSON file. The `segments` array contains objects with `seg_id`, `speaker`, `start_time_s`, and `text`. Process ALL segments — no chunking needed.

## Extraction Rules

1. Extract as many distinct health claims as possible from the transcript segments.
2. A claim must be either:
   - factual health/medical information presented as generally true, or
   - advice/recommendation intended to change listener behavior.
3. Exclude purely personal anecdotes about the speaker's own experience unless they are clearly generalized to others or used as advice.
4. Use `claim_type` from this set only: `medical_risk`, `treatment_effect`, `nutrition_claim`, `exercise_claim`, `epidemiology`, `other`.
5. Each claim must include at least one evidence item with an exact `seg_id` and verbatim quote from the transcript.
6. `time_range_s` start and end must be integer seconds; derive from evidence segment `start_time_s` values.
7. Add `boldness_rating` on a 1-3 scale for how bold/surprising the claim is:
   - 1 = common/unsurprising mainstream statement
   - 2 = moderately strong or somewhat surprising statement
   - 3 = very bold, counter-intuitive, or highly surprising statement
8. Prefer recall over precision: include explicit claims about risk, causality, effects, recommendations, prevalence, biomarkers, or dose-response.

## Output

### Markdown Report

Write to `data/outputs/claims-report.md` with this structure:

```markdown
# Health Claims: [Episode Title]

**Source**: [podcast name] — [episode title] ([published date])
**Transcript**: [file path]
**Date extracted**: [today's date]

## Summary

- Total claims extracted: N
- By type: medical_risk (X), treatment_effect (Y), ...
- By boldness: 1 (X), 2 (Y), 3 (Z)

## Claims

### 1. [Short claim summary]

- **Speaker**: [name]
- **Type**: [claim_type]
- **Boldness**: [rating]/3
- **Time**: [start]s – [end]s
- **Claim**: [full claim_text]
- **Evidence**:
  > "[verbatim quote]" — [seg_id]
```

### JSONL Data File

Write to `data/outputs/claims.jsonl` with one JSON object per line:

```json
{"claim_id":"clm_000001","doc_id":"...","speaker":"...","claim_text":"...","evidence":[{"seg_id":"...","quote":"..."}],"time_range_s":{"start":0,"end":0},"claim_type":"...","boldness_rating":2}
```

Number claim_ids sequentially: `clm_000001`, `clm_000002`, etc.

## Process

1. Read the transcript JSON file using the Read tool
2. Analyze ALL segments and extract claims following the rules above
3. Write the markdown report to `data/outputs/claims-report.md`
4. Write the JSONL file to `data/outputs/claims.jsonl`
5. Print a brief summary to the conversation (total claims, type breakdown, boldness breakdown)
