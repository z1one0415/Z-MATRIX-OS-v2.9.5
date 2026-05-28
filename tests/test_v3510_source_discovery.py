from zmatrix.sector_mapping_ingestion.source_discovery import discover_mapping_sources

def test_source_discovery():
    r = discover_mapping_sources(data_root="/tmp/nonexistent")
    assert r["source_status"] == "DATA_INSUFFICIENT"
