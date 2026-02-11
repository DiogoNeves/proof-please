from __future__ import annotations

from proof_please.pipeline.dedupe import dedupe_and_assign_claim_ids, dedupe_queries


def test_claim_dedupe_and_deterministic_ids() -> None:
    rows = [
        {
            "model": "qwen3:4b",
            "claim_text": "LDL raises risk",
            "evidence": [{"seg_id": "seg_000001", "quote": "LDL raises risk"}],
        },
        {
            "model": "qwen3:4b",
            "claim_text": "LDL raises risk.",
            "evidence": [{"seg_id": "seg_000001", "quote": "LDL raises risk"}],
        },
        {
            "model": "qwen3:4b",
            "claim_text": "Fiber lowers LDL",
            "evidence": [{"seg_id": "seg_000002", "quote": "Fiber lowers LDL"}],
        },
    ]

    deduped = dedupe_and_assign_claim_ids(rows)

    assert len(deduped) == 2
    assert [row["claim_id"] for row in deduped] == ["clm_000001", "clm_000002"]


def test_query_dedupe() -> None:
    rows = [
        {"query": "Is LDL an independent risk factor?"},
        {"query": "is LDL an independent risk factor"},
        {"query": "Does fiber lower LDL?"},
    ]

    deduped = dedupe_queries(rows)

    assert len(deduped) == 2
    assert deduped[0]["query"] == "Is LDL an independent risk factor?"
    assert deduped[1]["query"] == "Does fiber lower LDL?"
