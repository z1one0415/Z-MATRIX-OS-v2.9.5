#!/usr/bin/env python3
"""Phase 2-E: Verify Script Test"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

def test_verify_script_exists():
    assert (WORKSPACE / "scripts" / "verify_research_db_phase2_master_data.sh").exists()

def test_verify_script_calls_phase1_1():
    c = (WORKSPACE / "scripts" / "verify_research_db_phase2_master_data.sh").read_text()
    assert "verify_research_db_phase1_1_cloud_acceptance.sh" in c

def test_verify_script_calls_pytest():
    c = (WORKSPACE / "scripts" / "verify_research_db_phase2_master_data.sh").read_text()
    assert "tests/research_db/master_data/" in c
    assert "pytest" in c

def test_verify_script_has_safety_scan():
    c = (WORKSPACE / "scripts" / "verify_research_db_phase2_master_data.sh").read_text()
    assert "raw/" in c or "staging/" in c
    assert "vendor" in c.lower()

def test_verify_script_no_dev_null():
    c = (WORKSPACE / "scripts" / "verify_research_db_phase2_master_data.sh").read_text()
    assert "> /dev/null" not in c

def test_verify_script_no_tail_pipe():
    c = (WORKSPACE / "scripts" / "verify_research_db_phase2_master_data.sh").read_text()
    for line in c.split("\n"):
        if "| tail" in line and not line.strip().startswith("#"):
            raise AssertionError(f"pipe to tail: {line.strip()[:60]}")

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
