from __future__ import annotations

import subprocess
import sys


def test_prototype_script_help_lists_commands() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/prototype_extract_health_claims.py", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    output = result.stdout
    assert "extract-claims" in output
    assert "generate-queries" in output
    assert "run-pipeline" in output
