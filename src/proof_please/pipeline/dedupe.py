"""Deduplication helpers for claim/query rows."""

from __future__ import annotations

import re
from typing import Any


def _claim_dedupe_key(row: dict[str, Any]) -> tuple[str, str, tuple[str, ...]]:
    normalized_text = re.sub(r"\W+", " ", str(row.get("claim_text", "")).lower()).strip()
    evidence = row.get("evidence", [])
    seg_ids = tuple(
        sorted(
            str(item.get("seg_id", "")).strip()
            for item in evidence
            if isinstance(item, dict) and str(item.get("seg_id", "")).strip()
        )
    )
    return (str(row.get("model", "")), normalized_text, seg_ids)


def dedupe_and_assign_claim_ids(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate repeated chunk claims and assign final claim IDs."""
    unique_rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, tuple[str, ...]]] = set()
    for row in rows:
        key = _claim_dedupe_key(row)
        if key in seen:
            continue
        seen.add(key)
        unique_rows.append(row)

    final_rows: list[dict[str, Any]] = []
    for index, row in enumerate(unique_rows, start=1):
        updated = dict(row)
        updated["claim_id"] = f"clm_{index:06d}"
        final_rows.append(updated)
    return final_rows


def _query_dedupe_key(row: dict[str, Any]) -> str:
    return re.sub(r"\W+", " ", str(row.get("query", "")).lower()).strip()


def dedupe_queries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate query rows by normalized query text."""
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        key = _query_dedupe_key(row)
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique
