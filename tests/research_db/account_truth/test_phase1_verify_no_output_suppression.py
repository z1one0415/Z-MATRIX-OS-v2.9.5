#!/usr/bin/env python3
"""Phase 1.1: Verify Output Suppression Test"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent


def test_verify_script_no_dev_null():
    content = (WORKSPACE / "scripts" / "verify_research_db_phase1_account_truth.sh").read_text()
    assert "> /dev/null" not in content, "verify script must not suppress output to /dev/null"


def test_verify_script_no_tail():
    content = (WORKSPACE / "scripts" / "verify_research_db_phase1_account_truth.sh").read_text()
    # Allow tail as a tool command but not as output suppression
    for line in content.split("\n"):
        if "| tail" in line and not line.strip().startswith("#"):
            raise AssertionError(f"verify script must not pipe to tail: {line.strip()[:60]}")


def test_verify_script_runs_phase0_direct():
    content = (WORKSPACE / "scripts" / "verify_research_db_phase1_account_truth.sh").read_text()
    assert "verify_research_db_phase0.sh" in content


def test_verify_script_runs_pytest_direct():
    content = (WORKSPACE / "scripts" / "verify_research_db_phase1_account_truth.sh").read_text()
    assert "pytest" in content and "account_truth" in content


if __name__ == "__main__":
    test_verify_script_no_dev_null()
    test_verify_script_no_tail()
    test_verify_script_runs_phase0_direct()
    test_verify_script_runs_pytest_direct()
    print("✅ Phase 1.1 Output Suppression Fix tests PASS")
