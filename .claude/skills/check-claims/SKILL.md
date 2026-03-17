---
name: check-claims
description: Generate scientific validation queries for extracted health claims. Use when asked to check claims, validate claims, generate queries, find evidence for claims, or verify health claims against science.
---

# Generate Validation Queries for Health Claims

## Overview

Read extracted health claims and generate literature-search queries to validate each one against scientific evidence. Produce a readable markdown report and a structured JSONL file.

## Input

Default claims file: `data/outputs/claims.jsonl`

If that file does not exist, fall back to: `data/claims.jsonl`

If the user provides a file path as an argument, use that instead.

Read the JSONL file — each line is a JSON object with `claim_id`, `claim_text`, `claim_type`, `speaker`, `boldness_rating`, and other fields.

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

### Markdown Report

Write to `data/outputs/queries-report.md` with this structure:

```markdown
# Validation Queries: [Episode Title]

**Source claims**: [file path]
**Date generated**: [today's date]

## Summary

- Total queries generated: N
- Claims covered: X / Y total claims
- Preferred source breakdown: systematic review (A), meta-analysis (B), ...

## Queries

### 1. [claim_id] — [short claim summary]

- **Claim**: [claim_text]
- **Query**: [the search query]
- **Why**: [why_this_query]
- **Preferred sources**: systematic review, meta-analysis, ...
```

### JSONL Data File

Write to `data/outputs/queries.jsonl` with one JSON object per line:

```json
{"claim_id":"clm_000001","query":"...","why_this_query":"...","preferred_sources":["systematic review","meta-analysis"]}
```

## Process

1. Read the claims JSONL file using the Read tool
2. Generate validation queries following the rules above
3. Ensure every claim has at least one query (merge similar claims if appropriate)
4. Write the markdown report to `data/outputs/queries-report.md`
5. Write the JSONL file to `data/outputs/queries.jsonl`
6. Print a brief summary to the conversation (total queries, coverage, source type breakdown)
