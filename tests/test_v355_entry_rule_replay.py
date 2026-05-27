from zmatrix.entry_quality_repair.entry_rule_replay import run_entry_rule_replay

def test_entry_rule_replay_runs():
    rows = [{"paper_id": "p1", "actual_return_t20": -2, "entry_quality_score": 30, "entry_features": {"price_above_ma60": False, "volume_ratio_5_20": 0.5}, "entry_archetype": "LOW_VOLUME_WEAKNESS"}, {"paper_id": "p2", "actual_return_t20": 5, "entry_quality_score": 80, "entry_features": {"price_above_ma60": True, "volume_ratio_5_20": 1.2}, "entry_archetype": "QUALITY_ROTATION"}]
    r = run_entry_rule_replay(enriched_rows=rows)
    assert "baseline" in r
    assert "exclude_low_entry_quality" in r["candidates"]
    assert r["real_trade_allowed"] is False
