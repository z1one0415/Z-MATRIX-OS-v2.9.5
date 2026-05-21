"""Z9 calibration contract — CURRENT_PRICE_PROXY, no auto-adjust"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_z9_current_price_proxy_not_strict_t_plus_n():
    """backtest_at returns CURRENT_PRICE_PROXY, is_strict_t_plus_n=False"""
    from hermes.Z9_Calibration_Engine import Z9CalibrationEngine
    engine = Z9CalibrationEngine()

    # Pre-fill with enough predictions and cal log
    engine.db["predictions"] = [
        {"ticker": "600519", "name": "茅台", "predicted_price": 100,
         "action": "WATCH", "scoring_weights": {"FQS": 0.2, "ISS": 0.15},
         "date": "2026-05-15", "target_days": 5}
    ] * 60
    engine.db["calibration_log"] = [
        {"cal_count": i, "calibrated_at": "2026-05-15T00:00:00",
         "backtest_mode": "CURRENT_PRICE_PROXY", "is_strict_t_plus_n": False}
        for i in range(1, 5)
    ]
    engine._save_db = lambda: None

    r = engine.backtest_at(days=5, live_prices={
        "600519": {"price": 110, "pct": 10.0, "name": "贵州茅台"},
    })

    assert r["backtest_mode"] == "CURRENT_PRICE_PROXY"
    assert r["is_strict_t_plus_n"] is False
    assert "not strict historical T+N" in r["warning"]
    print(f"✅ mode={r['backtest_mode']} strict={r['is_strict_t_plus_n']}")


def test_z9_current_price_proxy_does_not_auto_adjust_weights():
    """CURRENT_PRICE_PROXY never calls adjust_weights()"""
    from hermes.Z9_Calibration_Engine import Z9CalibrationEngine
    engine = Z9CalibrationEngine()

    engine.db["predictions"] = [
        {"ticker": "600519", "name": "茅台", "predicted_price": 100,
         "action": "WATCH", "scoring_weights": {"FQS": 0.2, "ISS": 0.15},
         "date": "2026-05-15", "target_days": 5}
    ] * 60
    engine.db["calibration_log"] = [
        {"cal_count": i, "calibrated_at": "2026-05-15T00:00:00",
         "backtest_mode": "CURRENT_PRICE_PROXY", "is_strict_t_plus_n": False}
        for i in range(1, 5)
    ]
    engine._save_db = lambda: None
    called = {"adjust": False}
    engine.adjust_weights = lambda: called.__setitem__("adjust", True) or {}

    r = engine.backtest_at(days=5, live_prices={
        "600519": {"price": 110, "pct": 10.0, "name": "贵州茅台"},
    })

    assert called["adjust"] is False, "adjust_weights was called despite CURRENT_PRICE_PROXY"
    assert r["weight_adjustment"]["status"] == "SKIPPED"
    assert r["auto_adjust_skipped"]["reason"] == "NOT_STRICT_T_PLUS_N_OR_MIN_SAMPLE_NOT_MET"
    assert r["auto_adjust_skipped"]["backtest_mode"] == "CURRENT_PRICE_PROXY"
    print(f"✅ auto_adjust blocked: {r['auto_adjust_skipped']['reason']}")


if __name__ == "__main__":
    test_z9_current_price_proxy_not_strict_t_plus_n()
    test_z9_current_price_proxy_does_not_auto_adjust_weights()
    print("\n🏁 Z9 calibration contract tests PASS")
