"""V13.F3.5 — Safety audit tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
a = json.loads((B / "v13_f3_5_candidate_monitoring_plan_safety_audit.json").read_text())
def test_0_violations(): assert a.get("violation_count", 999) == 0
def test_prod_blocked(): assert a.get("production") == "BLOCKED"
