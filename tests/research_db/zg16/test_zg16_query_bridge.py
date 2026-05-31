"""G16-3.1 tests — ZG16 Query Bridge"""
import os, tempfile

def test_summary_has_envelope():
    from zmatrix.research_db.zg16_query_bridge import get_zg16_research_summary
    r = get_zg16_research_summary()
    assert r["status"] == "OK"
    assert r["quality_status"] == "STUB_ONLY"
    assert r["production_allowed"] is False
    assert "token_estimate" in r

def test_layer_slice_limit():
    from zmatrix.research_db.zg16_query_bridge import get_zg16_layer_slice
    assert get_zg16_layer_slice([], 0)["code"] == "NEED_NARROWER_QUERY"
    assert get_zg16_layer_slice([], 101)["code"] == "NEED_NARROWER_QUERY"

def test_source_not_registered():
    import zmatrix.research_db.source_health_registry as sh
    from zmatrix.research_db.zg16_query_bridge import get_zg16_source_health
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "h.jsonl")
        r = get_zg16_source_health("nonexistent")
        assert r["quality_status"] == "SOURCE_NOT_REGISTERED"

def test_source_error_blocked():
    import zmatrix.research_db.source_health_registry as sh
    from zmatrix.research_db.zg16_query_bridge import get_zg16_source_readiness
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "h.jsonl")
        sh.record_source_error("src1", "timeout")
        assert get_zg16_source_readiness("src1") == "DATA_SOURCE_BLOCKED"

def test_source_ready():
    import zmatrix.research_db.source_health_registry as sh
    from zmatrix.research_db.zg16_query_bridge import get_zg16_source_readiness
    import zmatrix.research_db.data_attribution_ledger as dal
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "h.jsonl")
        sh.record_source_ok("src1", row_count=10)
        dal.ATTRIBUTION_PATH = os.path.join(td, "attr.csv")
        with open(dal.ATTRIBUTION_PATH, 'w') as f:
            f.write("source_id,source_name,license,attribution_required,commercial_allowed,redistribution_allowed,research_only,usable_for_backtest,usable_for_current_snapshot,usable_for_report,notes\n")
            f.write("src1,Test,MIT,false,true,true,true,true,true,true,ok\n")
        assert get_zg16_source_readiness("src1") == "SOURCE_READY"

def test_license_unknown_requires_review():
    import zmatrix.research_db.source_health_registry as sh
    from zmatrix.research_db.zg16_query_bridge import get_zg16_source_readiness
    import zmatrix.research_db.data_attribution_ledger as dal
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "h.jsonl")
        sh.record_source_ok("src1", row_count=5)
        dal.ATTRIBUTION_PATH = os.path.join(td, "attr.csv")
        # No attribution record → license unknown
        assert get_zg16_source_readiness("src1") == "LICENSE_REVIEW_REQUIRED"
