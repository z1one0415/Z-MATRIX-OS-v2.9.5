#!/usr/bin/env python3
"""Phase 1-A0: Private Data Guardrail Tests"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent


def test_gitignore_contains_raw_protection():
    gi = (WORKSPACE / ".gitignore").read_text()
    assert "data/research_db/account/raw/" in gi
    assert "data/research_db/account/staging/" in gi


def test_gitignore_contains_file_type_protection():
    gi = (WORKSPACE / ".gitignore").read_text()
    for ext in ["*.xlsx", "*.xls", "*.csv.raw"]:
        assert ext in gi, f"missing {ext}"


def test_gitignore_allows_keep_files():
    gi = (WORKSPACE / ".gitignore").read_text()
    assert "!data/research_db/account/raw/.gitkeep" in gi
    assert "!data/research_db/account/staging/.gitkeep" in gi


def test_no_raw_files_tracked_by_git():
    r = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=str(WORKSPACE))
    lines = r.stdout.split("\n")
    for bad in [".xlsx", ".xls", ".csv.raw"]:
        tracked = [l for l in lines if l.endswith(bad)]
        assert len(tracked) == 0, f"tracked {bad}: {tracked}"


def test_no_raw_account_data_tracked():
    r = subprocess.run(["git", "ls-files", "data/research_db/account/raw/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    tracked = [l for l in r.stdout.split("\n") if l.strip() and not l.endswith(".gitkeep")]
    assert len(tracked) == 0, f"tracked raw data: {tracked}"


def test_gitkeep_files_exist():
    for f in ["data/research_db/account/raw/.gitkeep", "data/research_db/account/staging/.gitkeep"]:
        assert (WORKSPACE / f).exists(), f"missing {f}"


if __name__ == "__main__":
    test_gitignore_contains_raw_protection()
    test_gitignore_contains_file_type_protection()
    test_gitignore_allows_keep_files()
    test_no_raw_files_tracked_by_git()
    test_no_raw_account_data_tracked()
    test_gitkeep_files_exist()
    print("✅ Phase 1-A0 Private Data Guardrail tests PASS")
