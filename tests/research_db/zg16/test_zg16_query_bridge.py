"""G16-3A tests — ZG16 Query Bridge"""
import os, tempfile

def test_get_zg16_research_summary():
    from zmatrix.research_db.zg16_query_bridge import get_zg16_research_summary
    r = get_zg16_research_summary()
    assert r["status"] == "STUB_ONLY" and r["production_allowed"] is False and r["external_api_used"] is False

def test_get_zg16_layer_slice_respects_limit():
    from zmatrix.research_db.zg16_query_bridge import get_zg16_layer_slice
    assert get_zg16_layer_slice([], limit=0)["code"] == "NEED_NARROWER_QUERY"
    assert get_zg16_layer_slice([], limit=101)["code"] == "NEED_NARROWER_QUERY"

def test_get_zg16_source_attribution_nonexistent():
    import zmatrix.research_db.data_attribution_ledger as dal
    from zmatrix.research_db.zg16_query_bridge import get_zg16_source_attribution
    with tempfile.TemporaryDirectory() as td:
        dal.ATTRIBUTION_PATH = os.path.join(td, "attr.csv")
        assert get_zg16_source_attribution("nonexistent") is None

def test_get_zg16_all_sources_empty():
    import zmatrix.research_db.source_health_registry as sh
    from zmatrix.research_db.zg16_query_bridge import get_zg16_all_sources
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "h.jsonl")
        r = get_zg16_all_sources()
        assert r["total"] >= 0
        assert "token_estimate" in r
