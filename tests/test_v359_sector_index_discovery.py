from zmatrix.sector_clock_foundation.sector_index_discovery import discover_sector_indexes

def test_sector_index_data_insufficient():
    r = discover_sector_indexes(data_root="/tmp/nonexistent")
    assert r["sector_index_status"] == "DATA_INSUFFICIENT"
    assert r["synthetic_sector_index_required"] is True
