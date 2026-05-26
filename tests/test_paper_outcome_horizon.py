"""Horizon tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.horizon import build_horizon_dates, anchor_to_next_trading_day

def test_build_horizon_dates():
    r = build_horizon_dates("2024-06-03")  # Monday
    assert r["entry_date"] == "2024-06-03"
    assert r["t5_date"] > r["entry_date"]
    print("✅ horizon dates built")

def test_weekend_anchor():
    r = anchor_to_next_trading_day("2024-06-01")  # Sat → Mon
    assert r == "2024-06-03"
    print("✅ weekend anchored to Monday")

if __name__ == "__main__":
    test_build_horizon_dates()
    test_weekend_anchor()
    print("\n🏁 Horizon PASS")
