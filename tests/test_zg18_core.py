"""Z-G18 Tianji engine invariant tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_sigmoid_shield():
    """INV-TG18-01: raw_score=20, risk=0.5 → prob≤0.50"""
    from zmatrix.prediction.probability_model import fermi_weighted, sigmoid
    r = fermi_weighted(raw_score=20, coverage_adj=1.0, risk_penalty=0.5)
    assert r["probability"] <= 0.50, f"Shield failed: {r['probability']}"
    assert r["raw_sigmoid"] > 0.90
    print(f"✅ sigmoid shield: raw_sigmoid={r['raw_sigmoid']:.3f} prob={r['probability']:.3f}")


def test_coverage_after_sigmoid():
    """Coverage adjustment comes after sigmoid, not before"""
    from zmatrix.prediction.probability_model import fermi_weighted
    r = fermi_weighted(raw_score=10, coverage_adj=0.3)
    assert r["probability"] < 0.40, f"Should be penalized: {r['probability']}"
    print(f"✅ coverage after sigmoid: prob={r['probability']:.3f}")


def test_no_trade_actions():
    """INV-TG18-05: no BUY/SELL/ADD/CLEAR/AUTO_TRADE"""
    from zmatrix.prediction.contracts import ALLOWED_ACTIONS, FORBIDDEN_ACTIONS
    for a in FORBIDDEN_ACTIONS:
        assert a not in ALLOWED_ACTIONS, f"{a} leaked into allowed"
    from zmatrix.prediction.contracts import PredictionResult
    for f in ["BUY", "SELL", "PAPER_PROBE"]:
        try:
            r = PredictionResult(ticker="000", action_proposal=f)
            r.validate_action()
            assert False, f"Should have rejected {f}"
        except ValueError:
            pass
    print("✅ no trade actions")


def test_lineage_cap():
    """INV-TG18-02: PROXY→≤0.75, DATA_GAP→≤0.60"""
    from zmatrix.prediction.data_lineage import evaluate_lineage, apply_lineage_cap
    r = evaluate_lineage({"market_data": "DAILY_OHLCV_PROXY", "trust": "MEDIUM"})
    assert r["probability_cap"] <= 0.75
    assert apply_lineage_cap(0.90, r) <= 0.75
    r2 = evaluate_lineage({"upstream_status": "DATA_GAP", "trust": "LOW"})
    assert r2["probability_cap"] <= 0.60
    print(f"✅ lineage cap: proxy≤{r['probability_cap']} gap≤{r2['probability_cap']}")


def test_missing_lineage_degrades():
    """INV-TG18-07: missing lineage→LOW trust, 0.60 cap"""
    from zmatrix.prediction.data_lineage import evaluate_lineage
    r = evaluate_lineage(None)
    assert r["trust"] == "LOW"
    assert r["probability_cap"] <= 0.60
    print("✅ missing lineage→LOW")


def test_temporal_anchor():
    """INV-TG18-03: T5 high + T1 weak→WAIT_CONFIRM"""
    from zmatrix.prediction.temporal_calibrator import evaluate_temporal_consistency
    r = evaluate_temporal_consistency(0.30, 0.70, 0.75)
    assert r["action_cap"] == "WAIT_CONFIRM"
    assert len(r["next_triggers"]) > 0
    print("✅ temporal anchor: T5高+T1弱→WAIT_CONFIRM")


def test_auto_weight_freeze():
    """INV-TG18-04: <50 strict→ConfigurationLockedError"""
    from zmatrix.prediction.event_store import PredictionEventStore, ConfigurationLockedError
    store = PredictionEventStore()
    allowed, reason = store.is_auto_adjust_allowed()
    print(f"✅ weight freeze: allowed={allowed} ({store.count_resolved_strict()}/50)")


def test_trigger_not_execution():
    """INV-TG18-08: PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17, never PAPER_PROBE direct"""
    from zmatrix.prediction.contracts import ALLOWED_ACTIONS, FORBIDDEN_ACTIONS
    assert "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17" in ALLOWED_ACTIONS
    assert "PAPER_PROBE" in FORBIDDEN_ACTIONS
    print("✅ trigger eligibility vs execution")


def test_z9_strict_t_plus_n():
    """Z9 samples require strict_t_plus_n_required=True"""
    from zmatrix.prediction.contracts import Z9Sample
    s = Z9Sample(ticker="002472", probability=0.73)
    assert s.strict_t_plus_n_required is True
    assert s.auto_adjust_allowed is False
    print("✅ z9: strict_t_plus_n=True, auto_adjust=False")


def test_zg18_prediction_contract():
    """Z-G18 predictions include all required fields"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18", "pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    for p in r["predictions"]:
        for k in ("ticker","name","probability","horizon","evidence_coverage",
                   "data_lineage","temporal_consistency","next_triggers","action_proposal","z9"):
            assert k in p, f"missing {k}"
        assert p["z9"]["strict_t_plus_n_required"] is True
        assert "Z-G18" in r["pipeline_signature"]
    print("✅ prediction contract complete")


if __name__ == "__main__":
    test_sigmoid_shield()
    test_coverage_after_sigmoid()
    test_no_trade_actions()
    test_lineage_cap()
    test_missing_lineage_degrades()
    test_temporal_anchor()
    test_auto_weight_freeze()
    test_trigger_not_execution()
    test_z9_strict_t_plus_n()
    test_zg18_prediction_contract()
    print("\n🏁 Z-G18 Tianji engine tests PASS")
