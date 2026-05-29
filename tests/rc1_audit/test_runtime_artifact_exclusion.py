#!/usr/bin/env python3
"""RA-5: Runtime Artifact Exclusion Audit Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent


def test_exclusion_script_exists():
    """Verify the RA-5 exclusion audit script exists and is executable."""
    p = WORKSPACE / "scripts" / "verify_rc1_artifact_exclusion.sh"
    assert p.exists(), f"Script not found: {p}"
    assert os.access(p, os.X_OK), f"Script not executable: {p}"


def test_artifact_zip_works():
    """Run the audit script and verify it generates a test audit ZIP."""
    p = WORKSPACE / "scripts" / "verify_rc1_artifact_exclusion.sh"
    result = subprocess.run(
        ["bash", str(p)],
        capture_output=True,
        text=True,
        cwd=str(WORKSPACE),
    )
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"
    assert "runtime artifact exclusion PASS" in result.stdout

    # Verify the generated ZIP exists
    zip_path = WORKSPACE / "runtime_reports" / "rc1_artifact_test" / "test_audit.zip"
    assert zip_path.exists(), f"Test audit ZIP not generated: {zip_path}"
    assert zip_path.stat().st_size > 0, "Test audit ZIP is empty"


def test_runtime_not_tracked():
    """Verify git status does not show runtime_reports or .zip artifacts."""
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True,
        cwd=str(WORKSPACE),
    )
    assert result.returncode == 0

    tracked_lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
    violations = [
        line for line in tracked_lines
        if "runtime_reports" in line or (".zip" in line and "runtime_reports" not in line)
    ]

    # runtime_reports/*.zip should be gitignored; only our new files may show
    # Filter out the expected untracked: scripts/ and tests/rc1_audit/ (our new files)
    real_violations = [
        v for v in violations
        if "scripts/verify_rc1_artifact_exclusion.sh" not in v
        and "tests/rc1_audit/test_runtime_artifact_exclusion.py" not in v
        and "__pycache__" not in v
    ]

    assert len(real_violations) == 0, (
        f"Runtime artifacts found in git status:\n" + "\n".join(real_violations)
    )


if __name__ == "__main__":
    test_exclusion_script_exists()
    test_artifact_zip_works()
    test_runtime_not_tracked()
    print("✅ RA-5 Runtime Artifact Exclusion tests PASS")
