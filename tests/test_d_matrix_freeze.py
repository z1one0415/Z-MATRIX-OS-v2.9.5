"""D_MATRIX_FREEZE tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.d_matrix_freeze import evaluate_d_matrix_freeze

def test_d_matrix_freeze_blocks_black_horse_entry():
    r = evaluate_d_matrix_freeze(candidate_context={"role": "D_BLACK_HORSE"}, market_signals={"sector_heat_status": "RETREAT"})
    assert r["decision"] == "FREEZE"
    assert r["freeze_new_entries"] is True
    assert r["fallback_action"] == "WATCH_ONLY"
    print("✅ D-Matrix freeze blocks black horse entry")

if __name__ == "__main__":
    test_d_matrix_freeze_blocks_black_horse_entry()
    print("\n🏁 D-Matrix Freeze tests PASS")
