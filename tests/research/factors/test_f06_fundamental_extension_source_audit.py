"""V13.F2.3.2 — Stage B: source audit tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

a = L("f06_fundamental_extension_source_audit.json")

def test_audit_built():
    assert a.get("status") == "F06_FUNDAMENTAL_EXTENSION_SOURCE_AUDIT_BUILT"

def test_factor_id():
    assert a.get("factor_id") == "F06"

def test_required_fields():
    assert a.get("required_fields_available") is True

def test_has_ann_date():
    assert a.get("has_ann_date") is True

def test_has_end_date():
    assert a.get("has_end_date") is True

def test_fundamental_dir_exists():
    assert a.get("fundamental_directory_exists") is True

def test_files_found():
    assert a.get("total_fundamental_files", 0) > 0

def test_no_synthetic():
    assert a.get("synthetic_fundamentals_used") is False

def test_no_lookahead():
    assert a.get("lookahead_ann_date_detected") is False

def test_no_forward_fill():
    assert a.get("forward_filled_future_statement_detected") is False

def test_minimum_required():
    assert a.get("minimum_month_count_required") == 12

def test_preferred_required():
    assert a.get("preferred_month_count_required") == 24

def test_alpha_false():
    assert a.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert a.get("production") == "BLOCKED"
