"""Prototype script to extract health claims from a transcript.

This script is intentionally a scaffold only for now.
"""

from pathlib import Path

import typer
from rich.console import Console

console = Console()


def main(transcript: Path) -> None:
    """Entry point for prototype health-claim extraction."""
    if not transcript.exists():
        raise typer.BadParameter(f"Transcript path does not exist: {transcript}")

    console.print(
        "[yellow]Prototype health-claim extractor not implemented yet.[/yellow]\n"
        f"Transcript selected: {transcript}"
    )


if __name__ == "__main__":
    typer.run(main)
