from zmatrix.sector_clock_foundation.synthetic_sector_basket import build_synthetic_sector_basket_preview

def test_synthetic_basket():
    r = build_synthetic_sector_basket_preview(sector_mapping={"000001":{"sector":"fin"},"000002":{"sector":"fin"},"000003":{"sector":"tech"}}, max_sectors=50)
    assert r["synthetic_sector_index"] is True
    assert r["production_index_allowed"] is False
    assert r["sector_count"] == 2
