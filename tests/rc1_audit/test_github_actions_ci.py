"""RA-2: CI / Cloud Verification Parity — GitHub Actions workflow audit."""

import os
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "v40-rc1-audit.yml"


def _read_workflow():
    """Read the CI workflow file, skip if missing."""
    if not WORKFLOW_PATH.exists():
        return None
    return WORKFLOW_PATH.read_text()


def test_ci_workflow_exists():
    """Verify .github/workflows/v40-rc1-audit.yml exists."""
    assert WORKFLOW_PATH.exists(), (
        f"Workflow file not found at {WORKFLOW_PATH}"
    )


def test_ci_has_hardening_b():
    """Workflow must include verify_v40_hardening_b.sh."""
    content = _read_workflow()
    assert content is not None, "Workflow file missing"
    assert "verify_v40_hardening_b.sh" in content, (
        "Workflow does not reference verify_v40_hardening_b.sh"
    )


def test_ci_has_hardening_c2():
    """Workflow must include verify_v40_hardening_c2_all.sh."""
    content = _read_workflow()
    assert content is not None, "Workflow file missing"
    assert "verify_v40_hardening_c2_all.sh" in content, (
        "Workflow does not reference verify_v40_hardening_c2_all.sh"
    )


def test_ci_has_hardening_c3():
    """Workflow must include verify_v40_hardening_c3_all.sh."""
    content = _read_workflow()
    assert content is not None, "Workflow file missing"
    assert "verify_v40_hardening_c3_all.sh" in content, (
        "Workflow does not reference verify_v40_hardening_c3_all.sh"
    )


def test_ci_has_full_tests():
    """Workflow must include pytest -q tests/."""
    content = _read_workflow()
    assert content is not None, "Workflow file missing"
    assert "pytest -q tests/" in content or "pytest -q tests" in content, (
        "Workflow does not reference pytest -q tests/"
    )


def test_ci_uses_branch():
    """Workflow must target v4.0-batch-0-final-hardgates-scope-lock."""
    content = _read_workflow()
    assert content is not None, "Workflow file missing"
    assert "v4.0-batch-0-final-hardgates-scope-lock" in content, (
        "Workflow does not reference v4.0-batch-0-final-hardgates-scope-lock"
    )
