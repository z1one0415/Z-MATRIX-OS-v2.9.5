from zmatrix.sector_mapping_ingestion.mapping_validator import validate_sector_mapping

def test_validate_ready():
    mapping = {}
    for i in range(6000):
        mapping[str(i).zfill(6)] = {"sector":"test"}
    r = validate_sector_mapping(sector_mapping=mapping)
    assert r["sector_mapping_status"] == "READY"
    assert r["sector_coverage"] == 1.0
