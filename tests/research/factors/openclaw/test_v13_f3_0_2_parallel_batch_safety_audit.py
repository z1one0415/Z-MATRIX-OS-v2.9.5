"""V13.F3.0.2 — Canonical safety audit tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
a = json.loads((BATCH / "v13_f3_0_2_parallel_batch_safety_audit.json").read_text())
def test_violations_0(): assert a.get("violation_count", 999) == 0
def test_all_blocked(): assert a.get("all_blocked") is True
