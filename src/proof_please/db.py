"""DuckDB helpers for local data bootstrapping."""

from pathlib import Path

import duckdb


def get_connection(db_path: str) -> duckdb.DuckDBPyConnection:
    """Create a DuckDB connection, ensuring the parent folder exists."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(path))


def init_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """Create initial tables used by the project."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS health_claims (
            id BIGINT PRIMARY KEY,
            source_id TEXT NOT NULL,
            speaker TEXT,
            claim_text TEXT NOT NULL,
            extracted_at TIMESTAMP DEFAULT current_timestamp
        )
        """
    )
