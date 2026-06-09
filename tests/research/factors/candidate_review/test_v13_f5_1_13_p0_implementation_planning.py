"""V13.F5.1.13 — P0 implementation planning tests."""
import json, subprocess
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_1_13_p0_implementation_planning")
F12 = ["batch3_p0_implementation_planning_overview.json","batch3_p0_file_level_plan.json","batch3_p0_noop_runner_contract_plan.json","batch3_p0_static_input_snapshot_plan.json","batch3_p0_hash_only_evidence_plan.json","batch3_p0_noop_output_contract_plan.json","batch3_p0_safety_guard_plan.json","batch3_p0_rollback_plan.json","batch3_p0_test_and_proof_plan.json","batch3_p0_risk_register.json","batch3_p0_safety_audit.json","batch3_p0_implementation_planning_closeout.json"]

def test_dir(): assert D.exists()
def test_12_files():
    for f in F12: assert (D/f).exists(), f"Missing: {f}"
def test_docs_only():
    ov = json.loads((D/"batch3_p0_implementation_planning_overview.json").read_text())
    assert ov.get("docs_only_planning") is True
def test_no_code():
    co = json.loads((D/"batch3_p0_implementation_planning_closeout.json").read_text())
    assert co.get("code_changed") is False
def test_file_level_future_only():
    fl = json.loads((D/"batch3_p0_file_level_plan.json").read_text())
    assert fl.get("current_branch_changes_code") is False
    assert fl.get("runtime_reports_write_allowed") is False
def test_noop_not_implemented():
    co = json.loads((D/"batch3_p0_implementation_planning_closeout.json").read_text())
    assert co.get("noop_runner_implemented") is False
def test_no_execution():
    co = json.loads((D/"batch3_p0_implementation_planning_closeout.json").read_text())
    for k in ["dry_run_execution_started","monitoring_execution_started","candidate_review_executed","factor_calculation_executed","factor_results_modified","runtime_reports_modified","runtime_audit_modified","external_data_fetch_started"]:
        assert co.get(k) is False
def test_no_promotion():
    co = json.loads((D/"batch3_p0_implementation_planning_closeout.json").read_text())
    assert co.get("promotion_allowed") is False and co.get("alpha_claim_allowed") is False
def test_prod_blocked():
    co = json.loads((D/"batch3_p0_implementation_planning_closeout.json").read_text())
    for k in ["production","broker_runtime","real_trade"]: assert co.get(k) == "BLOCKED"
def test_safety_guards_24():
    g = json.loads((D/"batch3_p0_safety_guard_plan.json").read_text())
    assert g.get("guard_count",0) >= 24
def test_proof_31():
    t = json.loads((D/"batch3_p0_test_and_proof_plan.json").read_text())
    assert t.get("proof_count",0) >= 30
def test_risk_16():
    r = json.loads((D/"batch3_p0_risk_register.json").read_text())
    assert r.get("risk_count",0) >= 16
def test_rollback_no_cleanup():
    r = json.loads((D/"batch3_p0_rollback_plan.json").read_text())
    assert r.get("no_runtime_report_cleanup_required") is True
    assert r.get("no_factor_result_cleanup_required") is True
def test_safety_0():
    s = json.loads((D/"batch3_p0_safety_audit.json").read_text())
    assert s.get("violation_count",999) == 0
    for v in s.get("checks",{}).values(): assert v is True
def test_noop_runner_forbidden():
    nc = json.loads((D/"batch3_p0_noop_runner_contract_plan.json").read_text())
    assert nc.get("runner_enabled") is False
    assert nc.get("side_effects_allowed") is False
def test_next():
    co = json.loads((D/"batch3_p0_implementation_planning_closeout.json").read_text())
    assert "HUMAN" in co.get("next_legal_entry","")
def test_hash_only():
    h = json.loads((D/"batch3_p0_hash_only_evidence_plan.json").read_text())
    assert h.get("persistent_write_allowed") is False
def test_noop_output():
    no = json.loads((D/"batch3_p0_noop_output_contract_plan.json").read_text())
    assert no.get("trade_signal_allowed") is False and no.get("broker_runtime_allowed") is False
def test_registry():
    
    # Historical phase test: read phase-local closeout instead of mutable registry.
    # The global registry is cumulative and advances with each subsequent phase;
    # phase-local closeouts are the stable historical fact source.
    co = json.loads((D/"batch3_p0_implementation_planning_closeout.json").read_text())
    assert co.get("status") == "V13_F5_1_13_P0_IMPLEMENTATION_PLANNING_READY_FOR_HUMAN_DECISION"
    assert co.get("noop_runner_implemented") is False
    assert co.get("docs_only_planning") is True
    assert co.get("code_changed") is False
def test_skillos():
    r = subprocess.run("git diff --name-only -- skillos",shell=True,capture_output=True,text=True)
    assert r.stdout.strip() == ""
