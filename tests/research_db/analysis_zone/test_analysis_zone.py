import pytest
def test_analysis_zone_requires_uncertainty():
    from zmatrix.research_db.analysis_zone.research_analysis_zone import validate_analysis_zone
    r = validate_analysis_zone({"zone_id": "x", "title": "Test"})
    assert r["valid"] is False

def test_analysis_zone_trade_words_rejected():
    from zmatrix.research_db.analysis_zone.research_analysis_zone import create_analysis_zone
    with pytest.raises(ValueError, match="forbidden"):
        create_analysis_zone("event", "600519", "Test", "立即买入该股票")

def test_analysis_zone_production_false():
    from zmatrix.research_db.analysis_zone.research_analysis_zone import create_analysis_zone, validate_analysis_zone
    z = create_analysis_zone("event", "600519", "T", "观察到了变化，不确定原因", uncertainties=["原因不明"])
    r = validate_analysis_zone(z)
    assert r["valid"] is True
    assert z["production_allowed"] is False

def test_zg16_skill_wrappers_use_agent_kernel_contract():
    from zmatrix.research_db.zg16_skill_wrappers import create_caseforge_draft_proposal
    r = create_caseforge_draft_proposal("600519", "h1", "a1")
    assert r["human_review_required"] is True
    assert r["production_allowed"] is False

def test_all_zg16_write_skills_require_human_review():
    import json
    with open("data/research_db/agent/registry/skill_registry.json") as f:
        skills = json.load(f)
    for sk in skills:
        if sk["skill_id"].startswith("ZG16") and sk.get("write_layers"):
            assert sk["requires_human_review"] is True, f"{sk['skill_id']} missing human_review"
