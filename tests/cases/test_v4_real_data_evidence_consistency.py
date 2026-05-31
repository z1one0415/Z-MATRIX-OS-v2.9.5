"""Test V4.3 evidence consistency."""
import json
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent

@pytest.fixture
def rd():
    return json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json").read_text())

@pytest.fixture
def rr():
    return json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_real_return_readiness.json").read_text())

@pytest.fixture
def gate():
    return json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())

def test_gate_matches_readiness(rd, gate):
    assert gate["daily_price_real_read_only"] == rd["summary"]["daily_price_real"]
    assert gate["adjustment_factor_ready"] == rd["summary"]["adjustment_ready"]
    assert gate["benchmark_real_read_only"] == rd["summary"]["benchmark_local"]
    assert gate["calendar_real_read_only"] == rd["summary"]["calendar_local"]

def test_gate_matches_return(rr, gate):
    assert gate["ready_for_real_return"] == rr["summary"]["ready_for_real_return"]

def test_no_adj_missing_when_return_ready(rr):
    for r in rr["cases"]:
        if r["ready_for_real_return"]:
            assert r["adjustment_factor_status"] != "MISSING", r["case_id"]

def test_trading_days_not_null(rd):
    for r in rd["cases"]:
        if r["daily_price_status"] == "LOCAL_USER_PROVIDED":
            assert r["trading_days"] is not None and r["trading_days"] > 0

def test_start_end_not_null(rd):
    for r in rd["cases"]:
        if r["daily_price_status"] == "LOCAL_USER_PROVIDED":
            assert r["daily_price_start"] is not None
            assert r["daily_price_end"] is not None

def test_safety_blocked(rd, rr, gate):
    assert gate["production"] == "BLOCKED"
    assert gate["broker_runtime"] == "BLOCKED"
    assert gate["real_trade"] == "BLOCKED"

def test_adj_equals_non_missing(rd, rr):
    count = sum(1 for r in rr["cases"] if r["adjustment_factor_status"] != "MISSING")
    assert rd["summary"]["adjustment_ready"] == count
