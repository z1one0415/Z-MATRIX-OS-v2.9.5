"""G16-2B tests — Source Health + Attribution"""
import os, tempfile

def test_record_source_ok():
    import zmatrix.research_db.source_health_registry as sh
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "health.jsonl")
        r = sh.record_source_ok("test-source", row_count=42)
        assert r["usable_now"] is True
        assert r["freshness_status"] == "FRESH"

def test_record_source_error_blocks_usable():
    import zmatrix.research_db.source_health_registry as sh
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "health.jsonl")
        r = sh.record_source_error("broken-source", "timeout")
        assert r["usable_now"] is False
        assert r["freshness_status"] == "ERROR"

def test_is_source_usable_after_error():
    import zmatrix.research_db.source_health_registry as sh
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "health.jsonl")
        sh.record_source_error("src1", "fail")
        assert sh.is_source_usable("src1") is False

def test_get_source_health_aggregates():
    import zmatrix.research_db.source_health_registry as sh
    with tempfile.TemporaryDirectory() as td:
        sh.HEALTH_LEDGER_PATH = os.path.join(td, "health.jsonl")
        sh.record_source_ok("src1", row_count=10)
        sh.record_source_ok("src1", row_count=20)
        h = sh.get_source_health("src1")
        assert h is not None
        assert h["ok_count"] >= 2

def test_attribution_unknown_license_blocks():
    import zmatrix.research_db.data_attribution_ledger as dal
    with tempfile.TemporaryDirectory() as td:
        dal.ATTRIBUTION_PATH = os.path.join(td, "attr.csv")
        r = dal.validate_attribution("unregistered")
        assert r["valid"] is False
