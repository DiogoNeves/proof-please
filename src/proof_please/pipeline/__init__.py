"""Public entrypoints for the prototype health-claims pipeline."""

from proof_please.pipeline.io import load_claims_jsonl, write_jsonl
from proof_please.pipeline.models import OllamaConfig
from proof_please.pipeline.pipeline_runner import (
    fetch_available_models,
    parse_model_list,
    run_claim_extraction,
    run_query_generation,
    validate_common_args,
    validate_path_exists,
    warn_missing_models,
)
from proof_please.pipeline.printing import print_claim_rows, print_query_rows

__all__ = [
    "OllamaConfig",
    "fetch_available_models",
    "load_claims_jsonl",
    "parse_model_list",
    "print_claim_rows",
    "print_query_rows",
    "run_claim_extraction",
    "run_query_generation",
    "validate_common_args",
    "validate_path_exists",
    "warn_missing_models",
    "write_jsonl",
]
