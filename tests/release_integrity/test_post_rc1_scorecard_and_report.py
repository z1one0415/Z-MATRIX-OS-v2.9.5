#!/usr/bin/env python3
"""PRI: Release Docs Consistency + Scorecard + Report Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_docs_consistency_script_exists():
    assert (WORKSPACE / "scripts" / "verify_post_rc1_release_docs_consistency.py").exists()
    assert (WORKSPACE / "scripts" / "verify_post_rc1_release_docs_consistency.sh").exists()

def test_scorecard_exists_and_has_decision():
    text = (WORKSPACE / "docs" / "release_integrity" / "POST_RC1_INTEGRITY_SCORECARD.md").read_text()
    assert "POST_RC1_INTEGRITY_PASS" in text
    assert "100/100" in text

def test_audit_report_exists_and_no_production_claims():
    text = (WORKSPACE / "docs" / "release_integrity" / "POST_RC1_RELEASE_INTEGRITY_AUDIT_REPORT.md").read_text()
    assert "BLOCKED" in text
    for forbidden in ["Production: READY", "Broker/runtime: READY", "Real trade: READY"]:
        assert forbidden not in text

def test_remote_state_exists():
    assert (WORKSPACE / "docs" / "release_integrity" / "POST_RC1_REMOTE_RELEASE_STATE.md").exists()
    text = (WORKSPACE / "docs" / "release_integrity" / "POST_RC1_REMOTE_RELEASE_STATE.md").read_text()
    assert "GitHub Release object published" in text
    assert "FALSE" in text
    assert "BLOCKED" in text or "FALSE" in text

def test_full_verify_script_exists():
    assert (WORKSPACE / "scripts" / "verify_post_rc1_release_integrity_all.sh").exists()

if __name__ == "__main__":
    test_docs_consistency_script_exists()
    test_scorecard_exists_and_has_decision()
    test_audit_report_exists_and_no_production_claims()
    test_remote_state_exists()
    test_full_verify_script_exists()
    print("✅ PRI Release Integrity tests PASS")
