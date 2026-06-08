"""V13.F5.1.3 — Batch3 candidate review prep tests."""
import json, glob
from pathlib import Path

REVIEW_DIR = Path("research/factor_library/reviews/batch_003/f5_1_3_candidate_review_prep")
FACTORS = ["F21","F22","F24","F26","F27","F30","F31","F34"]
REQUIRED = [
    "batch3_candidate_review_prep_overview.json",
    "batch3_candidate_review_prep_factor_matrix.json",
    "batch3_candidate_review_prep_evidence_matrix.json",
    "batch3_candidate_review_prep_family_overlap_matrix.json",
    "batch3_candidate_review_prep_guardrail_matrix.json",
    "batch3_candidate_review_prep_pit_coverage_matrix.json",
    "batch3_candidate_review_prep_readonly_application_matrix.json",
    "batch3_candidate_review_prep_risk_register.json",
    "batch3_candidate_review_prep_decision_template.json",
    "batch3_candidate_review_prep_closeout.json",
    "batch3_candidate_review_prep_safety_audit.json"
]

def test_prep_directory_exists():
    assert REVIEW_DIR.exists()

def test_all_11_prep_files_exist():
    for f in REQUIRED:
        assert (REVIEW_DIR / f).exists(), f"Missing: {f}"

def test_factor_matrix_8_factors():
    m = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_factor_matrix.json").read_text())
    assert m.get("factor_count") == 8
    assert len(m.get("factors", [])) == 8

def test_evidence_matrix_8_factors():
    m = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_evidence_matrix.json").read_text())
    assert m.get("factor_count") == 8

def test_family_overlap_matrix_8():
    m = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_family_overlap_matrix.json").read_text())
    assert len(m.get("overlaps", [])) == 8

def test_guardrail_matrix_8():
    m = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_guardrail_matrix.json").read_text())
    assert m.get("factor_count") == 8

def test_pit_coverage_matrix_8():
    m = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_pit_coverage_matrix.json").read_text())
    assert m.get("factor_count") == 8

def test_readonly_matrix_8():
    m = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_readonly_application_matrix.json").read_text())
    assert m.get("factor_count") == 8

def test_risk_register_min_16():
    r = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_risk_register.json").read_text())
    assert r.get("risk_count", 0) >= 16, f"Only {r.get('risk_count')} risks (need >=16)"

def test_decision_template_pending():
    d = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_decision_template.json").read_text())
    assert d.get("decision_status") == "PENDING_HUMAN_REVIEW"
    assert d["pending_fields"]["decision"] == "PENDING"

def test_closeout_status():
    co = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_closeout.json").read_text())
    assert co.get("status") == "V13_F5_1_3_BATCH3_CANDIDATE_REVIEW_PREP_READY_FOR_HUMAN_DECISION"

def test_candidate_review_not_executed():
    co = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_closeout.json").read_text())
    assert co.get("candidate_review_executed") is False
    assert co.get("candidate_promotion_executed") is False

def test_promotion_alpha_false():
    co = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_closeout.json").read_text())
    assert co.get("promotion_allowed") is False
    assert co.get("alpha_claim_allowed") is False

def test_composite_weight_false():
    co = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_closeout.json").read_text())
    assert co.get("multi_factor_composite_built") is False
    assert co.get("weight_optimization_executed") is False

def test_prod_broker_rt_blocked():
    co = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_closeout.json").read_text())
    assert co.get("production") == "BLOCKED"
    assert co.get("broker_runtime") == "BLOCKED"
    assert co.get("real_trade") == "BLOCKED"

def test_skillos_not_modified():
    co = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_closeout.json").read_text())
    assert co.get("skillos_modified") is False
    assert co.get("runtime_reports_modified") is False
    assert co.get("factor_results_modified") is False

def test_no_buy_sell_in_app_contracts():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        outs = ac.get("allowed_outputs", [])
        for fb in ["buy_signal","sell_signal","position_weight","alpha_claim"]:
            assert fb not in outs, f"{fid}: forbidden output in allowed: {fb}"

def test_all_application_modes_canonical():
    canonical = {"REGISTRY_READ","EVIDENCE_READ","VALIDATION_SUMMARY","GUARDRAIL_SUMMARY","CANDIDATE_MONITOR","RESEARCH_CONTEXT","SCORING_CONTEXT_DRY_PLAN","COMPOSITION_GRAPH_DRY_PLAN"}
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        for mode in ac.get("allowed_application_modes", []):
            assert mode in canonical, f"{fid}: non-canonical mode: {mode}"

def test_rejected_factors_preserved():
    rfr = json.loads(Path("research/factor_library/rejected_factor_registry.json").read_text())
    rejected_ids = [f["factor_id"] for f in rfr.get("rejected_factors", [])]
    assert "F02" in rejected_ids
    assert "F03" in rejected_ids
    assert "F05" in rejected_ids

def test_safety_audit_0():
    s = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_safety_audit.json").read_text())
    assert s.get("violation_count", 999) == 0
    assert s["checks"]["no_candidate_promotion"] is True
    assert s["checks"]["no_alpha_claim"] is True
    assert s["checks"]["no_production"] is True
    assert s["checks"]["no_skillos_modification"] is True

def test_decision_template_forbidden():
    d = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_decision_template.json").read_text())
    assert "PROMOTE_TO_ALPHA" in d.get("forbidden_decisions", [])
    assert "START_PRODUCTION" in d.get("forbidden_decisions", [])

def test_next_legal_entry():
    co = json.loads((REVIEW_DIR / "batch3_candidate_review_prep_closeout.json").read_text())
    assert "HUMAN" in co.get("next_legal_entry", "")
