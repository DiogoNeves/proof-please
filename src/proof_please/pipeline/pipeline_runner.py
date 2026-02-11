"""Top-level orchestration helpers for the prototype pipeline CLI."""

from __future__ import annotations

import urllib.error
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from proof_please.pipeline.extract_claims import extract_claims_for_models
from proof_please.pipeline.generate_queries import choose_query_model, generate_validation_queries
from proof_please.pipeline.io import load_transcript
from proof_please.pipeline.models import OllamaConfig
from proof_please.pipeline.ollama_client import list_ollama_models


def parse_model_list(models: str) -> list[str]:
    """Parse comma-separated model list."""
    return [model.strip() for model in models.split(",") if model.strip()]


def validate_common_args(timeout: float, max_segments: int) -> None:
    """Validate shared runtime parameters."""
    if timeout <= 0:
        raise typer.BadParameter("--timeout must be > 0")
    if max_segments < 0:
        raise typer.BadParameter("--max-segments must be >= 0")


def validate_path_exists(path: Path, flag_name: str) -> None:
    """Validate path existence for CLI options."""
    if not path.exists():
        raise typer.BadParameter(f"{flag_name} path does not exist: {path}")


def _validate_chunking_for_cli(chunk_size: int, chunk_overlap: int, label: str) -> None:
    if chunk_size <= 0:
        raise typer.BadParameter(f"--{label}-size must be > 0")
    if chunk_overlap < 0:
        raise typer.BadParameter(f"--{label}-overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise typer.BadParameter(f"--{label}-overlap must be smaller than --{label}-size")


def fetch_available_models(config: OllamaConfig) -> list[str]:
    """Fetch available local Ollama models with CLI-friendly errors."""
    try:
        return list_ollama_models(config)
    except urllib.error.URLError as exc:
        raise typer.BadParameter(
            f"Could not connect to Ollama at {config.base_url}: {exc}"
        ) from exc


def warn_missing_models(requested_models: list[str], available_models: list[str], console: Console) -> None:
    """Print warning when requested model names are not available."""
    missing = [name for name in requested_models if name not in available_models]
    if missing:
        console.print(f"[yellow]Requested models not found in /api/tags: {missing}[/yellow]")


def run_claim_extraction(
    transcript: Path,
    model_list: list[str],
    config: OllamaConfig,
    max_segments: int,
    chunk_size: int,
    chunk_overlap: int,
    console: Console,
) -> list[dict[str, Any]]:
    """Run transcript claim extraction and return deduplicated claim rows."""
    if not model_list:
        raise typer.BadParameter("No models provided.")

    validate_path_exists(transcript, "--transcript")
    validate_common_args(timeout=config.timeout, max_segments=max_segments)
    _validate_chunking_for_cli(chunk_size=chunk_size, chunk_overlap=chunk_overlap, label="chunk")

    doc_id, segments = load_transcript(transcript)
    if max_segments > 0:
        segments = segments[:max_segments]

    return extract_claims_for_models(
        doc_id=doc_id,
        segments=segments,
        model_list=model_list,
        config=config,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        console=console,
    )


def run_query_generation(
    claims: list[dict[str, Any]],
    config: OllamaConfig,
    query_model: str | None,
    model_list: list[str],
    available_models: list[str],
    chunk_size: int,
    chunk_overlap: int,
    console: Console,
) -> list[dict[str, Any]]:
    """Generate validation queries from existing claim rows."""
    _validate_chunking_for_cli(chunk_size=chunk_size, chunk_overlap=chunk_overlap, label="query-chunk")
    selected_query_model = choose_query_model(
        query_model=query_model,
        model_list=model_list,
        available_models=available_models,
    )
    if selected_query_model is None:
        console.print(
            "[yellow]Skipping query generation: no model available. "
            "Use --query-model or install a local Ollama model.[/yellow]"
        )
        return []

    console.print(f"[cyan]Generating validation queries with:[/cyan] {selected_query_model}")
    return generate_validation_queries(
        claims=claims,
        config=config,
        query_model=selected_query_model,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        console=console,
    )
