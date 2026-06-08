"""V13.F3.5 — Trigger calendar tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
p = json.loads((B / "v13_f3_5_monitoring_trigger_calendar_plan.json").read_text())
def test_oos_boundary(): assert p.get("minimum_oos_start_exclusive") == "20260501"
def test_5d_label(): r = [x for x in p.get("label_availability_rules",[]) if x["horizon"]=="5D"]; assert r and "F11" in r[0]["required_for"]
def test_20d_label(): r = [x for x in p.get("label_availability_rules",[]) if x["horizon"]=="20D"]; assert r and all(f in r[0]["required_for"] for f in ["F04","F10","F11"])
def test_not_executed(): assert p.get("monitoring_execution_executed") is False
def test_no_oos(): assert p.get("true_oos_validation_executed") is False
def test_no_alpha(): assert p.get("alpha_claim_allowed") is False
