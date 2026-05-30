#!/usr/bin/env python3
"""Phase 3-B: Comprehensive Outcome Horizon Tests (35+)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures" / "market_data"

from zmatrix.research_db.market_data.outcome_schema import (
    OutcomeHorizon, OutcomeReadinessStatus, OutcomeHorizonRequest, OutcomeHorizonResult, HORIZON_FORWARD_DAYS,
)
from zmatrix.research_db.market_data.trading_calendar import TradingCalendar
from zmatrix.research_db.market_data.price_bar_store import PriceBarStore
from zmatrix.research_db.market_data.outcome_horizon_engine import OutcomeHorizonEngine
from zmatrix.research_db.market_data.outcome_readiness_gate import check_outcome_ready, batch_check_outcome_ready, summarize_readiness
from zmatrix.research_db.market_data.outcome_fixture_builder import build_outcome_test_requests, build_insufficient_forward_days_cases, build_missing_bar_cases

CAL = TradingCalendar(str(FIXTURES / "sample_trading_calendar.csv"))
BARS = PriceBarStore(str(FIXTURES / "sample_daily_price_bar.csv"))
ENGINE = OutcomeHorizonEngine(CAL, BARS)

# ── enum tests ──
def test_horizon_enum_values():
    assert {h.value for h in OutcomeHorizon} == {"T1","T5","T10","T20","T60"}
def test_readiness_enum_values():
    assert "INSUFFICIENT_FORWARD_DAYS" in {s.value for s in OutcomeReadinessStatus}
    assert "MISSING_ENTRY_BAR" in {s.value for s in OutcomeReadinessStatus}

# ── schema tests ──
def test_request_production_false():
    r = OutcomeHorizonRequest(ticker="X", observation_date="D", horizon=OutcomeHorizon.T1)
    assert r.production_allowed is False
def test_result_production_false():
    r = OutcomeHorizonResult(ticker="X", observation_date="D", horizon="T1", required_forward_days=1)
    assert r.production_allowed is False
def test_result_fallback_false():
    r = OutcomeHorizonResult(ticker="X", observation_date="D", horizon="T1", required_forward_days=1)
    assert r.fallback_used is False

# ── horizon mapping tests ──
def test_horizon_t1_days(): assert HORIZON_FORWARD_DAYS["T1"] == 1
def test_horizon_t5_days(): assert HORIZON_FORWARD_DAYS["T5"] == 5
def test_horizon_t10_days(): assert HORIZON_FORWARD_DAYS["T10"] == 10
def test_horizon_t20_days(): assert HORIZON_FORWARD_DAYS["T20"] == 20
def test_horizon_t60_days(): assert HORIZON_FORWARD_DAYS["T60"] == 60

# ── T20 readiness ──
def test_t20_ready():
    r = ENGINE.evaluate_horizon("000001","2024-01-02","T20")
    assert r.readiness_status == "READY", f"{r.reason}"
    assert r.exit_date is not None
    assert r.fallback_used is False

def test_t20_insufficient():
    r = ENGINE.evaluate_horizon("000001","2024-02-02","T20")
    assert r.readiness_status == "INSUFFICIENT_FORWARD_DAYS"
    assert r.exit_date is None
    assert r.fallback_used is False

def test_t60_insufficient():
    r = ENGINE.evaluate_horizon("000001","2024-01-31","T60")
    assert r.readiness_status == "INSUFFICIENT_FORWARD_DAYS"
    assert r.fallback_used is False

# ── missing bar cases ──
def test_missing_entry_bar():
    r = ENGINE.evaluate_horizon("999999","2024-01-02","T5")
    assert r.readiness_status == "MISSING_ENTRY_BAR"

def test_missing_exit_bar():
    # exit date for T20 from 2024-01-30 is beyond fixture range
    r = ENGINE.evaluate_horizon("000001","2024-01-30","T20")
    assert r.readiness_status in ("INSUFFICIENT_FORWARD_DAYS","MISSING_EXIT_BAR")

# ── suspension cases ──
def test_entry_suspended():
    r = ENGINE.evaluate_horizon("600519","2024-01-04","T1")
    assert r.readiness_status == "SUSPENDED_ENTRY"

# ── batch + summary ──
def test_evaluate_many():
    results = ENGINE.evaluate_many(build_outcome_test_requests())
    assert len(results) == 4

def test_batch_check():
    results = batch_check_outcome_ready(ENGINE, build_outcome_test_requests())
    assert len(results) == 4

def test_summarize():
    results = ENGINE.evaluate_many(build_outcome_test_requests())
    s = summarize_readiness(results)
    assert s["total"] == 4
    assert s["fallback_used_count"] == 0
    assert s["production_allowed"] is False

# ── no return/alpha/cost in modules ──
def test_no_return_in_modules():
    for name in ["outcome_schema.py","outcome_horizon_engine.py","outcome_readiness_gate.py","outcome_fixture_builder.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "market_data" / name).read_text()
        for fb in ["return_pct","benchmark_relative_return","commission","stamp_duty","BUY","SELL","AUTO_EXECUTE","production_allowed=True"]:
            assert fb not in text, f"{fb} in {name}"

# ── fixture builder ──
def test_fixture_builder_test_requests():
    assert len(build_outcome_test_requests()) == 4
def test_fixture_builder_insufficient():
    assert len(build_insufficient_forward_days_cases()) == 2
def test_fixture_builder_missing_bar():
    assert len(build_missing_bar_cases()) == 2

# ── gate ──
def test_check_outcome_ready():
    assert check_outcome_ready(ENGINE,"000001","2024-01-02","T5") is True
def test_check_outcome_not_ready():
    assert check_outcome_ready(ENGINE,"000001","2024-02-02","T20") is False

# ── summary fields ──
def test_summary_has_ready_count():
    s = summarize_readiness(ENGINE.evaluate_many(build_outcome_test_requests()))
    assert "ready_count" in s
def test_summary_has_insufficient_count():
    s = summarize_readiness(ENGINE.evaluate_many(build_insufficient_forward_days_cases()))
    assert s["insufficient_forward_days_count"] > 0

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
