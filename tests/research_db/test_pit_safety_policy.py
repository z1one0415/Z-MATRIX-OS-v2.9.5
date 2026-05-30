#!/usr/bin/env python3
"""ResearchDB Phase 0: PIT Safety Policy Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zmatrix.research_db.pit_policy import PITStatus, evaluate_pit_status


def test_pit_safe():
    assert evaluate_pit_status("2026-01-15", "2026-01-10") == PITStatus.PIT_SAFE


def test_pit_unknown_no_date():
    assert evaluate_pit_status("2026-01-15", None) == PITStatus.UNKNOWN_PIT_STATUS


def test_pit_current_snapshot():
    assert evaluate_pit_status("2026-01-15", "2026-01-10", current_snapshot=True) == PITStatus.CURRENT_SNAPSHOT_ONLY


def test_pit_blocked_future_date():
    assert evaluate_pit_status("2026-01-15", "2026-02-01") == PITStatus.BLOCKED_FOR_BACKTEST


def test_pit_safe_same_day():
    assert evaluate_pit_status("2026-01-15", "2026-01-15") == PITStatus.PIT_SAFE


if __name__ == "__main__":
    test_pit_safe()
    test_pit_unknown_no_date()
    test_pit_current_snapshot()
    test_pit_blocked_future_date()
    test_pit_safe_same_day()
    print("✅ ResearchDB Phase 0 PIT Safety Policy tests PASS")
