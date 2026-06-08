"""V13.F4.0.2 — Parent safety tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
a = json.loads((B2 / "v13_f4_0_2_batch2_parent_safety_audit.json").read_text())
def test_0(): assert a.get("violation_count", 999) == 0
def test_prod_blocked(): assert a.get("production") == "BLOCKED"
