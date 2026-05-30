#!/usr/bin/env python3
"""ResearchDB Phase 0: No Production Boundary Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zmatrix.research_db.no_production_boundary import SAFETY_FLAGS, check_boundary, is_production_allowed


def test_all_safety_flags_blocked():
    assert SAFETY_FLAGS["real_trade_allowed"] is False
    assert SAFETY_FLAGS["broker_order_allowed"] is False
    assert SAFETY_FLAGS["runtime_enabled"] is False
    assert SAFETY_FLAGS["auto_buy_allowed"] is False
    assert SAFETY_FLAGS["auto_sell_allowed"] is False
    assert SAFETY_FLAGS["production_allowed"] is False
    assert SAFETY_FLAGS["paper_only"] is True
    assert SAFETY_FLAGS["human_review_required"] is True


def test_check_boundary_returns_safe():
    r = check_boundary()
    assert r["status"] == "SAFE"
    assert r["production_allowed"] is False


def test_is_production_allowed_always_false():
    assert is_production_allowed() is False


if __name__ == "__main__":
    test_all_safety_flags_blocked()
    test_check_boundary_returns_safe()
    test_is_production_allowed_always_false()
    print("✅ ResearchDB Phase 0 No Production Boundary tests PASS")
