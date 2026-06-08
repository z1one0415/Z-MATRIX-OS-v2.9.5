"""V13.F2.3.2 — Stage E: sample readiness validation tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

v = L("f06_extended_sample_readiness_validation.json")

def test_validation_built():
    assert "F06_EXTENDED_SAMPLE_READINESS" in v.get("status", "")

def test_factor_id():
    assert v.get("factor_id") == "F06"

def test_pit_checked():
    assert isinstance(v.get("pit_passed"), bool)

def test_coverage_checked():
    assert isinstance(v.get("coverage_passed"), bool)

def test_minimum_required():
    assert v.get("minimum_month_count_required") == 12

def test_preferred_required():
    assert v.get("preferred_month_count_required") == 24

def test_ready_is_bool():
    assert isinstance(v.get("ready_for_revalidation"), bool)

def test_alpha_false():
    assert v.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert v.get("production") == "BLOCKED"
