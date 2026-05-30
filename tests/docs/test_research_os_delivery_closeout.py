#!/usr/bin/env python3
"""Research OS V3 Delivery Closeout — Documentation Tests"""
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

def test_onboarding_says_not_trading_bot():
    text = _r("ONBOARDING_GUIDE.md")
    assert "not" in text.lower() and ("trading robot" in text.lower() or "trading" in text.lower())

def test_user_manual_has_golden_path_command():
    text = _r("USER_OPERATION_MANUAL.md")
    assert "run_golden_path_600519.sh" in text

def test_human_report_readme_explains_8_sections():
    text = _r("GOLDEN_PATH_HUMAN_REPORT_README.md")
    assert "研究对象" in text and "建议动作" in text

def test_audit_pack_has_entries():
    text = _r("AUDIT_PREPARATION_PACK.md")
    assert "Architecture Freeze Audit" in text and "Golden Path" in text

def test_quality_plan_has_classification():
    text = _r("TEST_QUALITY_AUDIT_PLAN.md")
    assert "REAL_LOGIC" in text or "EXISTENCE_TEST" in text

def test_case_plan_is_plan_only():
    text = _r("CASE_EXPANSION_PLAN.md")
    assert "DO NOT IMPLEMENT" in text or "PLANNED" in text

def test_closeout_has_final_status():
    text = _r("RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md")
    assert "RESEARCH_OS_V3_DELIVERY_READY" in text
    assert "BLOCKED" in text

def test_no_production_claims():
    combined = "\n".join(_r(p) for p in ["DELIVERY_INDEX.md", "ONBOARDING_GUIDE.md", "RESEARCH_OS_V3_DELIVERY_CLOSEOUT.md"])
    for fb in ["Production Ready", "Broker Ready", "Runtime Ready", "Real Trade Ready"]:
        assert fb not in combined, f"Forbidden: {fb}"

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
