"""V13.F2.3 — Stage B: outcome label panel tests."""
import csv, json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

report = L("v13_f2_3_outcome_label_panel_build_report.json")

def test_report_built():
    assert report.get("status") == "V13_F2_3_OUTCOME_LABEL_PANEL_BUILT"

def test_label_panel_exists():
    p = RUNTIME_FACTORS / "single_factor_outcome_label_panel.csv"
    assert p.exists()

def test_label_role():
    assert report.get("label_role") == "OUTCOME_LABEL_ONLY"

def test_label_horizons():
    assert "20D" in report.get("label_horizons", [])
    assert "60D" in report.get("label_horizons", [])

def test_label_row_count_positive():
    assert report.get("label_row_count", 0) > 0

def test_label_known_after_rebalance():
    assert report.get("label_known_after_rebalance") is True

def test_not_written_to_factor_panel():
    assert report.get("written_to_factor_panel") is False

def test_no_forbidden_columns():
    assert report.get("forbidden_columns_written_to_factor_panel") is False

def test_no_buy_sell_trade():
    p = RUNTIME_FACTORS / "single_factor_outcome_label_panel.csv"
    with open(p) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
    forbidden = ["buy", "sell", "trade", "position"]
    assert not any(h.lower() in forbidden for h in headers)

def test_required_columns():
    p = RUNTIME_FACTORS / "single_factor_outcome_label_panel.csv"
    with open(p) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
    required = ["rebalance_date", "ticker", "forward_return_20d", "forward_return_60d", "label_role"]
    for col in required:
        assert col in headers

def test_alpha_false():
    assert report.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert report.get("production") == "BLOCKED"
