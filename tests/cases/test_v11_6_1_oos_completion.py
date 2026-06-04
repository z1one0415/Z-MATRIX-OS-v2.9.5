import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_contract_does_not_read_simulation():
    src=open(W/"scripts/cases/build_v11_6_1_oos_completion_contract.py").read()
    assert "v11_5_paper_portfolio_simulation" not in src
def test_contract_is_pure():
    ct=json.loads((W/"runtime_reports/cases/v11_6_1_oos_completion_contract.json").read_text())
    assert "observations" not in ct
    assert "t20_complete" not in ct
    assert ct["paper_tracking_period_completed"] is False
def test_due_labels_available():
    res=json.loads((W/"runtime_reports/cases/v11_6_1_oos_due_label_resolution.json").read_text())
    assert res["all_due_labels_available"] is True
    assert res["available_observation_count"]==30
def test_outcomes_calculated():
    out=json.loads((W/"runtime_reports/cases/v11_6_1_oos_paper_outcomes.json").read_text())
    assert out["calculated_observation_count"]==30
    assert out["blocked_observation_count"]==0
def test_audit_pass():
    a=json.loads((W/"runtime_reports/cases/v11_6_1_oos_completion_audit.json").read_text())
    assert a["status"]=="V11_6_1_OOS_COMPLETION_AUDIT_PASS"
    assert a["paper_tracking_period_completed"] is True
    assert a["contract_purity_ok"] is True
def test_closeout_reads_audit():
    co=json.loads((W/"runtime_reports/cases/v11_6_closeout.json").read_text())
    assert co["paper_tracking_period_completed"] is True
    assert co["substage_ready_for_v12_gate"] is True
def test_v12_research_only_safely():
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["status"]=="V12_ALPHA_OPERATING_LOOP_RESEARCH_ONLY_ALLOWED"
    assert g["blocking_reasons"]==[]
    assert g["ready_for_alpha_claim"] is False
    assert g["production"]=="BLOCKED"
