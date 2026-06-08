"""V13.F3.0 — Safety audit tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

BATCH = RUNTIME_FACTORS / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

a = load("v13_f3_0_parallel_batch_safety_audit.json")

def test_audit_present():
    assert "SAFETY" in a.get("status", "")

def test_violations_is_list():
    assert isinstance(a.get("violations"), list)

def test_all_prod_blocked():
    assert a.get("all_factors_blocked") is True
