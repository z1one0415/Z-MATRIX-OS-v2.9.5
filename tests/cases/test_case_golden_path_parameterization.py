"""Test Golden Path parameterization — ticker-specific results."""
from pathlib import Path
import json
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
REGISTRY = json.loads((WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())
sys_path = str(WORKSPACE)

def _case(cid):
    for c in REGISTRY:
        if c["case_id"] == cid: return c
    return {}

c001 = _case("CORE_001")
c002 = _case("CORE_002")


def test_golden_path_ticker_different():
    """CORE_001 and CORE_002 produce different hashes (different tickers)."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r1 = run_golden_path(ticker=c001["ticker"], case_id="CORE_001", name=c001["name"],
                         industry=c001["industry"], sector=c001["sector"], chain=c001["chain"],
                         dry_run=True)
    r2 = run_golden_path(ticker=c002["ticker"], case_id="CORE_002", name=c002["name"],
                         industry=c002["industry"], sector=c002["sector"], chain=c002["chain"],
                         dry_run=True)
    assert r1["_audit_hash"] != r2["_audit_hash"]


def test_golden_path_case_metadata():
    """_case metadata contains ticker, case_id, name, industry."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker=c002["ticker"], case_id="CORE_002", name=c002["name"],
                        industry=c002["industry"], sector=c002["sector"], chain=c002["chain"],
                        dry_run=True)
    c = r["_case"]
    assert c["ticker"] == c002["ticker"]
    assert c["case_id"] == "CORE_002"
    assert c["name"] == c002["name"]
    assert c["industry"] == c002["industry"]


def test_idea_ticker_from_case():
    """idea.ticker matches the passed ticker."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker=c002["ticker"], case_id="CORE_002", name=c002["name"],
                        industry=c002["industry"], sector=c002["sector"], chain=c002["chain"],
                        dry_run=True)
    assert r["idea"]["ticker"] == c002["ticker"]


def test_no_buy_sell_in_result():
    """Decision must be PASS (research-only), no active BUY/SELL."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker=c001["ticker"], case_id="CORE_001", name=c001["name"],
                        industry=c001["industry"], sector=c001["sector"], chain=c001["chain"],
                        dry_run=True)
    decision = r.get("council", {})
    ledger = r.get("decision", {})
    assert decision.get("status") == "PASS"
    assert ledger.get("buy", 0) == 0 and ledger.get("sell", 0) == 0


def test_human_report_uses_case_name():
    """CORE_002 human report contains 宁德时代, not 贵州茅台."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker=c002["ticker"], case_id="CORE_002", name=c002["name"],
                        industry=c002["industry"], sector=c002["sector"], chain=c002["chain"],
                        dry_run=True)
    text = Path(r["human_report"]).read_text()
    assert "宁德时代" in text
    assert "300750" in text
    assert "电力设备" in text
    assert "贵州茅台" not in text


def test_human_report_path_contains_case_ticker():
    """Human report path contains CORE_002_300750."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker=c002["ticker"], case_id="CORE_002", name=c002["name"],
                        industry=c002["industry"], sector=c002["sector"], chain=c002["chain"],
                        dry_run=True)
    assert "CORE_002_300750" in r["human_report"]


def test_runner_accepts_all_params():
    """Runner accepts 14 parameters."""
    import sys; sys.path.insert(0, sys_path)
    from zmatrix.research_os.golden_path_runner import run_golden_path
    r = run_golden_path(ticker=c001["ticker"], case_id="CORE_001", name=c001["name"],
                        exchange=c001["exchange"], category=c001["category"],
                        industry=c001["industry"], sector=c001["sector"], chain=c001["chain"],
                        style=c001["style"], risk=c001["risk"], benchmark_id="CSI300",
                        start_date="2024-01-02", end_date="2024-06-28", dry_run=True)
    assert r["_case"]["exchange"] == c001["exchange"]
    assert r["_case"]["category"] == c001["category"]
