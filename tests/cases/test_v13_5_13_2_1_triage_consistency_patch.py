"""V13.5.13.2.1 Triage Consistency Patch — tests."""
import json,csv;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
c1=L("v13_5_13_2_1_triage_consistency_contract.json")
attr=L("v13_5_13_2_april_oos_event_attribution.json")
sc=L("v13_5_13_2_sequential_risk_scorecard.json")
wk=L("v13_5_13_2_weekly_anchor_diagnostic.json")
co=L("v13_5_13_2_fast_tactical_evidence_triage_closeout.json")
def test_contract():assert c1
def test_hl_mismatch():assert c1.get("hl_mismatch_detected")is True
def test_hl_aligned():assert abs(sc.get("latest_formal_20d_hl",0)-attr.get("event_20d_hl",0))<0.0001
def test_sc_fail_aligned():assert sc.get("latest_event_scope_failure_confirmed")==attr.get("scope_failure_confirmed")
def test_hl_gt_minus2():assert attr.get("event_20d_hl",-99)>-0.02
def test_sc_fail_false():assert sc.get("latest_event_scope_failure_confirmed")is False
def test_anchor_filter():assert wk.get("min_anchor_date","")>"20260331"
def test_no_old_anchors():
    csv_f=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"/"v13_5_13_2_weekly_anchor_diagnostic_panel.csv"
    if csv_f.exists():
        for r in csv.DictReader(open(csv_f)):
            assert r["anchor_date"]>"20260331",f"old:{r['anchor_date']}"
def test_sus_not_allowed():assert sc.get("suspension_decision_allowed")is False
def test_retained():assert sc.get("candidate_retained")is True and co.get("candidate_suspended")is False
def test_no_v13_6():assert co.get("v13_6_allowed")is False
def test_alpha():assert co.get("alpha_claim_allowed")is False
def test_prod():assert co.get("production")=="BLOCKED"
