from zmatrix.regime_observation.sector_data_auditor import audit_sector_data

def test_sector_data_insufficient():
    r = audit_sector_data(rows=[{"paper_id":"p1"}])
    assert r["sector_data_status"] == "SECTOR_DATA_INSUFFICIENT"
    assert r["sector_field_coverage"] == 0

def test_sector_data_partial():
    r = audit_sector_data(rows=[{"paper_id":"p1","sector":"fin"},{"paper_id":"p2"}])
    assert r["sector_ready_count"] == 1
    assert r["sector_missing_count"] == 1
