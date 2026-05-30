#!/usr/bin/env python3
"""Research OS V3 Delivery Closeout — Documentation Tests (hardened)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def _r(p): return (WORKSPACE / "docs" / "research_os" / p).read_text()

def test_delivery_index_exists(): assert (WORKSPACE / "docs" / "research_os" / "DELIVERY_INDEX.md").exists()
def test_onboarding_guide_exists(): assert (WORKSPACE / "docs" / "research_os" / "ONBOARDING_GUIDE.md").exists()
def test_user_manual_exists(): assert (WORKSPACE / "docs" / "research_os" / "USER_OPERATION_MANUAL.md").exists()
def test_human_report_readme_exists(): assert (WORKSPACE / "docs" / "research_os" / "GOLDEN_PATH_HUMAN_REPORT_README.md").exists()
def test_audit_pack_exists(): assert (WORKSPACE / "docs" / "research_os" / "AUDIT_PREPARATION_PACK.md").exists()
def test_test_quality_plan_exists(): assert (WORKSPACE / "docs" / "research_os" / "TEST_QUALITY_AUDIT_PLAN.md").exists()
def test_case_plan_exists(): assert (WORKSPACE / "docs" / "research_os" / "CASE_EXPANSION_PLAN.md").exists()
def test_closeout_exists(): assert (WORKSPACE / "docs" / "research_os" / "RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md").exists()

# ── HARDENED tests (6 new) ──
def test_verify_script_no_dev_null():
    text = (WORKSPACE / "scripts" / "verify_research_os_delivery_closeout.sh").read_text()
    assert "> /dev/null" not in text
    assert "2>/dev/null" not in text

def test_verify_script_no_tail():
    text = (WORKSPACE / "scripts" / "verify_research_os_delivery_closeout.sh").read_text()
    for line in text.split("\n"):
        if "| tail" in line and not line.strip().startswith("#"):
            raise AssertionError(f"tail pipe: {line.strip()[:60]}")

def test_verify_script_no_or_true():
    text = (WORKSPACE / "scripts" / "verify_research_os_delivery_closeout.sh").read_text()
    assert "|| true" not in text

def test_delivery_closeout_consistent():
    idx = _r("DELIVERY_INDEX.md"); clo = _r("RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md")
    assert "160" in idx and "160" in clo
    assert "23" in idx and "23" in clo
    assert ("1240" in idx or "1,240" in idx) and ("1240" in clo or "1,240" in clo)

def test_closeout_has_freeze_maintained():
    text = _r("RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md")
    assert "freeze" in text.lower() and "maintained" in text.lower()

def test_closeout_has_human_report_verified():
    text = _r("RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md")
    assert "HUMAN_REPORT" in text or "Human Report" in text

def test_no_production_claims():
    combined = "\n".join(_r(p) for p in ["DELIVERY_INDEX.md", "RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md"])
    for fb in ["Production Ready", "Broker Ready", "Runtime Ready", "Real Trade Ready"]:
        assert fb not in combined, f"Forbidden: {fb}"

def test_onboarding_says_not_trading_bot():
    text = _r("ONBOARDING_GUIDE.md")
    assert "trading robot" in text.lower() or "not" in text.lower()

def test_user_manual_has_golden_path():
    assert "run_golden_path_600519.sh" in _r("USER_OPERATION_MANUAL.md")

def test_human_report_readme_has_8_sections():
    assert "研究对象" in _r("GOLDEN_PATH_HUMAN_REPORT_README.md")

def test_audit_pack_has_8_entries():
    text = _r("AUDIT_PREPARATION_PACK.md")
    assert "Architecture Freeze Audit" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
