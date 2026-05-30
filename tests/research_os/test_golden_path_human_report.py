#!/usr/bin/env python3
"""ROC-HR1: Human Report Adapter Tests — 10+ tests covering all sections"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

from zmatrix.research_os.golden_path_human_report import generate_human_report, save_human_report
from zmatrix.research_os.golden_path_runner import run_golden_path

GP_RESULT = run_golden_path(dry_run=True)
REPORT = generate_human_report(GP_RESULT)

def test_human_report_generated():
    assert len(REPORT) > 500, f"Report too short: {len(REPORT)} chars"

def test_contains_summary():
    assert "研究对象" in REPORT
    assert "600519" in REPORT

def test_contains_reason():
    assert "为什么这样判断" in REPORT
    assert "因子" in REPORT

def test_contains_attribution():
    assert "收益来源分析" in REPORT
    assert "市场贡献" in REPORT or "选股" in REPORT

def test_contains_risks():
    assert "主要风险" in REPORT

def test_contains_contradiction():
    assert "反方意见" in REPORT
    assert "Devil" in REPORT or "反方" in REPORT

def test_contains_recommendation():
    assert "建议动作" in REPORT

def test_contains_hash():
    assert "审计" in REPORT or "Audit" in REPORT
    assert GP_RESULT["_audit_hash"] in REPORT

def test_no_trade_instruction():
    for forbidden in ["买入", "卖出", "立即建仓", "立即清仓", "BUY", "SELL", "AUTO_EXECUTE"]:
        assert forbidden not in REPORT, f"Forbidden word in report: {forbidden}"

def test_architecture_freeze_maintained():
    """Module count must remain 160"""
    modules = list((WORKSPACE / "zmatrix" / "research_db").rglob("*.py"))
    actual = [m for m in modules if m.name != "__init__.py" and "__pycache__" not in str(m)]
    assert len(actual) == 160, f"Module count changed: {len(actual)} (freezed at 160)"

def test_save_human_report():
    path = save_human_report(GP_RESULT)
    assert Path(path).exists()
    content = Path(path).read_text()
    assert len(content) > 500

def test_production_blocked():
    assert "BLOCKED" in REPORT
    assert "production" in REPORT.lower() or "Production" in REPORT

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
