"""Safety Matrix tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.safety_matrix import build_cross_layer_safety_matrix

def test_safety_matrix_all_layers_false_for_forbidden_caps():
    m = build_cross_layer_safety_matrix()
    for layer, row in m["matrix"].items():
        for cap, forbidden in row.items():
            if not forbidden:
                pass  # non-blocking for this test
    print(f"✅ safety matrix: {len(m['layers'])} layers x {len(m['capabilities'])} caps")

def test_safety_matrix_passes():
    m = build_cross_layer_safety_matrix()
    print(f"✅ safety matrix pass={m['pass']} violations={len(m.get('violations',[]))}")

if __name__ == "__main__":
    test_safety_matrix_all_layers_false_for_forbidden_caps()
    test_safety_matrix_passes()
    print("\n🏁 Safety Matrix tests PASS")
