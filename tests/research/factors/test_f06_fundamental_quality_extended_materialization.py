"""V13.F2.3.2 — Stage D: extended materialization tests."""
import csv, json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

mat = L("f06_fundamental_quality_extended_materialization.json")

def test_materialized():
    assert mat.get("materialization_executed") is True

def test_extended_panel_built():
    assert mat.get("extended_panel_built") is True

def test_pit_applied():
    assert mat.get("strict_pit_filter_applied") is True

def test_no_null_known():
    assert mat.get("null_known_at_row_count", 999) == 0

def test_no_placeholder_zero():
    assert mat.get("placeholder_zero_row_count", 999) == 0

def test_no_future_leakage():
    assert mat.get("future_leakage_check_pass") is True

def test_no_forbidden_labels():
    assert mat.get("forbidden_label_columns_present") is False

def test_coverage():
    assert mat.get("coverage_ratio", 0) > 0.5

def test_panel_csv_exists():
    p = RUNTIME_FACTORS / "f06_fundamental_quality_extended_panel.csv"
    assert p.exists()

def test_panel_no_outcome_labels():
    p = RUNTIME_FACTORS / "f06_fundamental_quality_extended_panel.csv"
    with open(p) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
    forbidden = ["forward_return_20d", "forward_return_60d", "future_return", "target_return", "label"]
    for h in forbidden:
        assert h not in headers, f"Found forbidden column: {h}"

def test_panel_required_columns():
    p = RUNTIME_FACTORS / "f06_fundamental_quality_extended_panel.csv"
    with open(p) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
    for col in ["rebalance_date", "ticker", "factor_value", "known_at", "available_at"]:
        assert col in headers

def test_sample_month():
    assert mat.get("sample_month_count_after_extension", 0) >= 1

def test_minimum_required():
    assert mat.get("minimum_month_count_required") == 12

def test_alpha_false():
    assert mat.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert mat.get("production") == "BLOCKED"
