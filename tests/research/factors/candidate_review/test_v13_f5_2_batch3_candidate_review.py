"""
V13.F5.2 Batch3 Candidate Review Decision — Consolidated Test
==============================================================
Validates all 7 output artifacts for correctness, blocking flags,
and inter-file consistency.
"""

import json
from pathlib import Path

BASE = Path("/Users/z1/Documents/Z-MATRIX-OS v2.9.5")
REVIEW_DIR = BASE / "research/factor_library/reviews/batch_003/f5_2_candidate_review_decision"

ALL_FACTORS = ["F21", "F22", "F24", "F26", "F27", "F30", "F31", "F34"]
TACTICAL = ["F21", "F24", "F30"]
REGIME_SPECIFIC = ["F31"]
WATCH_ONLY = ["F22", "F26", "F27", "F34"]


def _load(filename: str) -> dict:
    return json.loads((REVIEW_DIR / filename).read_text())


# ─── Test 1: All 7 output files exist ────────────────────────────────────────

def test_all_output_files_exist():
    expected_files = [
        "v13_f5_2_batch3_candidate_review_contract.json",
        "v13_f5_2_batch3_candidate_evidence_package_audit.json",
        "v13_f5_2_batch3_family_overlap_review.json",
        "v13_f5_2_batch3_horizon_regime_cost_review.json",
        "v13_f5_2_batch3_candidate_review_scorecard.json",
        "v13_f5_2_batch3_candidate_review_safety_audit.json",
        "v13_f5_2_batch3_candidate_review_closeout.json",
    ]
    for f in expected_files:
        path = REVIEW_DIR / f
        assert path.exists(), f"Missing: {f}"
        # Verify valid JSON
        data = json.loads(path.read_text())
        assert isinstance(data, dict), f"Not a JSON object: {f}"


# ─── Test 2: Contract scope and blocking flags ────────────────────────────────

def test_contract_scope_and_blocking():
    c = _load("v13_f5_2_batch3_candidate_review_contract.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-2-BATCH3-CANDIDATE-REVIEW-CONTRACT"
    assert c["candidate_review_scope"] == ALL_FACTORS
    assert c["candidate_review_execution_allowed"] is True
    # Blocking flags
    assert c["candidate_freeze_allowed"] is False
    assert c["promotion_allowed"] is False
    assert c["multi_factor_composite_allowed"] is False
    assert c["weight_optimization_allowed"] is False
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["v13_6_allowed"] is False
    assert c["paper_trading_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"


# ─── Test 3: Evidence audit passes all 8 factors ─────────────────────────────

def test_evidence_audit_all_pass():
    a = _load("v13_f5_2_batch3_candidate_evidence_package_audit.json")
    assert a["status"] == "V13_F5_2_EVIDENCE_PACKAGE_AUDIT_PASS"
    assert a["factors_audited"] == ALL_FACTORS
    assert a["all_pass"] is True
    assert a["violation_count"] == 0
    assert a["ready_for_promotion_review"] == []
    # Each factor has all checks true
    for factor in ALL_FACTORS:
        audit = a["per_factor_audit"][factor]
        for key in ["manifest", "validation_snapshot", "guardrail_profile",
                    "application_contract", "evidence_envelope",
                    "blocks_alpha", "blocks_production",
                    "coverage_passed", "pit_passed"]:
            assert audit[key] is True, f"{factor}.{key} not True"


# ─── Test 4: Family overlap review — 3 families, correct overlap concerns ────

def test_family_overlap_review():
    f = _load("v13_f5_2_batch3_family_overlap_review.json")
    assert f["status"] == "V13_F5_2_FAMILY_OVERLAP_REVIEW_PASS"
    families = f["families"]
    assert set(families.keys()) == {"TREND_STRUCTURE", "LIQUIDITY_VOLUME", "TAIL_RISK"}

    # TREND_STRUCTURE
    ts = families["TREND_STRUCTURE"]
    assert ts["members"] == ["F21", "F22", "F24"]
    assert ts["existing_frozen_overlap"] == ["F04"]
    assert ts["advanced"] == ["F21", "F24"]
    assert ts["held_back"] == ["F22"]

    # LIQUIDITY_VOLUME
    lv = families["LIQUIDITY_VOLUME"]
    assert lv["members"] == ["F26", "F27", "F30"]
    assert lv["existing_frozen_overlap"] == ["F11"]
    assert lv["advanced"] == ["F30"]
    assert lv["held_back"] == ["F26", "F27"]

    # TAIL_RISK
    tr = families["TAIL_RISK"]
    assert tr["members"] == ["F31", "F34"]
    assert tr["existing_frozen_overlap"] == ["F10"]
    assert tr["advanced"] == ["F31"]
    assert tr["held_back"] == ["F34"]


# ─── Test 5: Horizon/regime review classifies all 8 ──────────────────────────

def test_horizon_regime_cost_review():
    h = _load("v13_f5_2_batch3_horizon_regime_cost_review.json")
    assert h["status"] == "V13_F5_2_HORIZON_REGIME_COST_REVIEW_PASS"
    classifications = h["classifications"]
    assert set(classifications.keys()) == set(ALL_FACTORS)

    for factor in ALL_FACTORS:
        assert "horizon" in classifications[factor]
        assert "regime_dependency" in classifications[factor]
        assert "cost_tier" in classifications[factor]
        assert "classification" in classifications[factor]

    # Verify specific classifications
    for f in TACTICAL:
        assert classifications[f]["classification"] == "TACTICAL_CANDIDATE"
    for f in REGIME_SPECIFIC:
        assert classifications[f]["classification"] == "REGIME_SPECIFIC_CANDIDATE"
    for f in WATCH_ONLY:
        assert classifications[f]["classification"] == "WATCH_ONLY"


# ─── Test 6: Scorecard — 3 tactical, 1 regime, 4 watch ───────────────────────

def test_scorecard_classifications():
    s = _load("v13_f5_2_batch3_candidate_review_scorecard.json")
    assert s["status"] == "V13_F5_2_BATCH3_CANDIDATE_REVIEW_SCORECARD_COMPLETE"
    assert s["reviewed_factors"] == ALL_FACTORS
    assert sorted(s["tactical_candidate_ready"]) == sorted(TACTICAL)
    assert s["regime_specific_candidate_ready"] == REGIME_SPECIFIC
    assert sorted(s["watch_only"]) == sorted(WATCH_ONLY)
    assert s["freeze_review_ready"] == []
    assert s["rework_required"] == []
    assert s["rejected"] == []
    assert s["ready_for_promotion_review"] == []
    assert s["candidate_freeze_executed"] is False
    assert s["promotion_allowed"] is False


# ─── Test 7: Safety audit — all checks pass, no violations ───────────────────

def test_safety_audit():
    sa = _load("v13_f5_2_batch3_candidate_review_safety_audit.json")
    assert sa["status"] == "V13_F5_2_SAFETY_AUDIT_PASS"
    assert sa["violation_count"] == 0
    checks = sa["checks"]
    # All "false" checks (things NOT done)
    false_checks = [
        "candidate_freeze_executed", "promotion_allowed",
        "multi_factor_composite_built", "weight_optimization_executed",
        "runner_enabled", "execution_allowed",
        "factor_calculation_executed", "materialization_executed",
        "oos_label_generation_executed", "true_oos_validation_executed",
        "skillos_adapter_implemented", "frontend_modified",
        "v13_6_allowed", "paper_trading_allowed", "alpha_claim_allowed",
    ]
    for key in false_checks:
        assert checks[key] is False, f"Safety check {key} should be False"
    # All "true" checks (things blocked)
    true_checks = [
        "ready_for_promotion_review_empty",
        "production_blocked", "broker_runtime_blocked", "real_trade_blocked",
    ]
    for key in true_checks:
        assert checks[key] is True, f"Safety check {key} should be True"


# ─── Test 8: Closeout — candidate_review_executed, freeze_review_ready=[], ready_for_f5_3 ─

def test_closeout():
    cl = _load("v13_f5_2_batch3_candidate_review_closeout.json")
    assert cl["status"] == "V13_F5_2_BATCH3_CANDIDATE_REVIEW_PASS"
    assert cl["candidate_review_executed"] is True
    assert cl["freeze_review_ready"] == []
    assert sorted(cl["ready_for_f5_3_candidate_freeze_review"]) == sorted(["F21", "F24", "F30", "F31"])
    assert cl["ready_for_promotion_review"] == []
    assert cl["tactical_candidate_ready"] == TACTICAL
    assert cl["regime_specific_candidate_ready"] == REGIME_SPECIFIC
    assert cl["watch_only"] == WATCH_ONLY
    assert cl["rework_required"] == []
    assert cl["rejected"] == []
    # Blocking
    assert cl["candidate_freeze_executed"] is False
    assert cl["promotion_allowed"] is False
    assert cl["multi_factor_composite_built"] is False
    assert cl["weight_optimization_executed"] is False
    assert cl["runner_enabled"] is False
    assert cl["execution_allowed"] is False
    assert cl["v13_6_allowed"] is False
    assert cl["paper_trading_allowed"] is False
    assert cl["alpha_claim_allowed"] is False
    assert cl["production"] == "BLOCKED"
    assert cl["broker_runtime"] == "BLOCKED"
    assert cl["real_trade"] == "BLOCKED"
    assert cl["recommended_next_action"] == "PREPARE_V13_F5_3_BATCH3_CANDIDATE_FREEZE_REVIEW"


# ─── Test 9: Cross-file blocking consistency ─────────────────────────────────

def test_cross_file_blocking_consistency():
    """All files that have production/broker/real_trade must be BLOCKED."""
    contract = _load("v13_f5_2_batch3_candidate_review_contract.json")
    closeout = _load("v13_f5_2_batch3_candidate_review_closeout.json")

    for doc_name, doc in [("contract", contract), ("closeout", closeout)]:
        assert doc["production"] == "BLOCKED", f"{doc_name} production not BLOCKED"
        assert doc["broker_runtime"] == "BLOCKED", f"{doc_name} broker_runtime not BLOCKED"
        assert doc["real_trade"] == "BLOCKED", f"{doc_name} real_trade not BLOCKED"
        assert doc["runner_enabled"] is False, f"{doc_name} runner_enabled not False"
        assert doc["execution_allowed"] is False, f"{doc_name} execution_allowed not False"

    safety = _load("v13_f5_2_batch3_candidate_review_safety_audit.json")
    assert safety["checks"]["production_blocked"] is True
    assert safety["checks"]["broker_runtime_blocked"] is True
    assert safety["checks"]["real_trade_blocked"] is True
    assert safety["checks"]["runner_enabled"] is False
    assert safety["checks"]["execution_allowed"] is False


# ─── Test 10: Recommended next action ────────────────────────────────────────

def test_recommended_next_action():
    cl = _load("v13_f5_2_batch3_candidate_review_closeout.json")
    assert cl["recommended_next_action"] == "PREPARE_V13_F5_3_BATCH3_CANDIDATE_FREEZE_REVIEW"
