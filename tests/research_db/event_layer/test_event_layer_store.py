"""G16-2A tests — EventLayer Version Store"""
import json, os, tempfile

def test_mark_layer_updated_increments_version():
    from zmatrix.research_db.event_layer_store import mark_layer_updated, get_layer_version, VERSION_STORE_PATH
    import zmatrix.research_db.event_layer_store as els
    with tempfile.TemporaryDirectory() as td:
        els.VERSION_STORE_PATH = os.path.join(td, "versions.json")
        mark_layer_updated("ACCOUNT_TRUTH_LAYER", 100)
        v = get_layer_version("ACCOUNT_TRUTH_LAYER")
        assert v is not None
        assert v["version"] >= 1
        assert v["row_count"] == 100
        assert v["freshness_status"] == "FRESH"

def test_get_layer_versions_returns_dict():
    from zmatrix.research_db.event_layer_store import get_layer_versions, mark_layer_updated, VERSION_STORE_PATH
    import zmatrix.research_db.event_layer_store as els
    with tempfile.TemporaryDirectory() as td:
        els.VERSION_STORE_PATH = os.path.join(td, "versions.json")
        mark_layer_updated("MARKET_OUTCOME_LAYER", 50)
        r = get_layer_versions()
        assert "versions" in r
        assert "MARKET_OUTCOME_LAYER" in r["versions"]

def test_get_changed_layers_detects_new_version():
    from zmatrix.research_db.event_layer_store import mark_layer_updated, get_changed_layers, VERSION_STORE_PATH
    import zmatrix.research_db.event_layer_store as els
    with tempfile.TemporaryDirectory() as td:
        els.VERSION_STORE_PATH = os.path.join(td, "versions.json")
        mark_layer_updated("PHYSICAL_SIGNAL_LAYER", 10)
        since = {"PHYSICAL_SIGNAL_LAYER": {"version": 0}}
        r = get_changed_layers(since)
        assert len(r["changed_layers"]) >= 1

def test_mark_layer_stale():
    from zmatrix.research_db.event_layer_store import mark_layer_updated, mark_layer_stale, get_layer_version, VERSION_STORE_PATH
    import zmatrix.research_db.event_layer_store as els
    with tempfile.TemporaryDirectory() as td:
        els.VERSION_STORE_PATH = os.path.join(td, "versions.json")
        mark_layer_updated("D_MATRIX_EVENT_LAYER", 5)
        mark_layer_stale("D_MATRIX_EVENT_LAYER")
        v = get_layer_version("D_MATRIX_EVENT_LAYER")
        assert v["freshness_status"] == "STALE"
