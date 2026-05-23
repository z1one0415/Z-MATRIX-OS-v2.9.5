"""R-Matrix v2.0 four-king service — full king tests"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_four_king_full_pass():
    from zmatrix.scoring.r_matrix.r_matrix_service import evaluate_r_matrix_cycle
    random.seed(42)
    prices = [100.0]
    for i in range(300):
        prices.append(prices[-1] + random.gauss(0.3, 3))
    
    r = evaluate_r_matrix_cycle("TEST", prices)
    assert r["version"] == "v2.0-cycle-four-king"
    assert r["legacy_fallback"] is False
    assert r["status"] in ("PASS", "DEGRADED")
    assert len(r["kings"]) >= 3, f"only {len(r['kings'])} kings"
    assert r["r_score"] is not None
    assert r["r_action_cap"] in ("WAIT", "WATCH_ENTRY", "HOLD", "RIDE", "AVOID", "WAIT_CONFIRM")
    print(f"✅ 4-king: status={r['status']} kings={len(r['kings'])} score={r['r_score']} cap={r['r_action_cap']}")

def test_impulse_king_output():
    from zmatrix.scoring.r_matrix.r_matrix_service import _impulse_king
    prices = [100 + i*0.2 for i in range(100)]
    r = _impulse_king(prices)
    assert "king" in r and r["king"] == "impulse"
    assert "type" in r
    assert "score" in r
    assert "evidence" in r
    print(f"✅ impulse: type={r['type']} score={r['score']}")

if __name__ == "__main__":
    test_four_king_full_pass()
    test_impulse_king_output()
    print("\n🏁 R-Matrix v2.0 four-king tests PASS")
