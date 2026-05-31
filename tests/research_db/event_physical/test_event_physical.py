"""G16-B tests — schema validation and fixture loading"""
def test_physical_signal_schema_requires_evidence_hash():
    from zmatrix.research_db.event_physical.physical_signal_schema import validate_signal
    r = validate_signal({"signal_id": "x"})
    assert r["valid"] is False
    assert any("evidence_hash" in e for e in r["errors"])

def test_narrative_event_schema_production_false():
    from zmatrix.research_db.event_physical.narrative_event_schema import validate_narrative_event
    r = validate_narrative_event({"event_id": "x", "evidence_hash": "h", "production_allowed": True})
    assert r["valid"] is False

def test_reality_check_links_event_and_signal():
    from zmatrix.research_db.event_physical.reality_check_schema import validate_reality_check
    r = validate_reality_check({"check_id": "x", "evidence_hash": "h"})
    assert r["valid"] is False  # missing narrative_event_id

def test_fixture_loader_no_external_api():
    from zmatrix.research_db.event_physical.physical_signal_loader import load_physical_signals
    signals = load_physical_signals()
    for s in signals:
        assert s.get("external_api_used") is False
        assert s.get("production_allowed") is False

def test_npa_schema_trade_false():
    from zmatrix.research_db.event_physical.npa_score_schema import validate_npa_score
    r = validate_npa_score({"score_id": "x", "trade_allowed": True})
    assert r["valid"] is False

def test_quality_checker_data_insufficient_when_missing_source():
    from zmatrix.research_db.event_physical.physical_signal_quality_checker import check_signal_quality
    r = check_signal_quality({"signal_id": "x"})
    assert r["quality_status"] == "DATA_INSUFFICIENT"
