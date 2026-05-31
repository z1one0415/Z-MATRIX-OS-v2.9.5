"""G16-4 tests — ZG16 Skill Router"""
import os, tempfile

def test_unknown_zg16_skill_blocked():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    r = route_zg16_skill("ZG16.UNKNOWN", {}, {})
    assert r["status"] == "BLOCKED"
    assert "Unknown ZG16 skill" in r.get("blocked_reason","")

def test_zg16_skill_result_no_trade():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    import zmatrix.research_db.source_health_registry as sh
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "h.jsonl")
        r = route_zg16_skill("ZG16.LOAD_PHYSICAL_SIGNAL_FIXTURE", {"ticker":"600519"}, {})
        assert r["trade_allowed"] is False
        assert r["verdict_allowed"] is False
        assert r["production_allowed"] is False

def test_zg16_skill_result_human_review():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    import zmatrix.research_db.source_health_registry as sh
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "h.jsonl")
        r = route_zg16_skill("ZG16.CREATE_HYPOTHESIS_DRAFT", {"ticker":"600519"}, {"hypothesis_type":"PHYSICAL_PRE_SIGNAL","involved_layers":["p"],"drivers":["d"]})
        assert r["human_review_required"] is True

def test_invoke_skill_routes_zg16():
    from zmatrix.agent.skill_invocation import invoke_skill
    import zmatrix.research_db.source_health_registry as sh
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "h.jsonl")
        cmd = {"command_id":"c1","agent_id":"z-orchestrator","requested_skill":"ZG16.LOAD_PHYSICAL_SIGNAL_FIXTURE","ticker":"600519","risk_level":"R0_READ","production_allowed":False,"requires_human_review":True}
        r = invoke_skill(cmd, {})
        assert r["status"] in ("DRAFT_CREATED","EXECUTED")
        assert r["production_allowed"] is False

def test_npa_score_returns_valid():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    r = route_zg16_skill("ZG16.CALCULATE_NPA_SCORE", {}, {"narrative_score":0.7,"physical_score":0.3})
    assert r["status"] in ("DRAFT_CREATED","EXECUTED")

def test_annotation_draft_returns_valid():
    from zmatrix.research_db.zg16_skill_router import route_zg16_skill
    r = route_zg16_skill("ZG16.CREATE_RESEARCH_ANNOTATION_DRAFT", {}, {"target_type":"TICKER","target_id":"600519","category":"observation","title":"T","body":"B"})
    assert r["status"] in ("DRAFT_CREATED","EXECUTED")
