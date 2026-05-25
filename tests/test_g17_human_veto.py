"""G17 Human Veto contract tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.g17_human_veto import build_g17_human_veto_preview, _FORBIDDEN
import json


def test_veto_preview_fields():
    r = build_g17_human_veto_preview({"ticker": "002472", "role": "A_LONG_CORE"})
    assert r["human_final_override_required"] is True
    assert r["system_action_limit"] == "PAPER_ONLY"
    assert r["human_must_confirm_before_real_trade"] is True
    assert r["g17_can_veto_all"] is True
    print("✅ g17: veto preview fields correct")


def test_no_forbidden():
    r = build_g17_human_veto_preview({"ticker": "002472"})
    for t in _FORBIDDEN:
        assert t not in json.dumps(r)
    print("✅ g17: no forbidden tokens")


if __name__ == "__main__":
    test_veto_preview_fields(); test_no_forbidden()
    print("\n🏁 G17 Human Veto — tests PASS")
