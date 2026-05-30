#!/usr/bin/env python3
"""Phase 2-E: CI Workflow Test"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

def test_ci_workflow_exists():
    assert (WORKSPACE / ".github" / "workflows" / "researchdb-phase2.yml").exists()

def test_ci_has_phase1_1():
    c = (WORKSPACE / ".github" / "workflows" / "researchdb-phase2.yml").read_text()
    assert "verify_research_db_phase1_1_cloud_acceptance.sh" in c

def test_ci_has_phase2_verify():
    c = (WORKSPACE / ".github" / "workflows" / "researchdb-phase2.yml").read_text()
    assert "verify_research_db_phase2_master_data.sh" in c

def test_ci_has_pytest():
    c = (WORKSPACE / ".github" / "workflows" / "researchdb-phase2.yml").read_text()
    assert "tests/research_db/master_data/" in c

def test_ci_no_production_enable():
    c = (WORKSPACE / ".github" / "workflows" / "researchdb-phase2.yml").read_text()
    for fb in ["production_allowed=True", "broker_order_allowed=True", "runtime_enabled=True"]:
        assert fb not in c

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
