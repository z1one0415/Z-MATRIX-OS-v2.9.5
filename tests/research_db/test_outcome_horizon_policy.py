#!/usr/bin/env python3
"""ResearchDB Phase 0: Outcome Horizon Policy Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zmatrix.research_db.outcome_horizon_policy import HORIZON_DAYS, validate_forward_window


def test_all_horizons_defined():
    assert set(HORIZON_DAYS.keys()) == {"T1", "T3", "T5", "T10", "T20", "T60"}


def test_t20_ready():
    r = validate_forward_window("T20", 25)
    assert r["ready"] is True
    assert r["required_days"] == 20


def test_t20_blocked_insufficient():
    r = validate_forward_window("T20", 18)
    assert r["ready"] is False
    assert r["blocked_reason"] == "INSUFFICIENT_FORWARD_TRADING_DAYS"
    assert r["fallback_last_price_allowed"] is False


def test_t60_ready():
    r = validate_forward_window("T60", 60)
    assert r["ready"] is True


def test_t60_blocked():
    r = validate_forward_window("T60", 59)
    assert r["ready"] is False


def test_unknown_horizon():
    r = validate_forward_window("TX", 100)
    assert r["ready"] is False
    assert "UNKNOWN_HORIZON" in r["blocked_reason"]


def test_fallback_never_allowed():
    for h in ["T20", "T60"]:
        r = validate_forward_window(h, 0)
        assert r["fallback_last_price_allowed"] is False


if __name__ == "__main__":
    test_all_horizons_defined()
    test_t20_ready()
    test_t20_blocked_insufficient()
    test_t60_ready()
    test_t60_blocked()
    test_unknown_horizon()
    test_fallback_never_allowed()
    print("✅ ResearchDB Phase 0 Outcome Horizon Policy tests PASS")
