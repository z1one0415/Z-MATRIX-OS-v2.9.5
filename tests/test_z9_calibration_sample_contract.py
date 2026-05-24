"""Z9 Calibration Sample v1.0 contract freeze tests — no real Z9 write"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_z9_sample_required_fields():
    from zmatrix.calibration.z9_calibration_sample import build_z9_calibration_sample
    rec = {"ticker":"002472","name":"test","paper_execution":{"entry_intent":"WAIT","exit_intent":None,"paper_action":None,"action_cap":"WAIT","required_confirmations":[]},"final_decision":{},"conflict_summary":{},"upstream_evidence_available":{},"missing_sources":[],"prediction":{}}
    r = build_z9_calibration_sample(rec)
    for k in ["sample_version","sample_type","sample_id","run_id","ticker","source_record",
              "prediction_snapshot","decision_snapshot","evidence_snapshot","review_plan",
              "outcome_placeholder","calibration_hooks","z9_write_policy","forbidden_real_trade_checked"]:
        assert k in r, f"missing {k}"
    assert r["sample_version"] == "v1.0"
    print("✅ z9 sample: all fields present")

def test_z9_sample_write_policy_disabled():
    from zmatrix.calibration.z9_calibration_sample import build_z9_calibration_sample
    r = build_z9_calibration_sample({"ticker":"002472","paper_execution":{"entry_intent":"WAIT","exit_intent":None,"paper_action":None,"action_cap":"WAIT","required_confirmations":[]},"final_decision":{},"conflict_summary":{},"upstream_evidence_available":{},"missing_sources":[],"prediction":{}})
    assert r["z9_write_policy"]["write_allowed"] is False
    assert "DEFERRED_NOT_CONNECTED" in r["z9_write_policy"]["write_status"]
    print("✅ z9 write: write_allowed=False")

def test_z9_sample_outcome_placeholders_pending():
    from zmatrix.calibration.z9_calibration_sample import build_z9_calibration_sample
    r = build_z9_calibration_sample({"ticker":"002472","paper_execution":{"entry_intent":"WAIT","exit_intent":None,"paper_action":None,"action_cap":"WAIT","required_confirmations":[]},"final_decision":{},"conflict_summary":{},"upstream_evidence_available":{},"missing_sources":[],"prediction":{}})
    for k in ["actual_return_T1","actual_return_T5","actual_return_T20"]:
        assert r["outcome_placeholder"][k] is None, f"{k} should be None"
    assert r["outcome_placeholder"]["decision_outcome"] == "PENDING_REVIEW"
    print("✅ outcome placeholders: pending")

def test_z9_sample_forbidden_real_trade_rejected():
    from zmatrix.calibration.z9_calibration_sample import build_z9_calibration_sample
    rec = {"ticker":"002472","paper_execution":{"entry_intent":"BUY","exit_intent":None,"paper_action":None,"action_cap":"WAIT","required_confirmations":[]},"final_decision":{},"conflict_summary":{},"upstream_evidence_available":{},"missing_sources":[],"prediction":{}}
    try:
        build_z9_calibration_sample(rec)
        assert False, "BUY should be rejected"
    except ValueError: pass
    print("✅ z9: BUY rejected")

def test_g18_output_contains_z9_calibration_sample_preview():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    p = r["predictions"][0]
    assert "z9_calibration_sample_preview" in p
    assert r["sections"]["z9_real_write_allowed"] is False
    assert r["sections"]["z9_write_status"] == "DEFERRED_NOT_CONNECTED"
    print("✅ G18: z9_calibration_sample_preview + write disabled")

if __name__ == "__main__":
    test_z9_sample_required_fields()
    test_z9_sample_write_policy_disabled()
    test_z9_sample_outcome_placeholders_pending()
    test_z9_sample_forbidden_real_trade_rejected()
    print("\n🏁 Z9 Calibration Sample contract tests PASS")
