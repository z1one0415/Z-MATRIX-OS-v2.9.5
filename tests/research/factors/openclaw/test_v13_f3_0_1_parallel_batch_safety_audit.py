"""V13.F3.0.1 — Safety audit tests."""
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

a = load("v13_f3_0_1_parallel_batch_safety_audit.json")

def test_audit_present():
    assert "SAFETY" in a.get("status", "")

def test_no_violations():
    assert a.get("violation_count", 999) == 0

def test_all_blocked():
    assert a.get("all_factors_blocked") is True
