"""Verify G14 uses r_matrix_service v2.0, not old R-Matrix v1.1"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_g14_no_old_rmatrix():
    s = open("pipelines/Z-G14_月度全量选股/gate_pipeline.py").read()
    assert "oscillation_king_ranker_v11" not in s, "G14 still imports old R-Matrix"
    assert "rank_type_a_horizontal" not in s, "G14 still calls Type A"
    assert "_get_r_matrix" not in s, "G14 still has old _get_r_matrix function"
    print("✅ no old R-Matrix")

def test_g14_uses_r_matrix_service():
    s = open("pipelines/Z-G14_月度全量选股/gate_pipeline.py").read()
    assert "r_matrix_service" in s or "evaluate_r_matrix_cycle" in s, "G14 doesn't use r_matrix_service"
    assert "v2.0-cycle-four-king" in s, "G14 doesn't reference v2.0"
    assert "R-Matrix v1.1" not in s, "G14 still references v1.1"
    print("✅ uses r_matrix_service v2.0")

if __name__ == "__main__":
    test_g14_no_old_rmatrix()
    test_g14_uses_r_matrix_service()
    print("\n🏁 Z-G14 R-Matrix service tests PASS")
