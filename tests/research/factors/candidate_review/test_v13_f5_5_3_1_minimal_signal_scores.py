"""Tests for V13.F5.5.3.1 Minimal Signal Scores."""
import json, csv
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")
FACTORS = ["F21", "F24", "F30", "F31"]


def _l(n):
    return json.loads((D / n).read_text())


def test_all_csvs_exist():
    for f in FACTORS:
        assert (D / f"{f}_signal_scores.csv").exists()


def test_csv_row_counts():
    for f in FACTORS:
        with open(D / f"{f}_signal_scores.csv") as fh:
            rows = list(csv.DictReader(fh))
            assert len(rows) == 5


def test_csv_schema():
    required = ["factor_id", "ticker", "rebalance_date", "score",
                "rank", "bucket", "score_available_at",
                "source_artifact_ref", "signal_role"]
    for f in FACTORS:
        with open(D / f"{f}_signal_scores.csv") as fh:
            reader = csv.DictReader(fh)
            for col in required:
                assert col in reader.fieldnames


def test_csv_no_forbidden_columns():
    forbidden = ["forward_return", "alpha_signal", "trade_signal",
                 "buy_signal", "sell_signal", "position_weight", "order"]
    for f in FACTORS:
        with open(D / f"{f}_signal_scores.csv") as fh:
            reader = csv.DictReader(fh)
            for col in forbidden:
                assert col not in reader.fieldnames


def test_csv_signal_role():
    for f in FACTORS:
        with open(D / f"{f}_signal_scores.csv") as fh:
            for row in csv.DictReader(fh):
                assert row["signal_role"] == "FACTOR_SIGNAL_ONLY"


def test_csv_scores_non_empty():
    for f in FACTORS:
        with open(D / f"{f}_signal_scores.csv") as fh:
            for row in csv.DictReader(fh):
                assert row["score"] != ""
                assert row["rank"] != ""
                assert row["bucket"] != ""


def test_csv_rebalance_date():
    for f in FACTORS:
        with open(D / f"{f}_signal_scores.csv") as fh:
            for row in csv.DictReader(fh):
                assert row["rebalance_date"] == "2026-05-06"


def test_manifest():
    m = _l("v13_f5_5_3_1_signal_scores_manifest.json")
    assert m["pipeline_signature"] == "Z2-V13-F5-5-3-1-SIGNAL-SCORES-MANIFEST"
    assert m["status"] == "V13_F5_5_3_1_SIGNAL_SCORES_GENERATED"
    assert m["total_signal_rows"] == 20
    assert m["rows_per_factor"] == 5
    assert m["ticker_count"] == 5
    assert m["signal_role"] == "FACTOR_SIGNAL_ONLY"
    assert m["forward_return_used_for_signal"] is False
    assert m["outcome_label_used_for_signal"] is False
    assert m["written_to_feature_store"] is False
