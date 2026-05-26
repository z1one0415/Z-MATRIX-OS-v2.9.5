"""Safety Matrix tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.safety_matrix import build_cross_layer_safety_matrix

def test_safety_matrix_all_layers_false():
    m = build_cross_layer_safety_matrix()
    for layer, row in m["matrix"].items():
        for cap, allowed in row.items():
            assert allowed is False, f"{layer}.{cap} unexpectedly allowed"
    print("✅ all layers forbid all capabilities")

def test_safety_matrix_passes():
    m = build_cross_layer_safety_matrix()
    assert m["pass"] is True, f"violations: {m.get('violations', [])}"
    assert m["violations"] == []
    print("✅ safety matrix passes")

def test_safety_matrix_includes_system_controller():
    m = build_cross_layer_safety_matrix()
    assert "SYSTEM_CONTROLLER" in m["layers"]
    for allowed in m["matrix"]["SYSTEM_CONTROLLER"].values():
        assert allowed is False
    print("✅ SYSTEM_CONTROLLER as non-runtime layer, all False")

if __name__ == "__main__":
    test_safety_matrix_all_layers_false()
    test_safety_matrix_passes()
    test_safety_matrix_includes_system_controller()
    print("\n🏁 Safety Matrix tests PASS")
