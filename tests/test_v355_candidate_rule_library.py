from zmatrix.entry_quality_repair.candidate_rule_library import apply_entry_candidate_rule

def test_candidate_rule_exclude_low_quality():
    rows = [{"paper_id": "p1", "entry_quality_score": 30, "entry_features": {}, "entry_archetype": "UNKNOWN_ENTRY_ARCHETYPE"}, {"paper_id": "p2", "entry_quality_score": 70, "entry_features": {}, "entry_archetype": "QUALITY_ROTATION"}]
    r = apply_entry_candidate_rule(enriched_rows=rows, rule_name="exclude_low_entry_quality")
    assert r["kept_count"] == 1
    assert r["kept"][0]["paper_id"] == "p2"
    assert r["real_trade_allowed"] is False
