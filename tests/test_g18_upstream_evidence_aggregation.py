"""G18 upstream evidence aggregation tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_aggregator_defaults_missing_sources():
    from zmatrix.prediction.upstream_evidence_aggregator import build_upstream_evidence
    r = build_upstream_evidence("002472", g09_signal={"available": True, "status": "PASS"})
    for s in ["g08", "g11", "g14", "z16", "g17"]:
        assert s in r["missing_sources"], f"{s} not in missing"
    assert r["evidence_available"]["g09"] is True
    print(f"✅ missing: {len(r['missing_sources'])} sources")

def test_g11_warning_only_contract():
    from zmatrix.prediction.upstream_evidence_aggregator import build_upstream_evidence
    from zmatrix.prediction.adapters.g11_risk_adapter import load_g11_signal
    r = build_upstream_evidence("002472", g11_signal=load_g11_signal())
    assert r["g11"]["hard_veto_allowed"] is False
    assert r["g11"]["risk_authority"] == "STRONG_WARNING_ONLY"
    print("✅ G11: STRONG_WARNING_ONLY, no hard veto")

def test_z16_g17_placeholder_not_trade():
    from zmatrix.prediction.upstream_evidence_aggregator import build_upstream_evidence
    from zmatrix.prediction.adapters.z16_price_gate_adapter import load_z16_signal
    from zmatrix.prediction.adapters.g17_account_confirm_adapter import load_g17_signal
    r = build_upstream_evidence("002472", z16_signal=load_z16_signal(), g17_signal=load_g17_signal())
    assert r["z16"]["status"] == "PLACEHOLDER_NOT_CONNECTED"
    assert r["g17"]["status"] == "PLACEHOLDER_NOT_CONNECTED"
    assert r["z16"]["required"] is True
    assert r["g17"]["required"] is True
    for bad in ["BUY", "SELL", "AUTO_TRADE"]:
        assert bad not in str(r["z16"]), f"z16 leaked {bad}"
        assert bad not in str(r["g17"]), f"g17 leaked {bad}"
    print("✅ Z16/G17: placeholder, required, no trade")

def test_final_decision_provenance_contains_z16_g17():
    from zmatrix.prediction.final_decision_envelope import build_final_decision
    from zmatrix.prediction.contracts import PredictionResult
    p = PredictionResult(ticker="002472", probability=0.75, action_proposal="WAIT")
    upstream = {"g09": {"available": True, "hard_blocks": []}, "g08": {}, "g11": {},
                "g14": {}, "z16": {"required": True, "status": "PLACEHOLDER"}, "g17": {"required": True, "status": "PLACEHOLDER"}}
    r = build_final_decision(p, upstream)
    assert "z16" in r["provenance"]
    assert "g17" in r["provenance"]
    print("✅ provenance: z16+g17 present")

if __name__ == "__main__":
    test_aggregator_defaults_missing_sources()
    test_g11_warning_only_contract()
    test_z16_g17_placeholder_not_trade()
    test_final_decision_provenance_contains_z16_g17()
    print("\n🏁 G18 upstream evidence aggregation tests PASS")
