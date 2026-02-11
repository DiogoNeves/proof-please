from __future__ import annotations

import pytest

from proof_please.pipeline.chunking import build_chunks


def test_build_chunks_with_overlap() -> None:
    items = list(range(10))
    chunks = build_chunks(items, chunk_size=4, chunk_overlap=1)
    assert chunks == [
        [0, 1, 2, 3],
        [3, 4, 5, 6],
        [6, 7, 8, 9],
    ]


@pytest.mark.parametrize(
    "chunk_size,chunk_overlap,error_text",
    [
        (0, 0, "chunk_size must be > 0"),
        (4, -1, "chunk_overlap must be >= 0"),
        (4, 4, "chunk_overlap must be smaller than chunk_size"),
    ],
)
def test_build_chunks_invalid_params(chunk_size: int, chunk_overlap: int, error_text: str) -> None:
    with pytest.raises(ValueError, match=error_text):
        build_chunks([1, 2, 3], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
