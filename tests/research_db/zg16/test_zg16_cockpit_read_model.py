"""G16-6A tests — Cockpit Read Model"""
def test_build_cockpit_read_model_valid_ticker():
    from zmatrix.research_db.zg16_cockpit_read_model import build_zg16_cockpit_read_model
    r = build_zg16_cockpit_read_model("600519")
    assert r["ticker"] == "600519"
    assert r["zg16_status"] in ("DRAFT_CHAIN_AVAILABLE", "NO_DRAFT_CHAIN")
    assert r["production_allowed"] is False
    assert r["trade_allowed"] is False
    assert r["human_review_required"] is True

def test_build_cockpit_read_model_missing_ticker():
    from zmatrix.research_db.zg16_cockpit_read_model import build_zg16_cockpit_read_model
    r = build_zg16_cockpit_read_model("")
    assert r["zg16_status"] == "DATA_INSUFFICIENT"

def test_cockpit_safety_fields():
    from zmatrix.research_db.zg16_cockpit_read_model import build_zg16_cockpit_read_model
    r = build_zg16_cockpit_read_model("600519")
    assert r["external_api_used"] is False
    assert r["shadowbroker_deployed"] is False
    assert r["verdict_allowed"] is False
