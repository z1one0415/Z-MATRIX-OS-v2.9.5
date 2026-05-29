#!/usr/bin/env python3
"""RA-3: Repository Hygiene Audit Tests"""
import sys, os, subprocess
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

WORKSPACE = Path(__file__).resolve().parent.parent.parent


def test_hygiene_script_exists():
    p = WORKSPACE / "scripts" / "verify_rc1_repo_hygiene.sh"
    assert p.exists(), "missing verify_rc1_repo_hygiene.sh"


def test_gitignore_exists():
    p = WORKSPACE / ".gitignore"
    assert p.exists(), ".gitignore missing"


def test_gitignore_covers_runtime():
    content = (WORKSPACE / ".gitignore").read_text()
    assert "runtime_reports" in content, ".gitignore missing runtime_reports"


def test_gitignore_covers_pycache():
    content = (WORKSPACE / ".gitignore").read_text()
    assert ".pytest_cache" in content, ".gitignore missing .pytest_cache"


def test_gitignore_covers_pyc():
    content = (WORKSPACE / ".gitignore").read_text()
    assert "__pycache__" in content, ".gitignore missing __pycache__"


def test_hygiene_script_runs():
    script = str(WORKSPACE / "scripts" / "verify_rc1_repo_hygiene.sh")
    result = subprocess.run(["bash", script], capture_output=True, text=True, timeout=30, cwd=str(WORKSPACE))
    assert result.returncode == 0, f"script failed:\n{result.stderr}"
    assert "repository hygiene PASS" in result.stdout


if __name__ == "__main__":
    test_hygiene_script_exists()
    test_gitignore_exists()
    test_gitignore_covers_runtime()
    test_gitignore_covers_pycache()
    test_gitignore_covers_pyc()
    test_hygiene_script_runs()
    print("✅ RA-3 Repo Hygiene tests PASS")
