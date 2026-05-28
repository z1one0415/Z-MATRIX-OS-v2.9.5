from zmatrix.sector_clock_foundation.stock_sector_joiner import join_stock_sector_mapping

def test_join_data_insufficient():
    r = join_stock_sector_mapping(rows=[{"ticker":"000001","paper_id":"p1"}], sector_mapping={})
    assert r["sector_join_status"] == "DATA_INSUFFICIENT"
    assert r["sector_join_coverage"] == 0
