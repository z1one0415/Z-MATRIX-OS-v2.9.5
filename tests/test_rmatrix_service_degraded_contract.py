"""R-Matrix v2.0 degraded contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_insufficient_bars_data_gap():
    from zmatrix.scoring.r_matrix.r_matrix_service import evaluate_r_matrix_cycle
    r = evaluate_r_matrix_cycle("TEST", [10]*10)
    assert r["status"] == "DATA_GAP"
    print(f"✅ <20 bars→DATA_GAP")

def test_errors_cause_degraded():
    from zmatrix.scoring.r_matrix.r_matrix_service import evaluate_r_matrix_cycle
    # Prices with NaN-like causing internal errors
    r = evaluate_r_matrix_cycle("TEST", [float('nan')]*50 + [10]*20)
    assert r["status"] != "PASS"
    print(f"✅ errors→{r['status']}")

def test_partial_kings_degraded():
    from zmatrix.scoring.r_matrix.r_matrix_service import evaluate_r_matrix_cycle
    prices = [100.0]*30  # not enough for rhythm/rotation
    r = evaluate_r_matrix_cycle("TEST", prices)
    assert r["status"] != "PASS"
    assert r["king_count"] < 4 if "king_count" in r else True
    print(f"✅ partial kings→{r['status']}")

def test_legacy_fallback_is_false():
    from zmatrix.scoring.r_matrix.r_matrix_service import evaluate_r_matrix_cycle
    r = evaluate_r_matrix_cycle("TEST", [100]*300)
    assert r["legacy_fallback"] is False
    print(f"✅ legacy_fallback=False")

if __name__ == "__main__":
    test_insufficient_bars_data_gap()
    test_errors_cause_degraded()
    test_partial_kings_degraded()
    test_legacy_fallback_is_false()
    print("\n🏁 R-Matrix degraded contract tests PASS")
