"""G18 Conflict Resolver v1.0 tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_g09_sell_vs_g18_entry_high_conflict():
    from zmatrix.prediction.conflict_resolver import resolve_upstream_conflicts
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="PAPER_TRACK")
    up = {"g09": {"position_action": "REDUCE_CORE", "sell_decision": {}, "hard_blocks": []}, "g08": {}, "g11": {}, "g14": {}}
    r = resolve_upstream_conflicts(up, p)
    assert r["conflict_level"] == "HIGH"
    assert r["suggested_action_cap"] == "WAIT"
    assert any(c["code"] == "G09_SELL_VS_G18_ENTRY" for c in r["conflicts"])
    print("✅ G09 sell vs G18 entry: HIGH")

def test_g09_hard_blocks_high_conflict():
    from zmatrix.prediction.conflict_resolver import resolve_upstream_conflicts
    p = type("", (), {"action_proposal": "PAPER_TRACK"})()
    up = {"g09": {"hard_blocks": ["ROTATION_TREND_DOWN"], "sell_decision": {}}, "g08": {}, "g11": {}, "g14": {}}
    r = resolve_upstream_conflicts(up, p)
    assert r["conflict_level"] == "HIGH"
    assert r["suggested_action_cap"] == "WAIT"
    print("✅ G09 hard_blocks: HIGH")

def test_g08_narrative_decay_medium_conflict():
    from zmatrix.prediction.conflict_resolver import resolve_upstream_conflicts
    p = type("", (), {"action_proposal": "PAPER_TRACK"})()
    up = {"g09": {}, "g08": {"available": True, "narrative_decay": 0.8, "bubble_temperature": 0.5}, "g11": {}, "g14": {}}
    r = resolve_upstream_conflicts(up, p)
    assert r["conflict_level"] in ("MEDIUM", "HIGH")
    assert any(c["code"] == "G08_NARRATIVE_DECAY_OR_BUBBLE" for c in r["conflicts"])
    print("✅ G08 narrative decay: MEDIUM")

def test_g11_warning_only_does_not_force_wait():
    from zmatrix.prediction.conflict_resolver import resolve_upstream_conflicts
    p = type("", (), {"action_proposal": "PAPER_TRACK"})()
    up = {"g09": {}, "g08": {}, "g11": {"hard_veto_allowed": False, "warnings": ["concentration_high"]}, "g14": {}}
    r = resolve_upstream_conflicts(up, p)
    assert r["suggested_action_cap"] != "WAIT"  # G11 alone should not force WAIT
    print(f"✅ G11 warning: cap={r['suggested_action_cap']}")

def test_z16_g17_missing_confirmation():
    from zmatrix.prediction.conflict_resolver import resolve_upstream_conflicts
    p = type("", (), {"action_proposal": "PAPER_TRACK"})()
    up = {"g09": {}, "g08": {}, "g11": {}, "g14": {},
          "z16": {"available": False}, "g17": {"available": False}}
    r = resolve_upstream_conflicts(up, p)
    assert any(c["code"] == "Z16_G17_CONFIRMATION_MISSING" for c in r["conflicts"])
    print("✅ Z16/G17 missing: MEDIUM")

def test_final_decision_contains_conflict_resolution()
    test_conflict_resolver_never_upgrades_wait_to_paper()
    test_final_decision_never_upgrades_wait_to_paper_pending():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="PAPER_TRACK")
    up = {"g09": {"available": True, "position_action": "REDUCE_CORE", "sell_decision": {}, "hard_blocks": []},
          "g08": {}, "g11": {}, "g14": {}, "z16": {}, "g17": {}}
    r = build_final_decision(p, up)
    assert "conflict_resolution" in r
    assert "conflicts" in r
    print(f"✅ final_decision: conflict_resolution={r.get('conflict_level','?')}")


def test_conflict_resolver_never_upgrades_wait_to_paper():
    from zmatrix.prediction.conflict_resolver import resolve_upstream_conflicts
    p = type("", (), {"action_proposal": "WAIT"})()
    up = {"g09": {}, "g08": {}, "g11": {}, "g14": {}, "z16": {"available": False}, "g17": {"available": False}}
    r = resolve_upstream_conflicts(up, p)
    assert r["suggested_action_cap"] == "WAIT"
    print("✅ conflict: never upgrades WAIT to paper")

def test_final_decision_never_upgrades_wait_to_paper_pending():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.50, action_proposal="WAIT")
    up = {"g09": {}, "g08": {}, "g11": {}, "g14": {}, "z16": {"available": False}, "g17": {"available": False}}
    r = build_final_decision(p, up)
    assert r["entry_intent"] == "WAIT"
    print("✅ final_decision: never upgrades WAIT")

if __name__ == "__main__":
    test_g09_sell_vs_g18_entry_high_conflict()
    test_g09_hard_blocks_high_conflict()
    test_g08_narrative_decay_medium_conflict()
    test_g11_warning_only_does_not_force_wait()
    test_z16_g17_missing_confirmation()
    test_final_decision_contains_conflict_resolution()
    test_conflict_resolver_never_upgrades_wait_to_paper()
    test_final_decision_never_upgrades_wait_to_paper_pending()
    print("\n🏁 G18 Conflict Resolver v1.0 tests PASS")
