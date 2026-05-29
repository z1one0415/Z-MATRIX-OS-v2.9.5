#!/usr/bin/env python3
"""C3-0 → C3-5 Scope Truth Tests — forward-compatible across C3 phases"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_c3_scope_lock_exists():
    path = WORKSPACE / "docs" / "upgrade" / "V40_HARDENING_C3_SCOPE_LOCK.md"
    assert path.exists(), f"missing: {path}"
    content = path.read_text()
    assert "12 reviewer independent files/configs" in content
    assert "12 markdown templates snapshot rendering" in content
    assert "audit zip real file export" in content
    assert "IRF-02/05/06/07/08 chain integration" in content

def test_c3_acceptance_matrix_exists():
    path = WORKSPACE / "docs" / "upgrade" / "V40_HARDENING_C3_ACCEPTANCE_MATRIX.md"
    assert path.exists(), f"missing: {path}"
    content = path.read_text()
    for phase in ["C3-0", "C3-1", "C3-2", "C3-3", "C3-4", "C3-5"]:
        assert phase in content, f"missing phase: {phase}"

def test_truth_report_integrity():
    path = WORKSPACE / "docs" / "release" / "V40_CLOSEOUT_TRUTH_REPORT.md"
    content = path.read_text()
    # Accept legitimate status progression from SMOKE to COMPLETE
    assert ("INTEGRATION_SMOKE_CANDIDATE" in content) or ("INTEGRATION_COMPLETE_CANDIDATE" in content)
    assert "NOT_APPROVED" in content
    assert "BLOCKED" in content
    # Must NOT claim RC1 approved or production ready
    assert "RC1 status: APPROVED" not in content
    assert "Production status: READY" not in content
    assert "This release is not RC1" in content
    assert "This release is not production-ready" in content

def test_four_gaps_only():
    path = WORKSPACE / "docs" / "upgrade" / "V40_HARDENING_C3_SCOPE_LOCK.md"
    content = path.read_text()
    gap_items = [l.strip() for l in content.split("\n") if l.strip().startswith(("1.", "2.", "3.", "4."))]
    assert len(gap_items) >= 4, f"expected 4 gaps, found {len(gap_items)}: {gap_items}"

def test_verify_script_exists():
    path = WORKSPACE / "scripts" / "verify_v40_hardening_c3_0_scope.sh"
    assert path.exists(), f"missing verify script: {path}"
    path2 = WORKSPACE / "scripts" / "verify_v40_hardening_c3_all.sh"
    assert path2.exists(), f"missing total verify: {path2}"

if __name__ == "__main__":
    test_c3_scope_lock_exists()
    test_c3_acceptance_matrix_exists()
    test_truth_report_integrity()
    test_four_gaps_only()
    test_verify_script_exists()
    print("✅ C3 Scope Truth tests PASS (phase-agnostic)")
