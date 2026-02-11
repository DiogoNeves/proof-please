"""Prototype CLI for health-claim extraction and validation-query generation."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from proof_please.pipeline import (
    OllamaConfig,
    fetch_available_models,
    load_claims_jsonl,
    parse_model_list,
    print_claim_rows,
    print_query_rows,
    run_claim_extraction,
    run_query_generation,
    validate_common_args,
    validate_path_exists,
    warn_missing_models,
    write_jsonl,
)

console = Console()

DEFAULT_INPUT = Path("data/transcripts/norm/web__the-ready-state__layne-norton__2022-10-20__v1.json")
DEFAULT_OUTPUT = Path("data/claims.jsonl")
DEFAULT_QUERIES_OUTPUT = Path("data/claim_queries.jsonl")
DEFAULT_MODELS = "gpt-oss:20b,qwen3:4b"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"

app = typer.Typer(help="Prototype commands for extracting health claims and validation queries.")

TRANSCRIPT_OPTION = typer.Option(
    DEFAULT_INPUT,
    "--transcript",
    help="Path to normalized transcript JSON with segments.",
)
CLAIMS_OUTPUT_OPTION = typer.Option(
    DEFAULT_OUTPUT,
    "--output",
    help="Output JSONL file path for extracted claims.",
)
CLAIMS_INPUT_OPTION = typer.Option(
    DEFAULT_OUTPUT,
    "--claims-input",
    help="Existing claims JSONL used as query-generation input.",
)
QUERIES_OUTPUT_OPTION = typer.Option(
    DEFAULT_QUERIES_OUTPUT,
    "--queries-output",
    help="Output JSONL file for validation queries.",
)
MODELS_OPTION = typer.Option(
    DEFAULT_MODELS,
    "--models",
    help="Comma-separated model names for extraction and query-model fallback selection.",
)
QUERY_MODEL_OPTION = typer.Option(
    None,
    "--query-model",
    help="Model for query generation (default: first available model from --models).",
)
OLLAMA_URL_OPTION = typer.Option(
    DEFAULT_OLLAMA_URL,
    "--ollama-url",
    help="Ollama base URL.",
)
TIMEOUT_OPTION = typer.Option(
    180.0,
    "--timeout",
    help="Ollama request timeout in seconds.",
)
MAX_SEGMENTS_OPTION = typer.Option(
    0,
    "--max-segments",
    help="Optional cap on transcript segments to process (0 = all).",
)
CHUNK_SIZE_OPTION = typer.Option(
    45,
    "--chunk-size",
    help="Transcript segments per model call.",
)
CHUNK_OVERLAP_OPTION = typer.Option(
    12,
    "--chunk-overlap",
    help="Segment overlap between adjacent chunks.",
)
QUERY_CHUNK_SIZE_OPTION = typer.Option(
    25,
    "--query-chunk-size",
    help="Claims per query-generation model call.",
)
QUERY_CHUNK_OVERLAP_OPTION = typer.Option(
    5,
    "--query-chunk-overlap",
    help="Claims overlap between query-generation chunks.",
)
LIST_CLAIMS_OPTION = typer.Option(
    True,
    "--list-claims/--no-list-claims",
    help="Print extracted claims after writing output.",
)
LIST_QUERIES_OPTION = typer.Option(
    True,
    "--list-queries/--no-list-queries",
    help="Print generated validation queries after writing output.",
)


@app.command("extract-claims")
def extract_claims_command(
    transcript: Path = TRANSCRIPT_OPTION,
    output: Path = CLAIMS_OUTPUT_OPTION,
    models: str = MODELS_OPTION,
    ollama_url: str = OLLAMA_URL_OPTION,
    timeout: float = TIMEOUT_OPTION,
    max_segments: int = MAX_SEGMENTS_OPTION,
    chunk_size: int = CHUNK_SIZE_OPTION,
    chunk_overlap: int = CHUNK_OVERLAP_OPTION,
    list_claims: bool = LIST_CLAIMS_OPTION,
) -> None:
    """Extract claims from transcript segments and write claims JSONL."""
    model_list = parse_model_list(models)
    if not model_list:
        raise typer.BadParameter("No models provided.")

    config = OllamaConfig(base_url=ollama_url, timeout=timeout)
    available_models = fetch_available_models(config)
    warn_missing_models(model_list, available_models, console)

    all_rows = run_claim_extraction(
        transcript=transcript,
        model_list=model_list,
        config=config,
        max_segments=max_segments,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        console=console,
    )
    write_jsonl(output, all_rows)
    console.print(f"[bold green]Wrote {len(all_rows)} claims to {output}[/bold green]")
    if list_claims:
        print_claim_rows(all_rows, console)


@app.command("generate-queries")
def generate_queries_command(
    claims_input: Path = CLAIMS_INPUT_OPTION,
    queries_output: Path = QUERIES_OUTPUT_OPTION,
    models: str = MODELS_OPTION,
    query_model: str | None = QUERY_MODEL_OPTION,
    ollama_url: str = OLLAMA_URL_OPTION,
    timeout: float = TIMEOUT_OPTION,
    query_chunk_size: int = QUERY_CHUNK_SIZE_OPTION,
    query_chunk_overlap: int = QUERY_CHUNK_OVERLAP_OPTION,
    list_queries: bool = LIST_QUERIES_OPTION,
) -> None:
    """Generate validation queries from an existing claims JSONL file."""
    validate_path_exists(claims_input, "--claims-input")
    validate_common_args(timeout=timeout, max_segments=0)

    model_list = parse_model_list(models)
    config = OllamaConfig(base_url=ollama_url, timeout=timeout)
    available_models = fetch_available_models(config)
    warn_missing_models(model_list, available_models, console)

    claims = load_claims_jsonl(claims_input)
    console.print(f"[green]Loaded {len(claims)} claims from {claims_input}[/green]")
    query_rows = run_query_generation(
        claims=claims,
        config=config,
        query_model=query_model,
        model_list=model_list,
        available_models=available_models,
        chunk_size=query_chunk_size,
        chunk_overlap=query_chunk_overlap,
        console=console,
    )
    write_jsonl(queries_output, query_rows)
    console.print(
        f"[bold green]Wrote {len(query_rows)} validation queries to {queries_output}[/bold green]"
    )
    if list_queries:
        print_query_rows(query_rows, console)


@app.command("run-pipeline")
def run_pipeline_command(
    transcript: Path = TRANSCRIPT_OPTION,
    output: Path = CLAIMS_OUTPUT_OPTION,
    queries_output: Path = QUERIES_OUTPUT_OPTION,
    models: str = MODELS_OPTION,
    query_model: str | None = QUERY_MODEL_OPTION,
    ollama_url: str = OLLAMA_URL_OPTION,
    timeout: float = TIMEOUT_OPTION,
    max_segments: int = MAX_SEGMENTS_OPTION,
    chunk_size: int = CHUNK_SIZE_OPTION,
    chunk_overlap: int = CHUNK_OVERLAP_OPTION,
    query_chunk_size: int = QUERY_CHUNK_SIZE_OPTION,
    query_chunk_overlap: int = QUERY_CHUNK_OVERLAP_OPTION,
    list_claims: bool = LIST_CLAIMS_OPTION,
    list_queries: bool = LIST_QUERIES_OPTION,
) -> None:
    """Run extraction and query generation end-to-end."""
    model_list = parse_model_list(models)
    if not model_list:
        raise typer.BadParameter("No models provided.")

    config = OllamaConfig(base_url=ollama_url, timeout=timeout)
    available_models = fetch_available_models(config)
    warn_missing_models(model_list, available_models, console)

    all_rows = run_claim_extraction(
        transcript=transcript,
        model_list=model_list,
        config=config,
        max_segments=max_segments,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        console=console,
    )
    write_jsonl(output, all_rows)
    console.print(f"[bold green]Wrote {len(all_rows)} claims to {output}[/bold green]")
    if list_claims:
        print_claim_rows(all_rows, console)

    query_rows = run_query_generation(
        claims=all_rows,
        config=config,
        query_model=query_model,
        model_list=model_list,
        available_models=available_models,
        chunk_size=query_chunk_size,
        chunk_overlap=query_chunk_overlap,
        console=console,
    )
    write_jsonl(queries_output, query_rows)
    console.print(
        f"[bold green]Wrote {len(query_rows)} validation queries to {queries_output}[/bold green]"
    )
    if list_queries:
        print_query_rows(query_rows, console)


if __name__ == "__main__":
    app()
