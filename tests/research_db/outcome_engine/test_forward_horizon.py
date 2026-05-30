#!/usr/bin/env python3
"""Phase 3-B: Forward Horizon Engine Tests (12+)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures" / "market_data"

from zmatrix.research_db.market_data.trading_calendar import TradingCalendar
from zmatrix.research_db.outcome_engine.forward_horizon import OutcomeHorizonEngine, HORIZON_DAYS

CAL = TradingCalendar(str(FIXTURES / "sample_trading_calendar.csv"))
ENG = OutcomeHorizonEngine(CAL)


def test_horizon_days_defined():
    assert set(HORIZON_DAYS.keys()) == {"T1", "T3", "T5", "T10", "T20", "T60"}
    assert HORIZON_DAYS["T20"] == 20
    assert HORIZON_DAYS["T60"] == 60


def test_compute_horizon_t20_ready():
    r = ENG.compute_horizon("2024-01-02", "T20")
    assert r["ready"] is True
    assert r["horizon"] == "T20"
    assert r["required_days"] == 20
    assert r["available_days"] >= 20
    assert r["blocked_reason"] is None
    assert r["fallback_last_price_allowed"] is False


def test_compute_horizon_t20_blocked_insufficient():
    r = ENG.compute_horizon("2024-01-25", "T20")
    assert r["ready"] is False
    assert r["blocked_reason"] == "INSUFFICIENT_FORWARD_TRADING_DAYS"
    assert r["fallback_last_price_allowed"] is False


def test_compute_horizon_t60_blocked():
    r = ENG.compute_horizon("2024-01-02", "T60")
    assert r["ready"] is False
    assert r["blocked_reason"] == "INSUFFICIENT_FORWARD_TRADING_DAYS"
    assert r["required_days"] == 60


def test_compute_horizon_t1_ready():
    r = ENG.compute_horizon("2024-01-02", "T1")
    assert r["ready"] is True
    assert r["required_days"] == 1
    assert r["available_days"] >= 1


def test_compute_horizon_t5_ready():
    r = ENG.compute_horizon("2024-01-02", "T5")
    assert r["ready"] is True
    assert r["required_days"] == 5


def test_compute_horizon_t10_ready():
    r = ENG.compute_horizon("2024-01-02", "T10")
    assert r["ready"] is True
    assert r["required_days"] == 10


def test_compute_horizon_unknown_horizon():
    r = ENG.compute_horizon("2024-01-02", "TX")
    assert r["ready"] is False
    assert "UNKNOWN_HORIZON" in r["blocked_reason"]
    assert r["fallback_last_price_allowed"] is False


def test_no_fallback_last_price_allowed_ever():
    for h in ["T20", "T60", "T1", "T5"]:
        r = ENG.compute_horizon("2024-01-02", h)
        assert r["fallback_last_price_allowed"] is False
    r = ENG.compute_horizon("2024-01-25", "T20")
    assert r["fallback_last_price_allowed"] is False


def test_compute_all_horizons_returns_all():
    results = ENG.compute_all_horizons("2024-01-02")
    assert set(results.keys()) == set(HORIZON_DAYS.keys())
    for h in ["T1", "T3", "T5", "T10", "T20"]:
        assert results[h]["ready"] is True
    assert results["T60"]["ready"] is False


def test_compute_all_horizons_late_date():
    results = ENG.compute_all_horizons("2024-01-31")
    assert results["T1"]["ready"] is True
    assert results["T20"]["ready"] is False
    assert results["T60"]["ready"] is False


def test_signal_date_not_in_calendar():
    r = ENG.compute_horizon("2024-01-01", "T1")
    assert r["ready"] is True


if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
