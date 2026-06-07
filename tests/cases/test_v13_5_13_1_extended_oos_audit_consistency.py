"""V13.5.13.1 Extended OOS Audit Consistency — tests."""
import json,os;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
c=L("v13_5_13_1_extended_oos_audit_consistency_contract.json")
a=L("v13_5_13_extended_oos_accumulation_audit.json")
m=L("v13_5_13_tactical_20d_monitor.json")
co=L("v13_5_13_tactical_monitoring_closeout.json")
forbidden=["v13_6_","paper_trading_","production_","broker_","real_trade_","alpha_"]
def test_contract():assert c
def test_inconsistent():assert c.get("audit_inconsistency_detected")is True
def test_prev_end():assert len(c.get("previous_oos_end",""))>0
def test_20241129_not_new():assert "20241129"not in c.get("true_new_oos_months",[])
def test_audit_exists():assert a
def test_no_new_oos():
    if a.get("total_oos_months")==a.get("v57_oos_month_count"):assert a.get("new_oos_count",-1)==0
def test_monitor_no_update():assert not m.get("monitoring_updated")is True
def test_retained():assert co.get("candidate_retained")is True
def test_alpha():assert co.get("alpha_claim_allowed")is False
def test_prod():assert co.get("production")=="BLOCKED"
def test_no_forbidden():
    for p in forbidden:assert not any(f.startswith(p)for f in os.listdir(C)),f"found:{[f for f in os.listdir(C)if f.startswith(p)]}"
