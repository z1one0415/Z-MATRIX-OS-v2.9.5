"""Tests for V13.F5.5.3 Signal Score Schema."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")


def _l(n):
    return json.loads((D / n).read_text())


def test_schema_exists():
    assert (D / "v13_f5_5_3_signal_score_schema.json").exists()


def test_schema_status():
    s = _l("v13_f5_5_3_signal_score_schema.json")
    assert s["pipeline_signature"] == "Z2-V13-F5-5-3-SIGNAL-SCORE-SCHEMA"
    assert s["status"] == "V13_F5_5_3_SIGNAL_SCORE_SCHEMA_DEFINED"


def test_required_fields():
    s = _l("v13_f5_5_3_signal_score_schema.json")
    field_names = [f["name"] for f in s["required_fields"]]
    expected = ["factor_id", "ticker", "rebalance_date", "score", "rank",
                "bucket", "score_available_at", "source_artifact_ref", "signal_role"]
    assert field_names == expected


def test_constraints():
    s = _l("v13_f5_5_3_signal_score_schema.json")
    c = s["constraints"]
    assert c["signal_role"] == "FACTOR_SIGNAL_ONLY"
    assert c["not_outcome_label"] is True
    assert c["not_trade_signal"] is True
    assert c["not_alpha_signal"] is True
    assert c["not_position_weight"] is True
    assert c["not_buy_sell_signal"] is True


def test_usage_restrictions():
    s = _l("v13_f5_5_3_signal_score_schema.json")
    blocked = s["usage_restrictions"]["blocked_for"]
    assert "trade_execution" in blocked
    assert "alpha_claim" in blocked
    assert "production" in blocked
    assert "broker" in blocked
