"""V13.F5.1.2 — Batch3 interface backfill tests."""
import json, glob
from pathlib import Path
ROOT = Path("research/factor_library")
FACTORS = ["F21","F22","F24","F26","F27","F30","F31","F34"]
REQUIRED_ARTIFACTS = ["factor_manifest.json","validation_snapshot.json","guardrail_profile.json","application_contract.json","evidence_envelope.json"]
SCHEMA_FIELDS = ["pipeline_signature","factor_id","factor_name","alpha_claim_allowed","production","broker_runtime","real_trade"]

# ---- 1. All 8 factors have 5 artifacts ----
def test_8_factors_all_have_5_artifacts():
    for fid in FACTORS:
        for art in REQUIRED_ARTIFACTS:
            p = ROOT / "factors" / fid / art
            assert p.exists(), f"Missing: {p}"

# ---- 2. Schema field presence ----
def test_all_manifests_have_required_fields():
    for fid in FACTORS:
        m = json.loads((ROOT / "factors" / fid / "factor_manifest.json").read_text())
        for f in ["interface_version","factor_id","factor_name","factor_family_id","factor_type","formula_ref","asof_policy","horizon_policy","ready_for_candidate_review","ready_for_promotion_review","promotion_allowed","alpha_claim_allowed","production","broker_runtime","real_trade"]:
            assert f in m, f"{fid} manifest missing: {f}"

def test_all_validation_snapshots_have_required_fields():
    for fid in FACTORS:
        v = json.loads((ROOT / "factors" / fid / "validation_snapshot.json").read_text())
        for f in ["factor_id","coverage_passed","pit_passed","single_factor_validation_executed","true_oos_validation_executed","ready_for_candidate_review","ready_for_promotion_review","promotion_allowed","multi_factor_composite_built","weight_optimization_executed","alpha_claim_allowed","production","broker_runtime","real_trade"]:
            assert f in v, f"{fid} snapshot missing: {f}"

def test_all_guardrails_have_required_fields():
    for fid in FACTORS:
        g = json.loads((ROOT / "factors" / fid / "guardrail_profile.json").read_text())
        for f in ["factor_id","required_guardrails","passed","requires_true_oos_before_promotion","promotion_allowed","alpha_claim_allowed"]:
            assert f in g, f"{fid} guardrail missing: {f}"

# ---- 3. Application contract 16 hard requires ----
REQUIRED_MODES = ["ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"]
REQUIRED_OUTPUTS = ["buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"]
REQUIRED_CONSUMERS = ["Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"]

def test_all_application_contracts_pass_16_hard_requires():
    for fid in FACTORS:
        ac = json.loads((ROOT / "factors" / fid / "application_contract.json").read_text())
        modes = ac.get("blocked_application_modes", [])
        outputs = ac.get("blocked_outputs", [])
        consumers = ac.get("blocked_downstream_consumers", [])
        for m in REQUIRED_MODES:
            assert m in modes, f"{fid}: missing blocked_application_modes: {m}"
        for o in REQUIRED_OUTPUTS:
            assert o in outputs, f"{fid}: missing blocked_outputs: {o}"
        for c in REQUIRED_CONSUMERS:
            assert c in consumers, f"{fid}: missing blocked_downstream_consumer: {c}"

def test_all_application_contracts_alpha_blocked():
    for fid in FACTORS:
        ac = json.loads((ROOT / "factors" / fid / "application_contract.json").read_text())
        assert ac.get("alpha_claim_allowed") is False

# ---- 4. Validation snapshot hard blocks ----
def test_all_validation_snapshots_promotion_false():
    for fid in FACTORS:
        v = json.loads((ROOT / "factors" / fid / "validation_snapshot.json").read_text())
        assert v.get("promotion_allowed") is False
        assert v.get("multi_factor_composite_built") is False
        assert v.get("weight_optimization_executed") is False

def test_all_validation_snapshots_no_promotion_review():
    for fid in FACTORS:
        v = json.loads((ROOT / "factors" / fid / "validation_snapshot.json").read_text())
        assert v.get("ready_for_promotion_review") == []

def test_all_validation_snapshots_alpha_blocked():
    for fid in FACTORS:
        v = json.loads((ROOT / "factors" / fid / "validation_snapshot.json").read_text())
        assert v.get("alpha_claim_allowed") is False

# ---- 5. All production/broker/real_trade BLOCKED ----
def test_all_artifacts_prod_blocked():
    for fid in FACTORS:
        for art in REQUIRED_ARTIFACTS:
            d = json.loads((ROOT / "factors" / fid / art).read_text())
            assert d.get("production") == "BLOCKED", f"{fid}/{art}: production={d.get('production')}"
            assert d.get("broker_runtime") == "BLOCKED", f"{fid}/{art}: broker={d.get('broker_runtime')}"
            assert d.get("real_trade") == "BLOCKED", f"{fid}/{art}: real_trade={d.get('real_trade')}"

# ---- 6. No buy/sell/position/alpha ----
def test_no_buy_sell_position_alpha_in_contracts():
    for fid in FACTORS:
        ac = json.loads((ROOT / "factors" / fid / "application_contract.json").read_text())
        outs = ac.get("allowed_outputs", [])
        for fb in ["buy_signal","sell_signal","position_weight","alpha_claim"]:
            assert fb not in outs, f"{fid}: forbidden output in allowed: {fb}"

# ---- 7. Batch closeout ----
def test_batch_closeout_completed():
    co = json.loads((ROOT / "batches" / "batch_003" / "batch3_interface_backfill_closeout.json").read_text())
    assert co.get("completed_backfill_count") == 8
    assert co.get("promotion_allowed") is False
    assert co.get("ready_for_candidate_review") == []
    assert co.get("alpha_claim_allowed") is False

# ---- 8. Evidence envelope ----
def test_all_envelopes_have_refs():
    for fid in FACTORS:
        e = json.loads((ROOT / "factors" / fid / "evidence_envelope.json").read_text())
        refs = e.get("artifact_refs", {})
        assert "formula_contract" in refs
        assert "materialization" in refs
        assert "coverage_validation" in refs

# ---- 9. Registry ----
def test_registry_has_backfilled():
    r = json.loads((ROOT / "registry.json").read_text())
    assert len(r.get("backfilled_batch3_pre_interface", [])) == 8

# ---- 10. Family registry ----
def test_family_registry_has_9():
    f = json.loads((ROOT / "family_registry.json").read_text())
    assert f.get("family_count") == 9

# ---- 11. Safety audit ----
def test_safety_audit_0():
    s = json.loads((ROOT / "batches" / "batch_003" / "batch3_interface_backfill_safety_audit.json").read_text())
    assert s.get("violation_count", 999) == 0

# ---- 12. Evidence audit ----
def test_evidence_audit_all():
    a = json.loads((ROOT / "batches" / "batch_003" / "batch3_interface_backfill_evidence_audit.json").read_text())
    assert a.get("audited_backfill_count") == 8
    assert a.get("all_backfilled") is True

# ---- 13. Rejected registry ----
def test_rejected_3():
    r = json.loads((ROOT / "rejected_factor_registry.json").read_text())
    assert len(r.get("rejected_factors", [])) == 3

# ---- 14. Unified candidate registry ----
def test_unified_candidate_6_frozen_8_pre():
    u = json.loads((ROOT / "unified_candidate_registry.json").read_text())
    assert u.get("total_frozen_candidate_count") == 6
    assert len(u.get("pre_interface_candidates", [])) == 8
