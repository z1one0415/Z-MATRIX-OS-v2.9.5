"""Z-G18 Tianji engine invariant tests — P0/P1 hardened"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_sigmoid_shield():
    """INV-TG18-01: raw=20, risk_penalty=0.5(multiplicative) → prob≤0.50"""
    from zmatrix.prediction.probability_model import fermi_weighted
    r = fermi_weighted(raw_score=20, coverage_adj=1.0, risk_penalty=0.5)
    assert r["probability"] <= 0.50, f"Shield failed: {r['probability']}"
    assert r["raw_sigmoid"] > 0.90
    print(f"✅ sigmoid: raw={r['raw_sigmoid']:.3f} prob={r['probability']:.3f}")


def test_coverage_after_sigmoid():
    from zmatrix.prediction.probability_model import fermi_weighted
    r = fermi_weighted(raw_score=10, coverage_adj=0.3)
    assert r["probability"] < 0.40
    print(f"✅ coverage after sigmoid: prob={r['probability']:.3f}")


def test_no_trade_actions():
    """INV-TG18-05: BUY/SELL/PAPER_PROBE/AUTO_TRADE forbidden"""
    from zmatrix.prediction.contracts import PredictionResult, FORBIDDEN_ACTIONS, ALLOWED_ACTIONS
    for f in ["BUY", "SELL", "PAPER_PROBE", "AUTO_TRADE"]:
        try:
            PredictionResult(ticker="000", action_proposal=f).validate_action()
            assert False, f"Should reject {f}"
        except ValueError: pass
    assert "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17" in ALLOWED_ACTIONS
    assert "PAPER_PROBE" in FORBIDDEN_ACTIONS
    print("✅ no trade actions")


def test_lineage_cap():
    """INV-TG18-02: PROXY≤0.75, DATA_GAP≤0.60"""
    from zmatrix.prediction.data_lineage import evaluate_lineage, apply_lineage_cap
    r = evaluate_lineage({"market_data":"DAILY_OHLCV_PROXY","trust":"MEDIUM"})
    assert r["probability_cap"] <= 0.75
    assert apply_lineage_cap(0.90, r) <= 0.75
    r2 = evaluate_lineage({"upstream_status":"DATA_GAP","trust":"LOW"})
    assert r2["probability_cap"] <= 0.60
    print(f"✅ lineage cap: proxy≤{r['probability_cap']} gap≤{r2['probability_cap']}")


def test_missing_lineage_degrades():
    """INV-TG18-07: None→LOW+0.60; m1/l2 false→MEDIUM"""
    from zmatrix.prediction.data_lineage import evaluate_lineage
    r = evaluate_lineage(None)
    assert r["trust"] == "LOW"
    assert r["probability_cap"] <= 0.60
    r2 = evaluate_lineage({"market_data":"PASS","intraday":"PASS","m1":False,"l2":False,"upstream_status":"PASS","trust":"HIGH"})
    assert r2["confidence_cap"] == "MEDIUM"
    assert r2["probability_cap"] <= 0.75
    print("✅ m1/l2 false→MEDIUM, missing→LOW")


def test_temporal_anchor():
    """INV-TG18-03: T1=0.52, T5=0.85, T20=0.40 → WAIT_CONFIRM (Event Window)"""
    from zmatrix.prediction.temporal_calibrator import evaluate_temporal_consistency
    r = evaluate_temporal_consistency(0.52, 0.85, 0.40)
    assert r["action_cap"] == "WAIT_CONFIRM"
    assert len(r["next_triggers"]) > 0
    import json
    assert "NEXT_AUCTION_WEAK_TO_STRONG" in json.dumps(r)
    print("✅ T5=0.85+T1=0.52→WAIT_CONFIRM (Event Window)")


def test_auto_weight_freeze():
    """INV-TG18-04: adjust_weights() throws when <50 strict"""
    from zmatrix.prediction.event_store import PredictionEventStore, ConfigurationLockedError
    store = PredictionEventStore()
    try:
        store.adjust_weights()
        assert store.count_resolved_strict() >= 50, "Should have thrown"
    except ConfigurationLockedError:
        pass
    print(f"✅ weight freeze: adjust_weights blocked ({store.count_resolved_strict()}/50 strict)")


def test_normalize_missing_lineage():
    """INV-TG18-07: upstream without data_provenance_mask → DEGRADED"""
    from zmatrix.prediction.data_lineage import normalize_upstream_lineage
    r = normalize_upstream_lineage({"ticker":"002472","score":80})
    assert r["upstream_status"] == "DEGRADED_MISSING_LINEAGE"
    print("✅ missing lineage→DEGRADED_MISSING_LINEAGE")


def test_z9_auto_adjust_always_false():
    """P0-1: Z-G18 never sets auto_adjust_allowed=True"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    for p in r["predictions"]:
        assert p["z9"]["auto_adjust_allowed"] is False, f"Z-G18 leaked True"
        assert "SAMPLE_ONLY" in p["z9"]["auto_adjust_reason"] or "FORBIDDEN" in p["z9"]["auto_adjust_reason"]
        assert p["z9"]["strict_t_plus_n_required"] is True
    print("✅ z9 auto_adjust_allowed=False in all predictions")


def test_horizon_clamped_to_lineage_cap():
    """P0-3: T1/T5/T20 never exceed probability_cap"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    for p in r["predictions"]:
        cap = p["data_lineage"]["probability_cap"]
        for h in ["T1","T5","T20"]:
            v = p["horizon"][h]
            assert 0.0 <= v <= cap, f"{h}={v} exceeds cap={cap}"
    print("✅ all horizons clamped to lineage cap")



def test_zg18_sections_auto_adjust_always_false():
    import importlib.util
    spec = importlib.util.spec_from_file_location('zg18','pipelines/Z-G18_天机引擎/gate_pipeline.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=['002472'])
    assert r['sections']['auto_adjust_allowed'] is False
    assert 'SAMPLE_ONLY' in r['sections']['auto_adjust_reason'] or 'FORBIDDEN' in r['sections']['auto_adjust_reason']
    print(f"✅ sections auto_adjust_allowed=False: {r['sections']['auto_adjust_reason']}")

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
    print("\n🏁 Z-G18 Tianji engine tests PASS (P0/P1 hardened)")
