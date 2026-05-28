from zmatrix.sector_mapping_ingestion.mapping_normalizer import normalize_mapping_sources

def test_normalize_empty():
    r = normalize_mapping_sources(source_files=[])
    assert r["normalized_count"] == 0
