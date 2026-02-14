# Reviewer Rubric (Manual + LLM Judge)

This rubric standardizes how we review extracted health claims and generated evidence queries.
It is designed for:

1. **Manual reviewer calibration** (consistent human scoring)
2. **LLM judge automation** (same criteria, machine-applied)

## Review goals

- Prioritize **factual safety** and **traceability to source evidence**.
- Make decisions reproducible across reviewers.
- Flag high-risk items early for senior review.

## Scoring scale (all criteria)

Use the same 3-point scale for each criterion:

- **2 = Pass**: Meets the criterion clearly.
- **1 = Partial**: Mixed quality; usable with edits.
- **0 = Fail**: Does not meet minimum quality.

Optional: add a short rationale (1-2 lines) when score is 0 or 1.

---

## Per-claim rubric

Evaluate each extracted claim against all criteria below.

### 1) Extractability

**Question:** Is this a valid, explicit health claim from the transcript?

- **2 (Pass):** Claim is explicit in transcript and clearly health-related.
- **1 (Partial):** Claim is implied or phrased ambiguously but still plausibly health-related.
- **0 (Fail):** Not a health claim, or not supported by transcript content.

### 2) Atomicity

**Question:** Is this one claim rather than multiple bundled claims?

- **2 (Pass):** Single, testable proposition.
- **1 (Partial):** Mostly one claim but includes a minor secondary assertion.
- **0 (Fail):** Multiple independent claims bundled together.

### 3) Evidence span quality

**Question:** Is the quoted/linked transcript evidence relevant and sufficient?

- **2 (Pass):** Evidence span directly supports the extracted claim.
- **1 (Partial):** Evidence is related but incomplete, noisy, or over-broad.
- **0 (Fail):** Evidence is missing, off-topic, or does not support claim text.

### 4) Severity/priority

**Question:** Is the claim correctly tagged for risk-based review priority?

- **2 (Pass):** High-risk claims are clearly flagged (e.g., treatment efficacy, safety, contraindications, dosing, vulnerable populations).
- **1 (Partial):** Risk is plausible but tag is uncertain or inconsistently applied.
- **0 (Fail):** High-risk claim is not flagged, or low-risk claim is incorrectly escalated without rationale.

### Claim-level disposition (recommended)

- **Accept:** No 0 scores and total score >= 7/8.
- **Needs revision:** No critical safety miss, but total score 4-6.
- **Escalate:** Any severity/priority score of 0 on potentially harmful claims.
- **Reject:** Total score <= 3 or clear hallucination/non-extractable claim.

---

## Per-query rubric

Evaluate each generated query against all criteria below.

### 1) Searchability

**Question:** Could a literature API retrieve useful evidence for this query?

- **2 (Pass):** Terms are index-friendly and likely to return relevant biomedical literature.
- **1 (Partial):** Query has some useful keywords but is too broad, too narrow, or poorly structured.
- **0 (Fail):** Query is unlikely to retrieve meaningful evidence.

### 2) Specificity

**Question:** Are population/intervention/outcome (or equivalent elements) clear enough?

- **2 (Pass):** Query includes enough specificity to disambiguate intent (PIC(O)-like where applicable).
- **1 (Partial):** Some key elements present but important context missing.
- **0 (Fail):** Vague query with unclear target population, intervention, or outcome.

### 3) Neutrality

**Question:** Is the query non-leading and falsifiable?

- **2 (Pass):** Neutral wording that allows confirmatory or disconfirmatory evidence.
- **1 (Partial):** Mildly leading language but still testable.
- **0 (Fail):** Loaded/biased framing or not practically falsifiable.

### Query-level disposition (recommended)

- **Accept:** No 0 scores and total score >= 5/6.
- **Needs revision:** Total score 3-4.
- **Reject/regenerate:** Total score <= 2 or neutrality score of 0.

---

## LLM judge mode (implementation notes)

To align human and model reviews:

- Keep rubric text and scoring definitions in version control.
- Require structured output per item, for example:
  - `criterion_scores`: map of criterion -> {score, rationale}
  - `disposition`: accept / needs_revision / escalate / reject
  - `confidence`: low / medium / high
- Calibrate regularly against a small human-labeled set.
- Default to conservative behavior: if low confidence on safety-sensitive items, escalate.

## Suggested review record schema

Use one record per claim/query review:

```json
{
  "item_type": "claim",
  "item_id": "claim_012",
  "criterion_scores": {
    "extractability": {"score": 2, "rationale": "Explicitly stated in transcript."},
    "atomicity": {"score": 1, "rationale": "Contains one minor bundled assertion."},
    "evidence_span_quality": {"score": 2, "rationale": "Quote directly supports claim."},
    "severity_priority": {"score": 2, "rationale": "Correctly tagged high-risk."}
  },
  "total_score": 7,
  "disposition": "accept",
  "confidence": "high",
  "reviewer_type": "human"
}
```

## Open questions to revisit

- Should we split **severity** and **priority** into separate criteria?
- Should we introduce weighted scoring for safety-sensitive claim types?
- What minimum agreement threshold should we enforce between human and LLM judge?
