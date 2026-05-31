"""G16-E: skill registry contract validation"""
import json, os

def _load_skills():
    with open("data/research_db/agent/registry/skill_registry.json") as f:
        return json.load(f)

def test_all_skills_have_input_output_schema_refs():
    for sk in _load_skills():
        assert "input_schema_ref" in sk, f"{sk['skill_id']} missing input_schema_ref"
        assert "output_schema_ref" in sk, f"{sk['skill_id']} missing output_schema_ref"

def test_zg16_read_skills_have_read_layers():
    for sk in _load_skills():
        if sk["skill_id"].startswith("ZG16.GET_"):
            assert sk.get("read_layers"), f"{sk['skill_id']} missing read_layers"
            assert sk.get("risk_level") == "R0_READ"

def test_zg16_write_skills_have_write_layers():
    for sk in _load_skills():
        if sk["skill_id"].startswith("ZG16.CREATE_"):
            assert sk.get("write_layers"), f"{sk['skill_id']} missing write_layers"

def test_zg16_write_skills_require_human_review():
    for sk in _load_skills():
        if sk.get("write_layers"):
            assert sk["requires_human_review"] is True, f"{sk['skill_id']} human_review not required"

def test_no_zg16_skill_production_allowed():
    for sk in _load_skills():
        if sk["skill_id"].startswith("ZG16"):
            assert sk.get("production_allowed") is False, f"{sk['skill_id']} production allowed"

def test_all_zg16_wrappers_callable():
    from zmatrix.research_db.zg16_skill_wrappers import (
        load_physical_signal_fixture, calculate_npa_score, create_hypothesis_draft,
        create_research_annotation_draft, create_analysis_zone_draft, create_caseforge_draft_proposal,
    )
    assert load_physical_signal_fixture("600519")["status"] == "DRAFT_CREATED"
    r = calculate_npa_score(0.7, 0.3)
    assert r["trade_allowed"] is False
    h = create_hypothesis_draft("PHYSICAL_PRE_SIGNAL", "600519", ["p"], ["d"])
    assert h["trade_allowed"] is False
    a = create_research_annotation_draft("TICKER", "600519", "observation", "T", "B")
    assert a["production_allowed"] is False
    z = create_analysis_zone_draft("event", "600519", "T", "observing change, uncertain why")
    assert z["production_allowed"] is False
    c = create_caseforge_draft_proposal("600519", "h1", "a1")
    assert c["human_review_required"] is True
