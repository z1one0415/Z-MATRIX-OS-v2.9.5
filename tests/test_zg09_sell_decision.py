"""Z-G09 sell_decision contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_shuanghuan_base_case():
    """双环传动: cost=41.711, price=44.40, shares=1800, no strong harvest → HOLD_PROFIT"""
    from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision
    r = evaluate_position_sell_decision("002472", 1800, 41.711, 44.40, {
        "hard_blocks": [], "exit_alert": "NONE",
        "kings": {
            "rhythm": {"action": "BOX", "position": 0.75, "type": "BOX"},
            "rotation": {"type": "TREND_UP", "action": "HOLD"},
            "oscillation": {"position": 0.74, "action": "HARVEST"},
            "impulse": {"action": "WAIT"},
        }})
    assert r["profit_band"] == "PROFIT_5_10"
    assert round(r["profit_pct"], 1) == 6.4
    assert r["position_action"] in {"HOLD_PROFIT", "HOLD_CORE"}
    assert r["sell_ratio"] == 0.0
    assert r["sell_shares"] == 0
    assert r["keep_shares"] == 1800
    assert r["profit_lines"]["cost_plus_10"] == round(41.711 * 1.10, 2)
    print(f"✅ 双环 base: {r['position_action']} profit={r['profit_pct']}%")


def test_rhythm_harvest_rotation_not_broken():
    """律动HARVEST + 轮动未坏 → SELL_TRADING_KEEP_CORE 33%"""
    from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision
    r = evaluate_position_sell_decision("002472", 1800, 41.711, 47.00, {
        "hard_blocks": [], "exit_alert": "HARVEST",
        "kings": {
            "rhythm": {"action": "HARVEST", "position": 0.90, "type": "TREND_UP"},
            "rotation": {"type": "TREND_UP", "action": "HOLD"},
            "oscillation": {}, "impulse": {},
        }})
    assert r["position_action"] == "SELL_TRADING_KEEP_CORE"
    assert r["sell_ratio"] == 0.33
    assert r["sell_shares"] == 600  # 1800*0.33≈594→round to 600
    assert r["keep_shares"] == 1200
    assert "RHYTHM_HIGH_SELL_TRADING_KEEP_ROTATION_CORE" in r["reason_codes"]
    print(f"✅ 律动高抛: sell={r['sell_shares']}/{r['keep_shares']}")


def test_rhythm_and_rotation_both_harvest():
    """律动HARVEST + 轮动HARVEST → REDUCE_CORE 50% (优先级高于单高)"""
    from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision
    r = evaluate_position_sell_decision("002472", 1800, 41.711, 47.00, {
        "hard_blocks": [], "exit_alert": "HARVEST",
        "kings": {
            "rhythm": {"action": "HARVEST", "position": 0.90, "type": "TREND_UP"},
            "rotation": {"type": "TREND_UP", "action": "HARVEST"},
            "oscillation": {}, "impulse": {},
        }})
    assert r["position_action"] == "REDUCE_CORE", f"got {r['position_action']}"
    assert r["sell_ratio"] == 0.50
    assert "RHYTHM_AND_ROTATION_HIGH_REDUCE_CORE" in r["reason_codes"]
    print(f"✅ 双高: {r['position_action']} ratio={r['sell_ratio']}")


def test_rotation_trend_down():
    """轮动TREND_DOWN → MAJOR_REDUCE_OR_EXIT"""
    from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision
    r = evaluate_position_sell_decision("002472", 1800, 41.711, 44.40, {
        "hard_blocks": ["ROTATION_TREND_DOWN"], "exit_alert": "NONE",
        "kings": {"rhythm": {}, "rotation": {"type": "TREND_DOWN"}, "oscillation": {}, "impulse": {}},
    })
    assert r["position_action"] == "MAJOR_REDUCE_OR_EXIT"
    assert r["sell_ratio"] >= 0.5
    assert "ROTATION_BROKEN_DO_NOT_WAIT_HIGHER" in r["reason_codes"]
    print(f"✅ 轮动坏: {r['position_action']}")


def test_no_trade_action_leak():
    from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision
    forbidden = {"BUY", "SELL", "AUTO_TRADE", "MARKET_ORDER"}
    for price in [44, 47, 35]:
        r = evaluate_position_sell_decision("002472", 1800, 41.71, price, {
            "hard_blocks": [], "exit_alert": "NONE",
            "kings": {"rhythm": {}, "rotation": {"type": "TREND_UP"}, "oscillation": {}, "impulse": {}},
        })
        assert r["position_action"] not in forbidden, f"leaked {r['position_action']}"
        assert "BUY" not in str(r)
    print("✅ no trade action leak")


def test_profit_lines():
    from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision
    r = evaluate_position_sell_decision("002472", 1800, 41.711, 44.40, {
        "hard_blocks": [], "exit_alert": "NONE",
        "kings": {"rhythm": {}, "rotation": {"type": "TREND_UP"}, "oscillation": {}, "impulse": {}},
    })
    assert r["profit_lines"]["cost_plus_10"] == round(41.711 * 1.10, 2)
    assert r["profit_lines"]["cost_plus_20"] == round(41.711 * 1.20, 2)
    assert r["protection_line"] > 0
    print(f"✅ profit lines: +10%={r['profit_lines']['cost_plus_10']} +20%={r['profit_lines']['cost_plus_20']}")


if __name__ == "__main__":
    test_shuanghuan_base_case()
    test_rhythm_harvest_rotation_not_broken()
    test_rhythm_and_rotation_both_harvest()
    test_rotation_trend_down()
    test_no_trade_action_leak()
    test_profit_lines()
    print("\n🏁 Z-G09 sell decision tests PASS")
