from zmatrix.sector_clock_foundation.sector_mapping_discovery import discover_sector_mapping

def test_sector_mapping_data_insufficient():
    r = discover_sector_mapping(data_root="/tmp/nonexistent")
    assert r["sector_mapping_status"] == "DATA_INSUFFICIENT"
    assert r["ticker_count"] == 0
