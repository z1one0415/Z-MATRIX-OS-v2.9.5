"""Learned Heuristics tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.hermes_kernel.learned_heuristics import build_learned_heuristic_preview

def test_heuristic_preview_read_only():
    r = build_learned_heuristic_preview(
        source_event_id="a"*32, title="test", rule="rule",
        scope={"ticker": "002472"}, confidence="MEDIUM", evidence_count=3,
    )
    assert r["preview_only"] is True
    assert r["write_allowed"] is False
    print("✅ heuristic preview read-only")

def test_heuristic_has_safety():
    r = build_learned_heuristic_preview(
        source_event_id="b"*32, title="rule2", rule="rule2",
        scope={}, confidence="HIGH", evidence_count=5,
    )
    assert r["safety"]["hermes_memory_write_allowed"] is False
    assert r["safety"]["auto_calibration_allowed"] is False
    print("✅ heuristic has safety")

def test_learned_heuristic_has_decay_status():
    r = build_learned_heuristic_preview(
        source_event_id="a" * 32,
        title="test",
        rule="observe risk",
        scope={"ticker": "002472"},
        confidence="HIGH",
        evidence_count=3,
    )
    h = r["heuristic"]
    assert h["decay_status"] == "ACTIVE"
    assert h["status"] == "ACTIVE"
    print("✅ heuristic has both decay_status and status")

if __name__ == "__main__":
    test_heuristic_preview_read_only()
    test_heuristic_has_safety()
    test_learned_heuristic_has_decay_status()
    print("\n🏁 Learned Heuristics tests PASS")
