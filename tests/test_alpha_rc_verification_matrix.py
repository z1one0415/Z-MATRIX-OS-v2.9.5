"""Alpha RC Verification Matrix tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_rc.verification_matrix import build_v3_alpha_verification_matrix

def test_verification_matrix_covers_8_components():
    m = build_v3_alpha_verification_matrix()
    assert len(m["rows"]) == 8
    print(f"✅ matrix covers {len(m['rows'])} components")

def test_verification_matrix_all_status_frozen_pass():
    m = build_v3_alpha_verification_matrix()
    for row in m["rows"]:
        assert row["status"] == "FROZEN_PASS"
        assert row["runtime_allowed"] is False
    print("✅ all rows FROZEN_PASS, runtime=False")

if __name__ == "__main__":
    test_verification_matrix_covers_8_components()
    test_verification_matrix_all_status_frozen_pass()
    print("\n🏁 Alpha RC Verification Matrix tests PASS")
