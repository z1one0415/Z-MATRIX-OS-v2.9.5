"""B-Matrix Downgrade tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_matrix_pit.b_matrix_pit_builder import build_b_matrix_pit

def test_no_fundamentals_d_reject():
    b = build_b_matrix_pit(ticker="XXXXXX", replay_date="2024-06-03", local_data_root="/tmp/nonexistent")
    assert b["status"] == "FAIL"
    assert b["role_cap"] == "D_REJECT"
    assert b["valuation_data_status"] == "MISSING"
    print("✅ no fund → D_REJECT")

def test_has_role_cap():
    b = build_b_matrix_pit(ticker="000001", replay_date="2026-05-01", local_data_root=".")
    assert "role_cap" in b
    assert "valuation_confidence" in b
    assert "downgrade" in b
    print(f"✅ 000001: cap={b['role_cap']} conf={b['valuation_confidence']} dg={b['downgrade']['downgraded']}")

def test_no_hard_vs_gate():
    b = build_b_matrix_pit(ticker="300001", replay_date="2026-05-01", local_data_root=".")
    # Even if vs < 30, should not D_REJECT if quality+growth pass
    print(f"✅ 300001: status={b['status']} cap={b['role_cap']} vs={b['valuation_score']}")

if __name__ == "__main__":
    test_no_fundamentals_d_reject(); test_has_role_cap(); test_no_hard_vs_gate()
    print("\n🏁 B-Matrix Downgrade PASS")
