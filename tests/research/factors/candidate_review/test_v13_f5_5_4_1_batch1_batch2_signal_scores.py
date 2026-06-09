"""Tests for V13.F5.5.4.1 Batch1/Batch2 Signal Scores."""
import json, csv
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")
MATERIALIZED = ["F04", "F10", "F11"]
BLOCKED = ["F14", "F15", "F16"]

def _l(n): return json.loads((D / n).read_text())

def test_materialized_csvs_exist():
    for f in MATERIALIZED:
        assert (D / f"{f}_signal_scores.csv").exists()

def test_blocked_csvs_not_exist():
    for f in BLOCKED:
        assert not (D / f"{f}_signal_scores.csv").exists()

def test_csv_row_counts():
    for f in MATERIALIZED:
        with open(D / f"{f}_signal_scores.csv") as fh:
            assert len(list(csv.DictReader(fh))) == 5

def test_csv_signal_role():
    for f in MATERIALIZED:
        with open(D / f"{f}_signal_scores.csv") as fh:
            for row in csv.DictReader(fh):
                assert row["signal_role"] == "FACTOR_SIGNAL_ONLY"

def test_csv_no_forbidden_columns():
    forbidden = ["forward_return", "alpha_signal", "trade_signal",
                 "buy_signal", "sell_signal", "position_weight", "order"]
    for f in MATERIALIZED:
        with open(D / f"{f}_signal_scores.csv") as fh:
            reader = csv.DictReader(fh)
            for col in forbidden:
                assert col not in reader.fieldnames

def test_manifest():
    m = _l("v13_f5_5_4_1_signal_scores_manifest.json")
    assert m["status"] == "V13_F5_5_4_1_SIGNAL_SCORES_PARTIAL"
    assert m["materialized_factors"] == MATERIALIZED
    assert m["blocked_factors"] == BLOCKED
    assert m["total_signal_rows"] == 15
    assert m["forward_return_used_for_signal"] is False
    assert m["written_to_feature_store"] is False
