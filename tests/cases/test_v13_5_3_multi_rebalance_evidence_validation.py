"""V13.5.3 Multi-Rebalance Evidence Validation — targeted tests."""
import json;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
em=L("v13_5_3_multi_rebalance_alpha_evidence_metrics.json");ev=L("v13_5_3_multi_rebalance_alpha_evidence_validation.json")
def test_metrics_exists():assert em
def test_validation_exists():assert ev
def test_sample_count():
    if ev.get("alpha_validation_executed"):assert ev.get("sample_month_count",0)>=24
def test_required_fields():
    for f in["bucket_monotonicity_20d_pass","long_short_spread_20d_mean","win_rate_20d","cost_adjusted_spread_20d_mean"]:assert f in em
def test_pass_or_blocked():assert"PASS"in ev.get("status","")or"BLOCKED"in ev.get("status","")
def test_evidence_pass_implies_grade():
    if ev.get("evidence_passed"):assert em.get("evidence_grade")=="PASS"
def test_evidence_blocked_has_reasons():
    if not ev.get("evidence_passed"):assert len(ev.get("blocked_reasons",[]))>0
def test_alpha_false():assert ev.get("alpha_claim_allowed")is False
def test_ready_false():assert ev.get("ready_for_alpha_claim")is False
def test_validated_false():assert ev.get("alpha_validated")is False
def test_prod_blocked():
    for k in["production","broker_runtime","real_trade"]:assert ev.get(k)=="BLOCKED"
