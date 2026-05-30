#!/usr/bin/env python3
"""Phase 1.1: CI Workflow Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent


def test_ci_workflow_exists():
    assert (WORKSPACE / ".github" / "workflows" / "researchdb-phase1.yml").exists()


def test_ci_has_phase0():
    content = (WORKSPACE / ".github" / "workflows" / "researchdb-phase1.yml").read_text()
    assert "verify_research_db_phase0.sh" in content


def test_ci_has_guardrail():
    content = (WORKSPACE / ".github" / "workflows" / "researchdb-phase1.yml").read_text()
    assert "verify_research_db_private_data_guardrail.sh" in content


def test_ci_has_phase1():
    content = (WORKSPACE / ".github" / "workflows" / "researchdb-phase1.yml").read_text()
    assert "verify_research_db_phase1_account_truth.sh" in content


def test_ci_has_pytest():
    content = (WORKSPACE / ".github" / "workflows" / "researchdb-phase1.yml").read_text()
    assert "account_truth" in content


if __name__ == "__main__":
    test_ci_workflow_exists()
    test_ci_has_phase0()
    test_ci_has_guardrail()
    test_ci_has_phase1()
    test_ci_has_pytest()
    print("✅ Phase 1.1 CI Workflow tests PASS")
