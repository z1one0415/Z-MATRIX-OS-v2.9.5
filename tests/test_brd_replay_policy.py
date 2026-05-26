"""BRD Replay Policy tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_replay.policy import assert_no_brd_replay_runtime_effects

def test_rejects_real_trade():
    v = assert_no_brd_replay_runtime_effects({"real_trade_allowed":True})
    assert any("real_trade_allowed" in e for e in v)

def test_rejects_non_dict_safety():
    v = assert_no_brd_replay_runtime_effects({"safety":"bad"})
    assert "safety must be dict" in v

if __name__ == "__main__":
    test_rejects_real_trade(); test_rejects_non_dict_safety()
    print("\n🏁 Policy PASS")
