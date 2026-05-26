"""Historical Replay BRD Adapter tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.historical_replay.brd_replay_adapter import build_brd_replay_payload, normalize_brd_replay_result

def test_brd_replay_payload_is_point_in_time_only():
    r = build_brd_replay_payload(replay_date="2024-06-03", ticker="002472", price_snapshot={"close":45.0})
    assert r["point_in_time_only"] is True
    assert r["future_data_allowed"] is False
    print("✅ point_in_time_only")

def test_brd_replay_payload_no_real_trade():
    r = build_brd_replay_payload(replay_date="2024-06-03", ticker="002472", price_snapshot={})
    assert r["safety"]["real_trade_allowed"] is False
    assert r["safety"]["broker_order_allowed"] is False
    print("✅ no real trade, no broker")

def test_brd_replay_result_normalizes_role_and_decision():
    r = normalize_brd_replay_result(replay_date="2024-06-03", ticker="002472", brd_result={"role":"A_LONG_CORE","decision":"ENTER"})
    assert r["role"] == "A_LONG_CORE"
    assert r["decision"] == "ENTER"
    print("✅ normalize works")

if __name__ == "__main__":
    test_brd_replay_payload_is_point_in_time_only()
    test_brd_replay_payload_no_real_trade()
    test_brd_replay_result_normalizes_role_and_decision()
    print("\n🏁 Replay Adapter PASS")
