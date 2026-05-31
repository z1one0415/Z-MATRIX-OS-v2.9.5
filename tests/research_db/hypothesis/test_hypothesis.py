"""G16-C tests — hypothesis generation and validation"""
def test_hypothesis_production_false():
    from zmatrix.research_db.hypothesis.cross_layer_hypothesis_engine import generate_hypothesis, validate_hypothesis
    h = generate_hypothesis("NARRATIVE_REALITY_DIVERGENCE", "600519", ["narrative"], ["test"])
    r = validate_hypothesis(h)
    assert r["valid"] is True
    assert h["production_allowed"] is False

def test_hypothesis_not_verdict():
    from zmatrix.research_db.hypothesis.cross_layer_hypothesis_engine import generate_hypothesis
    h = generate_hypothesis("PHYSICAL_PRE_SIGNAL", "600519", ["physical"], ["test"])
    assert h["verdict_allowed"] is False
    assert h["trade_allowed"] is False

def test_hypothesis_trade_allowed_false():
    from zmatrix.research_db.hypothesis.cross_layer_hypothesis_engine import validate_hypothesis
    r = validate_hypothesis({"trade_allowed": True, "hypothesis_id": "x"})
    assert r["valid"] is False

def test_sell_on_news_trap_detected_from_fixture():
    from zmatrix.research_db.hypothesis.cross_layer_hypothesis_engine import detect_sell_on_news_trap
    h = detect_sell_on_news_trap(
        {"ticker": "600519", "body": "price adjustment rumor"},
        {"signal_type": "supply_chain_disruption"}
    )
    assert h is not None
    assert h["hypothesis_type"] == "SELL_ON_NEWS_TRAP"
    assert h["trade_allowed"] is False

def test_physical_pre_signal_detected_from_fixture():
    from zmatrix.research_db.hypothesis.cross_layer_hypothesis_engine import detect_physical_pre_signal
    results = detect_physical_pre_signal([
        {"signal_type": "supply_chain_disruption", "ticker": "600519"}
    ])
    assert len(results) >= 1
    assert results[0]["hypothesis_type"] == "PHYSICAL_PRE_SIGNAL"

def test_data_insufficient_blocks_confidence_upgrade():
    from zmatrix.research_db.hypothesis.cross_layer_hypothesis_engine import generate_hypothesis
    h = generate_hypothesis("DATA_SOURCE_DEGRADATION_IMPACT", "600519", ["source_health"], [], 0.1)
    assert h["confidence"] == 0.1

def test_npa_score_never_trade_signal():
    from zmatrix.research_db.event_physical.npa_scorer import calculate_npa
    result = calculate_npa(0.7, 0.3)
    assert result["trade_allowed"] is False
    assert result["production_allowed"] is False
