"""G16-6B tests — Agent Read Model Adapter"""
def test_get_agent_summary_safety():
    from zmatrix.research_db.zg16_agent_read_adapter import get_zg16_agent_summary
    r = get_zg16_agent_summary("600519")
    assert r["production_allowed"] is False
    assert r["trade_allowed"] is False
    assert r["verdict_allowed"] is False
    assert r["human_review_required"] is True

def test_get_agent_next_actions():
    from zmatrix.research_db.zg16_agent_read_adapter import get_zg16_agent_next_actions
    r = get_zg16_agent_next_actions("600519")
    assert len(r["actions"]) >= 1
    assert r["production_allowed"] is False
