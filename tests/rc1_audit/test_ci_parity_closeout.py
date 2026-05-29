#!/usr/bin/env python3
"""CI0: CI Parity Closeout Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_ci_parity_closeout_exists():
    assert (WORKSPACE / "docs" / "rc1_audit" / "RC1_CI_PARITY_CLOSEOUT.md").exists()

def test_ci_parity_closeout_has_required_markers():
    text = (WORKSPACE / "docs" / "rc1_audit" / "RC1_CI_PARITY_CLOSEOUT.md").read_text(encoding="utf-8")
    for marker in ["CI parity status:", "Workflow: v40-rc1-audit.yml", "Run ID:", "Run URL:", "Head SHA:", "Conclusion:"]:
        assert marker in text, f"missing: {marker}"
    assert ("RC1 tag" in text) and ("FALSE" in text or "NOT CREATED" in text)

def test_ci_parity_reports_updated():
    audit = (WORKSPACE / "docs" / "rc1_audit" / "RC1_READINESS_AUDIT_REPORT.md").read_text(encoding="utf-8")
    score = (WORKSPACE / "docs" / "rc1_audit" / "RC1_READINESS_SCORECARD.md").read_text(encoding="utf-8")
    assert "GitHub Actions CI" in audit
    assert "CI Cloud Run" in score

def test_ci_parity_does_not_approve_rc1_or_production():
    combined = "\n".join([
        (WORKSPACE / "docs" / "rc1_audit" / "RC1_CI_PARITY_CLOSEOUT.md").read_text(encoding="utf-8"),
        (WORKSPACE / "docs" / "rc1_audit" / "RC1_READINESS_AUDIT_REPORT.md").read_text(encoding="utf-8"),
        (WORKSPACE / "docs" / "rc1_audit" / "RC1_READINESS_SCORECARD.md").read_text(encoding="utf-8"),
    ])
    for fb in ["RC1 tag created: TRUE", "Production: READY", "Broker/runtime: READY", "RC1 status: APPROVED"]:
        assert fb not in combined, f"Forbidden: {fb}"

def test_verify_script_exists():
    assert (WORKSPACE / "scripts" / "verify_rc1_ci_parity_closeout.sh").exists()

if __name__ == "__main__":
    test_ci_parity_closeout_exists()
    test_ci_parity_closeout_has_required_markers()
    test_ci_parity_reports_updated()
    test_ci_parity_does_not_approve_rc1_or_production()
    test_verify_script_exists()
    print("✅ CI0 CI Parity Closeout tests PASS")
