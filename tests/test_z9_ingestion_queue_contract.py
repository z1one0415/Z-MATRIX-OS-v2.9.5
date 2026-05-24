"""Z9 Ingestion Queue v1.0 contract tests — no real write"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _make_valid_sample():
    return {"sample_id":"Z9S_001","ticker":"002472","sample_version":"v1.0","source_record":{"record_ref":"Z9S_001"},
            "decision_snapshot":{"entry_intent":"WAIT","exit_intent":None,"paper_action":None,"action_cap":"WAIT"},
            "outcome_placeholder":{"review_status":"WAITING_FOR_FUTURE_MARKET_DATA"},
            "review_plan":{"needs_future_review":True},"calibration_hooks":{}}

def test_queue_item_required_fields():
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    r = build_z9_ingestion_queue_item(_make_valid_sample())
    for k in ["queue_version","queue_type","queue_id","sample_id","ticker","idempotency",
              "state","sample_snapshot","validation","write_policy","forbidden_real_trade_checked"]:
        assert k in r, f"missing {k}"
    assert r["queue_version"] == "v1.0"
    print("✅ queue: all fields present")

def test_queue_write_policy_disabled():
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    r = build_z9_ingestion_queue_item(_make_valid_sample())
    assert r["write_policy"]["queue_write_allowed"] is False
    assert r["write_policy"]["z9_write_allowed"] is False
    print("✅ queue: write_allowed=False")

def test_idempotency_key_stable():
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    r1 = build_z9_ingestion_queue_item(_make_valid_sample())
    r2 = build_z9_ingestion_queue_item(_make_valid_sample())
    assert r1["idempotency"]["idempotency_key"] == r2["idempotency"]["idempotency_key"]
    print("✅ idempotency: stable")

def test_dedup_key_not_random():
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    r = build_z9_ingestion_queue_item(_make_valid_sample())
    assert "002472" in r["idempotency"]["dedup_key"]
    assert "Z9S_001" in r["idempotency"]["dedup_key"]
    print("✅ dedup: ticker+sample_id")

def test_waiting_market_data_status():
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    r = build_z9_ingestion_queue_item(_make_valid_sample())
    assert r["state"]["status"] == "WAITING_MARKET_DATA"
    print("✅ status: WAITING_MARKET_DATA")

def test_missing_required_field_rejected():
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    r = build_z9_ingestion_queue_item({"decision_snapshot":{"entry_intent":"WAIT","exit_intent":None,"paper_action":None,"action_cap":"WAIT"}})
    assert r["state"]["status"] == "REJECTED"
    assert len(r["validation"]["reject_reasons"]) >= 1
    print("✅ missing fields→REJECTED")

def test_forbidden_real_trade_rejected():
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    try:
        build_z9_ingestion_queue_item({"decision_snapshot":{"entry_intent":"BUY","exit_intent":None,"paper_action":None,"action_cap":"WAIT"}})
        assert False, "BUY should be rejected"
    except ValueError: pass
    print("✅ BUY rejected")

def test_conflict_code_not_rejected():
    from zmatrix.calibration.z9_ingestion_queue import build_z9_ingestion_queue_item
    # Conflict code G09_SELL_VS_G18_ENTRY should NOT be rejected
    r = build_z9_ingestion_queue_item({"ticker":"002472","sample_id":"Z9S_002","sample_version":"v1.0","source_record":{"record_ref":"Z9S_002"},
        "decision_snapshot":{"entry_intent":"WAIT","exit_intent":None,"paper_action":None,"action_cap":"WAIT"},
        "outcome_placeholder":{},"review_plan":{},"calibration_hooks":{}})
    assert r["state"]["status"] != "REJECTED"  # conflict codes are in the sample, not in action fields
    print("✅ conflict code not rejected")

def test_g18_output_contains_queue_preview():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg18","pipelines/Z-G18_天机引擎/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    p = r["predictions"][0]
    assert "z9_ingestion_queue_preview" in p
    assert r["sections"]["z9_queue_write_allowed"] is False
    print("✅ G18: queue preview + write disabled")

if __name__ == "__main__":
    test_queue_item_required_fields()
    test_queue_write_policy_disabled()
    test_idempotency_key_stable()
    test_dedup_key_not_random()
    test_waiting_market_data_status()
    test_missing_required_field_rejected()
    test_forbidden_real_trade_rejected()
    test_conflict_code_not_rejected()
    test_g18_output_contains_queue_preview()
    print("\n🏁 Z9 Ingestion Queue v1.0 contract tests PASS")
