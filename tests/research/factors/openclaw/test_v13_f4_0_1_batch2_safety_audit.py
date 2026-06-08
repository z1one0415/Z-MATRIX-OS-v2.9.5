"""V13.F4.0.1 — Safety audit tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
a = json.loads((B2 / "v13_f4_0_1_batch2_safety_audit.json").read_text())
def test_0_violations(): assert a.get("violation_count", 999) == 0
def test_prod_blocked(): assert a.get("production") == "BLOCKED"
