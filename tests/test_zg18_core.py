"""Z-G18 Tianji engine invariant tests — P0/P1 hardened"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_sigmoid_shield():
    from zmatrix.prediction.probability_model import fermi_weighted
    r = fermi_weighted(raw_score=20, coverage_adj=1.0, risk_penalty=0.5)
    assert r["probability"] <= 0.50
    print(f"✅ sigmoid: prob={r['probability']:.3f}")


def test_coverage_after_sigmoid():
    from zmatrix.prediction.probability_model import fermi_weighted
    r = fermi_weighted(raw_score=10, coverage_adj=0.3)
    assert r["probability"] < 0.40
    print(f"✅ coverage after sigmoid: prob={r['probability']:.3f}")


def test_no_trade_actions():
    from zmatrix.prediction.contracts import PredictionResult, FORBIDDEN_ACTIONS, ALLOWED_ACTIONS
    for f in ["BUY", "SELL", "PAPER_PROBE", "AUTO_TRADE"]:
        try: PredictionResult(ticker="000", action_proposal=f).validate_action(); assert False
        except ValueError: pass
    assert "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17" in ALLOWED_ACTIONS
    print("✅ no trade actions")


def test_lineage_cap():
    from zmatrix.prediction.data_lineage import evaluate_lineage, apply_lineage_cap
    r = evaluate_lineage({"market_data":"DAILY_OHLCV_PROXY","trust":"MEDIUM"})
    assert apply_lineage_cap(0.90, r) <= 0.75
    r2 = evaluate_lineage({"upstream_status":"DATA_GAP","trust":"LOW"})
    assert r2["probability_cap"] <= 0.60
    print(f"✅ lineage cap: proxy≤{r['probability_cap']} gap≤{r2['probability_cap']}")


def test_missing_lineage_degrades():
    from zmatrix.prediction.data_lineage import evaluate_lineage
    assert evaluate_lineage(None)["trust"] == "LOW"
    r = evaluate_lineage({"market_data":"PASS","m1":False,"l2":False,"upstream_status":"PASS","trust":"HIGH"})
    assert r["confidence_cap"] == "MEDIUM"
    print("✅ m1/l2 false→MEDIUM, missing→LOW")


def test_temporal_anchor():
    from zmatrix.prediction.temporal_calibrator import evaluate_temporal_consistency
    import json
    r = evaluate_temporal_consistency(0.52, 0.85, 0.40)
    assert r["action_cap"] == "WAIT_CONFIRM"
    assert "NEXT_AUCTION_WEAK_TO_STRONG" in json.dumps(r)
    print("✅ T5=0.85+T1=0.52→WAIT_CONFIRM")


def test_auto_weight_freeze():
    import tempfile, json, os
    from zmatrix.prediction.event_store import PredictionEventStore, ConfigurationLockedError
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"predictions":[],"calibration_log":[],"resolved_samples":[]}, f); db_path = f.name
    try:
        store = PredictionEventStore(db_path=db_path)
        try: store.adjust_weights(); assert False
        except ConfigurationLockedError: pass
    finally: os.unlink(db_path)
    print("✅ weight freeze: 0/50→ConfigurationLockedError")


def test_normalize_missing_lineage():
    from zmatrix.prediction.data_lineage import normalize_upstream_lineage
    assert normalize_upstream_lineage({"ticker":"002472","score":80})["upstream_status"] == "DEGRADED_MISSING_LINEAGE"
    print("✅ missing lineage→DEGRADED")


def test_z9_auto_adjust_always_false():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for p in mod.run(tickers=["002472"])["predictions"]:
        assert p["z9"]["auto_adjust_allowed"] is False
    print("✅ z9 auto_adjust_allowed=False")


def test_horizon_clamped_to_lineage_cap():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for p in mod.run(tickers=["002472"])["predictions"]:
        cap = p["data_lineage"]["probability_cap"]
        for h in ["T1","T5","T20"]: assert 0.0 <= p["horizon"][h] <= cap
    print("✅ horizons clamped")


def test_zg18_sections_auto_adjust_always_false():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    assert r["sections"]["auto_adjust_allowed"] is False
    print("✅ sections auto_adjust locked")


def test_zg18_top_level_data_lineage_not_empty():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    assert r["data_lineage"] is not None
    assert "global_data_precision" in r["data_lineage"]
    assert r["data_lineage"]["m1_connected"] is False
    print(f"✅ top-level data_lineage: {r['data_lineage']['global_data_precision']}")


def test_zg18_z9_write_status_is_deferred():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    assert r["sections"]["z9_samples_written"] == 0
    assert r["sections"]["z9_write_status"] == "DEFERRED_NOT_CONNECTED"
    assert r["sections"]["z9_prediction_samples_ready"] == len(r["predictions"])
    print(f"✅ z9: ready={r['sections']['z9_prediction_samples_ready']} written=0")


if __name__ == "__main__":
    test_sigmoid_shield()
    test_coverage_after_sigmoid()
    test_no_trade_actions()
    test_lineage_cap()
    test_missing_lineage_degrades()
    test_temporal_anchor()
    test_auto_weight_freeze()
    test_normalize_missing_lineage()
    test_z9_auto_adjust_always_false()
    test_horizon_clamped_to_lineage_cap()
    test_zg18_sections_auto_adjust_always_false()
    test_zg18_top_level_data_lineage_not_empty()
    test_zg18_z9_write_status_is_deferred()
    print("\n🏁 Z-G18 Tianji engine tests PASS (P0/P1 hardened)")
