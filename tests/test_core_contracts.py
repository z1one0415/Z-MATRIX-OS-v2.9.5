"""v2.9.5-RC behavior contract tests — 行为契约验证 (非run()存在检查)"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PAUSED = "SKIP"

def test_zg16_lite_when_missing_world_or_l15():
    """Z-G16 Lite: missing world or L1.5→Lite mode, no price_zones, no PAPER_PROBE action"""
    spec = importlib.util.spec_from_file_location("zg16","pipelines/Z-G16_纸面验证/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    r = mod.run({"symbol":"002463","name":"测试","selected_role":"R_MATRIX",
        "action_proposal":{"action":"PAPER_TRACK"},"price":100,  # missing world, l1_5
    })
    assert r.get("mode") == "Lite", f"Expected Lite, got {r.get('mode')}"
    assert r.get("forbidden_fields") is not None, "Lite must have forbidden_fields"
    assert "PAPER_PROBE" in r.get("forbidden_fields",[]), "PAPER_PROBE must be forbidden in Lite"
    assert "coach_plan" not in r or "price_zones" not in r.get("coach_plan",{}), "Lite must not have price_zones"
    print("✅ test_zg16_lite_when_missing_world_or_l15")

def test_zg16_full_no_default_paper_probe_action():
    """Z-G16 Full: PAPER_PROBE only in conditional_outputs, not as default action"""
    spec = importlib.util.spec_from_file_location("zg16","pipelines/Z-G16_纸面验证/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    r = mod.run({"symbol":"002463","name":"测试","selected_role":"R_MATRIX",
        "action_proposal":{"action":"PAPER_TRACK"},"price":102.6,
        "world":"PAPER_WORLD","l1_5_status":"SAFE","operating_mode":"NORMAL","hibernation_no_attack":False
    })
    # Verify no PAPER_PROBE as default action in either Full or Lite mode
    coach = r.get("coach_plan",{})
    if coach:
        for route in coach.get("scenario_routes",[]):
            assert route.get("action") != "PAPER_PROBE", f"PAPER_PROBE found as action in route: {route}"
        for step in coach.get("position_playbook",{}).get("steps",[]):
            assert step.get("action") != "PAPER_PROBE", f"PAPER_PROBE found as action in step: {step}"
    # Lite: verify forbidden_fields contains PAPER_PROBE
    if r.get("mode") == "Lite":
        assert "PAPER_PROBE" in r.get("forbidden_fields",[]), "Lite must forbid PAPER_PROBE"
    # Full: verify capability_mask has PAPER_PROBE as conditional
    if r.get("mode") == "Full" or r.get("capability_mask"):
        cm = r.get("capability_mask",{}) or {}
        cond = cm.get("conditional_outputs",[])
        if cond:
            assert any(c.get("output")=="PAPER_PROBE" for c in cond), "Full mode conditional_outputs must contain PAPER_PROBE"
    print("✅ test_zg16_full_no_default_paper_probe_action")

def test_zg16a_missing_fill_fields_no_fill():
    """Z-G16A: missing fill fields→NO_FILL, no position"""
    spec = importlib.util.spec_from_file_location("zg16a","pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    # Test resolve_fill_quality directly with missing defaults (fail-closed)
    r = mod.resolve_fill_quality("BLOCK","unknown","unknown","unknown",False,100)
    assert r["fill_quality"] == "NO_FILL", f"Expected NO_FILL, got {r['fill_quality']}"
    assert r["fill_price"] is None, f"NO_FILL must have fill_price=None, got {r['fill_price']}"
    assert r["attribution_allowed"] == False
    print("✅ test_zg16a_missing_fill_fields_no_fill")

def test_zg16a_mt_block_no_fill():
    """Z-G16A: MT BLOCK→NO_FILL regardless of other fields"""
    spec = importlib.util.spec_from_file_location("zg16a","pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    r = mod.resolve_fill_quality("BLOCK","raw_unadjusted","execution_quote","primary",True,100)
    assert r["fill_quality"] == "NO_FILL", f"MT BLOCK must be NO_FILL, got {r['fill_quality']}"
    assert r["fill_price"] is None
    print("✅ test_zg16a_mt_block_no_fill")

def test_zg16a_degraded_fill_no_attribution():
    """Z-G16A: DEGRADED_FILL→attribution_allowed=False"""
    spec = importlib.util.spec_from_file_location("zg16a","pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    r = mod.resolve_fill_quality("DEGRADED","raw_unadjusted","realtime_research","raw_fallback",True,100)
    assert r["fill_quality"] == "DEGRADED_FILL", f"Expected DEGRADED_FILL, got {r['fill_quality']}"
    assert r["attribution_allowed"] == False, "DEGRADED_FILL must have attribution_allowed=False"
    assert r["fill_price"] is not None, "DEGRADED_FILL should have fill_price"
    assert "DIRECTIONAL_ALPHA_ONLY" in r["reason_codes"]
    print("✅ test_zg16a_degraded_fill_no_attribution")

def test_zg16a_high_confidence_fill():
    """Z-G16A: full credentials→HIGH_CONFIDENCE_FILL"""
    spec = importlib.util.spec_from_file_location("zg16a","pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    r = mod.resolve_fill_quality("PASS","raw_unadjusted","execution_quote","primary",True,100)
    assert r["fill_quality"] == "HIGH_CONFIDENCE_FILL"
    assert r["attribution_allowed"] == True
    assert r["fill_price"] == 100.15  # 100 * 1.0015
    print("✅ test_zg16a_high_confidence_fill")



def test_zg16a_run_missing_fill_fields_created_no_fill():
    """Z-G16A run: missing fill fields→CREATED_NO_FILL, position=None"""
    spec = importlib.util.spec_from_file_location("zg16a","pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    r = mod.run({"validation_id":"test","validation_hypothesis":"PCB验证","ghost_benchmark":"512480",
        "planned_horizon_days":30,"invalidation_conditions":["跌破MA60"],"primary_role":"R_MATRIX",
        "entry_price":100})
    assert r["plan_status"] == "CREATED_NO_FILL", f"Expected CREATED_NO_FILL, got {r['plan_status']}"
    assert r.get("position") is None, "position must be None on NO_FILL"
    assert r["fill_quality"]["fill_quality"] == "NO_FILL"
    print("✅ test_zg16a_run_missing_fill_fields_created_no_fill")

def test_zg16a_run_degraded_fill_position_metadata():
    """Z-G16A run: DEGRADED_FILL→position with correct metadata"""
    spec = importlib.util.spec_from_file_location("zg16a","pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    r = mod.run({"validation_id":"test","validation_hypothesis":"PCB验证","ghost_benchmark":"512480",
        "planned_horizon_days":30,"invalidation_conditions":["跌破MA60"],"primary_role":"R_MATRIX",
        "entry_price":100,"market_truth_status":"DEGRADED","price_basis":"raw_unadjusted",
        "quote_domain":"realtime_research","quote_role":"raw_fallback","ttl_valid":True})
    
    assert r.get("position") is not None, "position must exist for DEGRADED_FILL"
    assert r["position"]["fill_quality"] == "DEGRADED_FILL"
    assert r["position"]["attribution_allowed"] is False, "DEGRADED must have attribution_allowed=False"
    assert r["fill_quality"]["fill_confidence"] == "degraded"
    print("✅ test_zg16a_run_degraded_fill_position_metadata")

def test_zg16a_run_high_confidence_no_nameerror():
    """Z-G16A run: HIGH_CONFIDENCE_FILL→correct fill_price + no NameError"""
    spec = importlib.util.spec_from_file_location("zg16a","pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    r = mod.run({"validation_id":"test","validation_hypothesis":"PCB验证","ghost_benchmark":"512480",
        "planned_horizon_days":30,"invalidation_conditions":["跌破MA60"],"primary_role":"R_MATRIX",
        "entry_price":100,"market_truth_status":"PASS","price_basis":"raw_unadjusted",
        "quote_domain":"execution_quote","quote_role":"primary","ttl_valid":True})
    
    assert r.get("position") is not None
    assert r["position"]["fill_quality"] == "HIGH_CONFIDENCE_FILL"
    assert r["position"]["attribution_allowed"] is True
    assert r["position"]["fill_price"] == 100.15
    assert r["fill_quality"]["fill_quality"] == "HIGH_CONFIDENCE_FILL"
    print("✅ test_zg16a_run_high_confidence_no_nameerror")

if __name__ == "__main__":
    results = []
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                results.append((name, "PASS"))
            except AssertionError as e:
                results.append((name, f"FAIL: {e}"))
                print(f"❌ {name}: {e}")
            except Exception as e:
                results.append((name, f"ERROR: {e}"))
                print(f"💥 {name}: {e}")
    
    passed = sum(1 for _, r in results if r == "PASS")
    total = len(results)
    print(f"\n🏁 {passed}/{total} PASS")
    if passed < total:
        sys.exit(1)
