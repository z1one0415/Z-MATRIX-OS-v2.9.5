"""Integration Readiness Map tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.readiness_map import build_v3_alpha_readiness_map

def test_readiness_map_contains_all_v3_layers():
    m = build_v3_alpha_readiness_map()
    assert "EVENT_STORE" in m["layers"]
    assert "HERMES_MEMORY" in m["layers"]
    assert "APPROVAL_LOOP" in m["layers"]
    print(f"✅ readiness map has {len(m['layers'])} layers")

def test_readiness_map_runtime_allowed_false():
    m = build_v3_alpha_readiness_map()
    assert m["alpha_runtime_allowed"] is False
    for layer in m["layers"].values():
        assert layer["runtime_allowed"] is False
    print("✅ runtime_allowed=False for all layers")

def test_required_pipelines_present():
    m = build_v3_alpha_readiness_map()
    assert len(m["missing_pipelines"]) == 0
    print("✅ all required pipelines present")

if __name__ == "__main__":
    test_readiness_map_contains_all_v3_layers()
    test_readiness_map_runtime_allowed_false()
    test_required_pipelines_present()
    print("\n🏁 Readiness Map tests PASS")
