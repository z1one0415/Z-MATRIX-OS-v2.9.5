"""V13.F2.3.2 — Stage C: available-at map tests."""
import csv, json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

r = L("f06_extended_available_at_map_report.json")

def test_map_built_or_blocked():
    assert "F06_EXTENDED_AVAILABLE_AT_MAP" in r.get("status", "")

def test_no_null_known():
    assert r.get("null_known_at_row_count", 999) == 0

def test_no_null_avail():
    assert r.get("null_available_at_row_count", 999) == 0

def test_no_null_ann():
    assert r.get("null_ann_date_row_count", 999) == 0

def test_no_future_leakage():
    assert r.get("future_statement_leakage_detected") is False

def test_csv_exists():
    p = RUNTIME_FACTORS / "f06_extended_available_at_map.csv"
    assert p.exists()

def test_csv_has_required_columns():
    p = RUNTIME_FACTORS / "f06_extended_available_at_map.csv"
    with open(p) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
    for col in ["ticker", "ann_date", "known_at", "available_at", "source_mode"]:
        assert col in headers

def test_source_mode_is_real():
    p = RUNTIME_FACTORS / "f06_extended_available_at_map.csv"
    with open(p) as f:
        reader = csv.DictReader(f)
        for row in reader:
            assert row.get("source_mode") == "REAL_FUNDAMENTALS"

def test_alpha_false():
    assert r.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert r.get("production") == "BLOCKED"
