def test_fast_tier_contains_market():
    from zmatrix.runtime.research_refresh_tiers import get_tier, FAST_RESEARCH_LAYER
    assert "MARKET_OUTCOME_LAYER" in FAST_RESEARCH_LAYER
    assert get_tier("MARKET_OUTCOME_LAYER") == "FAST"

def test_heavy_tier_contains_caseforge():
    from zmatrix.runtime.research_refresh_tiers import get_tier
    assert get_tier("AUTOCASEFORGE_LAYER") == "HEAVY"

def test_unknown_tier():
    from zmatrix.runtime.research_refresh_tiers import get_tier
    assert get_tier("NONEXISTENT_LAYER") == "UNKNOWN"
