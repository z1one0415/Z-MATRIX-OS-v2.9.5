"""Test Golden Path parameterization — ticker-specific results."""
from pathlib import Path
import json
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys_path = str(WORKSPACE)


def test_golden_path_ticker_different():
    """CORE_001 and CORE_002 produce different hashes (different tickers)."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r1 = run_golden_path(ticker="600519", case_id="CORE_001", name="贵州茅台", industry="食品饮料", dry_run=True)
    r2 = run_golden_path(ticker="300750", case_id="CORE_002", name="宁德时代", industry="电力设备", dry_run=True)
    assert r1["_audit_hash"] != r2["_audit_hash"], f"Same hash: {r1['_audit_hash']}"


def test_golden_path_case_metadata():
    """_case metadata contains ticker, case_id, name, industry."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker="300750", case_id="CORE_002", name="宁德时代", industry="电力设备", dry_run=True)
    c = r["_case"]
    assert c["ticker"] == "300750"
    assert c["case_id"] == "CORE_002"
    assert c["name"] == "宁德时代"
    assert c["industry"] == "电力设备"


def test_idea_ticker_from_case():
    """idea.ticker matches the passed ticker."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker="300750", case_id="CORE_002", dry_run=True)
    assert r["idea"]["ticker"] == "300750"


def test_no_buy_sell_in_result():
    """Decision must be PASS (research-only), no BUY/SELL instructions."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker="600519", case_id="CORE_001", dry_run=True)
    decision = r.get("council", {})
    ledger = r.get("decision", {})
    assert decision.get("status") == "PASS", f"council.status={decision.get('status')}"
    # Ledger tracks BUY count=0, but no active BUY instructions
    assert ledger.get("buy", 0) == 0 and ledger.get("sell", 0) == 0


def test_human_report_uses_case_name():
    """CORE_002 human report contains 宁德时代, not 贵州茅台."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker="300750", case_id="CORE_002", name="宁德时代", industry="电力设备",
                        sector="新能源", chain="电池", dry_run=True)
    text = Path(r["human_report"]).read_text()
    assert "宁德时代" in text
    assert "300750" in text
    assert "电力设备" in text
    assert "贵州茅台" not in text


def test_human_report_path_contains_case_ticker():
    """Human report path contains CORE_002_300750."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker="300750", case_id="CORE_002", name="宁德时代", dry_run=True)
    assert "CORE_002_300750" in r["human_report"]


def test_runner_accepts_all_params():
    """Runner accepts 14 parameters."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker="600519", case_id="CORE_001", name="贵州茅台", exchange="SSE",
                        category="白马蓝筹", industry="食品饮料", sector="消费", chain="白酒",
                        style="quality", risk="low", benchmark_id="CSI300",
                        start_date="2024-01-02", end_date="2024-06-28", dry_run=True)
    assert r["_case"]["exchange"] == "SSE"
    assert r["_case"]["category"] == "白马蓝筹"
