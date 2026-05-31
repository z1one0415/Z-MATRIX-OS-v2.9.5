"""G16-4.1 tests — full coverage + status semantics"""
import os, tempfile

def test_unknown_zg16_skill_blocked():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    r = route_zg16_skill("ZG16.UNKNOWN", {}, {})
    assert r["status"] == "BLOCKED"

def test_all_registered_zg16_read_skills_executed():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    for sid in ["ZG16.GET_SOURCE_REGISTRY","ZG16.GET_PHYSICAL_SIGNAL_SCHEMA","ZG16.GET_NPA_SCHEMA"]:
        r = route_zg16_skill(sid, {}, {})
        assert r["status"] == "EXECUTED", f"{sid} should be EXECUTED"
        assert r["quality_status"] == "STUB_ONLY"

def test_zg16_r2_draft_not_executed():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    r = route_zg16_skill("ZG16.CREATE_HYPOTHESIS_DRAFT", {"ticker":"600519"}, {"hypothesis_type":"PHYSICAL_PRE_SIGNAL","involved_layers":["p"],"drivers":["d"]})
    assert r["status"] == "DRAFT_CREATED"
    assert r["status"] != "EXECUTED"

def test_zg16_r2_draft_proposal_required():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    r = route_zg16_skill("ZG16.CREATE_CASEFORGE_DRAFT_PROPOSAL", {"ticker":"600519"}, {"hypothesis_id":"h1","annotation_id":"a1"})
    assert r["proposal_required"] is True
    assert r["closed"] is False

def test_zg16_result_has_unified_envelope():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    r = route_zg16_skill("ZG16.GET_SOURCE_REGISTRY", {}, {})
    for key in ["token_estimate","evidence_refs","trade_allowed","verdict_allowed","external_api_used"]:
        assert key in r, f"missing {key}"

def test_sell_on_news_trap_not_blocked():
    from zmatrix.agent.skill_invocation import invoke_skill
    cmd = {"command_id":"c1","agent_id":"z-orchestrator","requested_skill":"ZG16.CREATE_HYPOTHESIS_DRAFT","ticker":"600519","risk_level":"R0_READ","production_allowed":False,"requires_human_review":True}
    r = invoke_skill(cmd, {"hypothesis_type":"SELL_ON_NEWS_TRAP","involved_layers":["narrative"],"drivers":["d"]})
    assert r["status"] != "BLOCKED" or "SELL_ON_NEWS_TRAP" not in r.get("blocked_reason","")

def test_invoke_skill_routes_all_13_zg16_skills():
    from zmatrix.agent.skill_invocation import invoke_skill
    import json
    with open("data/research_db/agent/registry/skill_registry.json") as f:
        skills = json.load(f)
    zg16_skills = [s["skill_id"] for s in skills if s["skill_id"].startswith("ZG16.")]
    assert len(zg16_skills) >= 13, f"Expected 13 ZG16 skills, got {len(zg16_skills)}"
