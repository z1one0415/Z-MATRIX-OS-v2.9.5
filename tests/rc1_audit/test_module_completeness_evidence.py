"""RC1 Module Completeness Evidence – self-audit tests.

Tests that the evidence generator script runs cleanly and that every
module passes its readiness gate (no BLOCKED statuses).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
SCRIPTS = WORKSPACE / "scripts"
DOCS = WORKSPACE / "docs" / "rc1_audit"
GENERATOR = SCRIPTS / "generate_rc1_module_evidence.py"
EVIDENCE_JSON = DOCS / "RC1_MODULE_EVIDENCE.json"
EVIDENCE_MD = DOCS / "RC1_MODULE_COMPLETENESS_EVIDENCE.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _run_generator() -> subprocess.CompletedProcess:
    """Run the evidence generator and return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(GENERATOR)],
        cwd=str(WORKSPACE),
        capture_output=True,
        text=True,
        env={**__import__("os").environ, "PYTHONPATH": str(WORKSPACE)},
    )


def _load_evidence() -> list[dict]:
    """Load RC1_MODULE_EVIDENCE.json and return the module list."""
    return json.loads(EVIDENCE_JSON.read_text())


def _get_module(modules: list[dict], name: str) -> dict:
    for m in modules:
        if m["module_name"] == name:
            return m
    raise KeyError(f"Module {name!r} not found in evidence")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
@pytest.mark.rc1_audit
@pytest.mark.module_evidence
class TestGeneratorScript:
    def test_generator_script_exists(self):
        """The generator script must be present."""
        assert GENERATOR.exists(), f"Missing {GENERATOR}"

    def test_module_evidence_json_generated(self):
        """Running the generator must produce RC1_MODULE_EVIDENCE.json."""
        result = _run_generator()
        assert result.returncode == 0, (
            f"Generator failed:\n{result.stderr}"
        )
        assert EVIDENCE_JSON.exists(), f"Missing {EVIDENCE_JSON}"

    def test_module_evidence_md_generated(self):
        """Running the generator must produce RC1_MODULE_COMPLETENESS_EVIDENCE.md."""
        result = _run_generator()
        assert result.returncode == 0, (
            f"Generator failed:\n{result.stderr}"
        )
        assert EVIDENCE_MD.exists(), f"Missing {EVIDENCE_MD}"


@pytest.mark.rc1_audit
@pytest.mark.module_evidence
class TestModuleStatuses:
    def test_no_blocked_modules(self):
        """No module may have BLOCKED status for RC1."""
        _run_generator()
        modules = _load_evidence()
        blocked = [m["module_name"] for m in modules if m["status"] == "BLOCKED"]
        assert not blocked, (
            f"BLOCKED modules detected: {blocked}"
        )

    def test_irf_chains_pass(self):
        """IRF-01~08 must be PASS."""
        _run_generator()
        m = _get_module(_load_evidence(), "IRF-01~08")
        assert m["status"] == "PASS", (
            f"IRF-01~08 status={m['status']}, expected PASS"
        )

    def test_safety_gates_pass(self):
        """Safety Gates must be PASS."""
        _run_generator()
        m = _get_module(_load_evidence(), "Safety Gates")
        assert m["status"] == "PASS", (
            f"Safety Gates status={m['status']}, expected PASS"
        )

    def test_research_council_pass(self):
        """Research Council must be PASS."""
        _run_generator()
        m = _get_module(_load_evidence(), "Research Council")
        assert m["status"] == "PASS", (
            f"Research Council status={m['status']}, expected PASS"
        )
