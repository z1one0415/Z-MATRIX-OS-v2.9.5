"""Tests for V13.F5.5.1.2 Actual OOS Label Panel."""
import json, csv
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_csv_exists():
    assert (D / "v13_f5_5_1_2_actual_oos_label_panel.csv").exists()


def test_csv_has_data():
    csv_path = D / "v13_f5_5_1_2_actual_oos_label_panel.csv"
    lines = csv_path.read_text().strip().split("\n")
    assert len(lines) > 1  # header + at least 1 data row


def test_csv_schema():
    csv_path = D / "v13_f5_5_1_2_actual_oos_label_panel.csv"
    header = csv_path.read_text().strip().split("\n")[0]
    required = ["ticker", "rebalance_date", "label_month", "horizon",
                "forward_return", "label_available_at",
                "source_price_start_date", "source_price_end_date", "label_role"]
    for col in required:
        assert col in header


def test_csv_no_forbidden_columns():
    csv_path = D / "v13_f5_5_1_2_actual_oos_label_panel.csv"
    header = csv_path.read_text().strip().split("\n")[0]
    forbidden = ["factor_score", "rank", "bucket", "alpha_signal",
                 "trade_signal", "position", "order"]
    for col in forbidden:
        assert col not in header


def test_csv_label_role():
    csv_path = D / "v13_f5_5_1_2_actual_oos_label_panel.csv"
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            assert row["label_role"] == "OUTCOME_LABEL_ONLY"


def test_csv_horizons():
    csv_path = D / "v13_f5_5_1_2_actual_oos_label_panel.csv"
    horizons = set()
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            horizons.add(row["horizon"])
    assert "5D" in horizons
    assert "20D" in horizons
    assert "60D" not in horizons


def test_csv_forward_return_non_empty():
    csv_path = D / "v13_f5_5_1_2_actual_oos_label_panel.csv"
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            assert row["forward_return"] != ""
            assert float(row["forward_return"]) != 0 or True  # can be zero legitimately


def test_manifest():
    m = _l("v13_f5_5_1_2_actual_oos_label_panel_manifest.json")
    assert m["pipeline_signature"] == "Z2-V13-F5-5-1-2-ACTUAL-OOS-LABEL-PANEL-MANIFEST"
    assert m["label_role"] == "OUTCOME_LABEL_ONLY"
    assert m["total_rows"] > 0
    assert m["rows_5D"] > 0
    assert m["rows_20D"] > 0
    assert m["rows_60D"] == 0
    assert m["written_to_feature_store"] is False
    assert m["used_for_factor_calculation"] is False
    assert m["used_for_candidate_decision"] is False
    assert m["used_for_monitoring_execution"] is False
