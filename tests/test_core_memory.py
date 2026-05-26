"""Core Memory tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.hermes_kernel.core_memory import build_core_memory_preview

def test_core_memory_preview_read_only():
    r = build_core_memory_preview(memory_id="m1", memory_type="lesson", title="test", content="content")
    assert r["preview_only"] is True
    assert r["write_allowed"] is False
    assert r["hermes_memory_write_allowed"] is False
    print("✅ core memory preview read-only")

def test_core_memory_has_safety():
    r = build_core_memory_preview(memory_id="m2", memory_type="rule", title="rule1", content="rule")
    assert r["safety"]["real_trade_allowed"] is False
    assert r["safety"]["preview_only"] is True
    print("✅ core memory has safety")

if __name__ == "__main__":
    test_core_memory_preview_read_only()
    test_core_memory_has_safety()
    print("\n🏁 Core Memory tests PASS")
