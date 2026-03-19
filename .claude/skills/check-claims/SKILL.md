---
name: check-claims
description: Generate scientific validation queries for extracted health claims. Use when asked to check claims, validate claims, generate queries, find evidence for claims, or verify health claims against science.
---

# Generate Validation Queries for Health Claims

## Overview

Read extracted health claims and generate literature-search queries to validate each one against scientific evidence. Enriches `claims.jsonl` in place by adding query fields to each record.

## Input

Default claims file: `data/outputs/claims.jsonl`

If that file does not exist, fall back to: `data/claims.jsonl`

If the user provides a file path as an argument, use that instead.

Read the JSONL file — each line is a JSON object. See CLAUDE.md for the full schema. Key fields used by this skill:
- `claim_id` — unique identifier (e.g. `clm_000001`)
- `claim_text` — the full claim statement
- `claim_type` — one of: `medical_risk`, `treatment_effect`, `nutrition_claim`, `exercise_claim`, `epidemiology`, `other`
- `boldness_rating` — 1–3 (prioritise bold/surprising claims for query generation)
- `speaker` — who made the claim
- `evidence` — array of `{seg_id, quote}` (for context if needed)

## Query Generation Rules

1. Generate as many high-value validation queries as possible for the claims.
2. You may merge very similar claims into one query and use one representative `claim_id`.
3. Phrase each query naturally and directly as a question a human would type in search.
   - Good: "Is LDL cholesterol an independent risk factor for heart disease?"
   - Good: "Does reducing saturated fat lower LDL cholesterol?"
   - Bad: "What is the current scientific consensus on whether LDL cholesterol is an independent risk factor for heart disease?"
4. Keep queries concise and optimized for evidence retrieval.
5. Do not use repetitive scaffolding such as "What is the current scientific consensus on...".
6. Prefer question openings like Is/Are/Does/Do/Can/Should/How much.
7. Do not append source types inside `query`; keep source types only in `preferred_sources`.
8. Prefer source types like systematic review, meta-analysis, guideline, mendelian randomisation, RCT.
9. For each query, explain briefly why this query validates the claim (`why_this_query`).

## Output

Enrich `claims.jsonl` in place: read all records, add `query`, `why_this_query`, and `preferred_sources` to each, then overwrite the file. The schema for each enriched record is in CLAUDE.md.

```json
{"claim_id":"clm_000001","doc_id":"...","speaker":"...","claim_text":"...","claim_type":"treatment_effect","boldness_rating":2,"evidence":[{"seg_id":"seg_000042","quote":"..."}],"time_range_s":{"start":312,"end":341},"query":"...","why_this_query":"...","preferred_sources":["systematic review","meta-analysis"]}
```

Claims that were merged under a shared query still get their own record; copy the same `query`, `why_this_query`, and `preferred_sources` to each merged claim's record.

## Process

1. Read the claims JSONL file using the Read tool
2. Generate validation queries following the rules above
3. Ensure every claim has at least one query (merge similar claims if appropriate)
4. Overwrite the input JSONL file with enriched records (all original fields preserved, query fields added)
5. Print a brief summary to the conversation (total queries, coverage, source type breakdown)
