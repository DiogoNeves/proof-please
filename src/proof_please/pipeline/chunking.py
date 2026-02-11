"""Chunking helpers for transcripts and claim lists."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def build_chunks(items: list[T], chunk_size: int, chunk_overlap: int) -> list[list[T]]:
    """Split items into overlapping chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: list[list[T]] = []
    step = chunk_size - chunk_overlap
    for start in range(0, len(items), step):
        chunk = items[start : start + chunk_size]
        if not chunk:
            continue
        chunks.append(chunk)
        if start + chunk_size >= len(items):
            break
    return chunks
