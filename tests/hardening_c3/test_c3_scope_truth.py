#!/usr/bin/env python3
"""C3-0 Scope Truth Tests — verify scope lock and acceptance matrix integrity"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def _forbidden_in_allowed_context(text, forbidden_tokens):
    """Check that forbidden tokens only appear in explicitly forbidden (❌) lines"""
    lines = text.split("\n")
    for line in lines:
        stripped = line.strip()
        for token in forbidden_tokens:
            if token in stripped and not stripped.startswith("❌") and not stripped.startswith("- ❌"):
                return True, token, stripped[:80]
    return False, None, ""

def test_c3_scope_lock_exists():
    path = WORKSPACE / "docs" / "upgrade" / "V40_HARDENING_C3_SCOPE_LOCK.md"
    assert path.exists(), f"missing: {path}"
    content = path.read_text()
    assert "12 reviewer independent files/configs" in content
    assert "12 markdown templates snapshot rendering" in content
    assert "audit zip real file export" in content
    assert "IRF-02/05/06/07/08 chain integration" in content
    # Forbidden tokens must appear only in explicitly forbidden (❌) contexts
    triggered, token, ctx = _forbidden_in_allowed_context(content,
        ["RC1_APPROVED", "PRODUCTION_READY", "BROKER_READY", "ACCEPTANCE_DONE"])
    assert not triggered, f"forbidden token {token} in non-forbidden context: {ctx}"

def test_c3_acceptance_matrix_exists():
    path = WORKSPACE / "docs" / "upgrade" / "V40_HARDENING_C3_ACCEPTANCE_MATRIX.md"
    assert path.exists(), f"missing: {path}"
    content = path.read_text()
    for phase in ["C3-0", "C3-1", "C3-2", "C3-3", "C3-4", "C3-5"]:
        assert phase in content, f"missing phase: {phase}"
    assert "NOT_STARTED" in content
    triggered, token, ctx = _forbidden_in_allowed_context(content,
        ["ACCEPTANCE_DONE", "RC1_APPROVED", "PRODUCTION_READY"])
    assert not triggered, f"forbidden token {token} in non-forbidden context: {ctx}"

def test_truth_report_still_smoke():
    path = WORKSPACE / "docs" / "release" / "V40_CLOSEOUT_TRUTH_REPORT.md"
    content = path.read_text()
    assert "INTEGRATION_SMOKE_CANDIDATE" in content
    assert "NOT_APPROVED" in content
    assert "BLOCKED" in content
    triggered, token, ctx = _forbidden_in_allowed_context(content,
        ["INTEGRATION_COMPLETE_CANDIDATE", "RC1_APPROVED", "PRODUCTION_READY", "ACCEPTANCE_DONE"])
    assert not triggered, f"forbidden token {token} in truth report: {ctx}"

def test_four_gaps_only():
    path = WORKSPACE / "docs" / "upgrade" / "V40_HARDENING_C3_SCOPE_LOCK.md"
    content = path.read_text()
    gap_items = [l.strip() for l in content.split("\n") if l.strip().startswith(("1.", "2.", "3.", "4."))]
    assert len(gap_items) >= 4, f"expected 4 gaps, found {len(gap_items)}: {gap_items}"

def test_verify_script_exists():
    path = WORKSPACE / "scripts" / "verify_v40_hardening_c3_0_scope.sh"
    assert path.exists(), f"missing verify script: {path}"

if __name__ == "__main__":
    test_c3_scope_lock_exists()
    test_c3_acceptance_matrix_exists()
    test_truth_report_still_smoke()
    test_four_gaps_only()
    test_verify_script_exists()
    print("✅ C3-0 Scope Truth tests PASS")
