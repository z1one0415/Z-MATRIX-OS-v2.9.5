from zmatrix.sector_mapping_ingestion.mapping_merger import merge_sector_mappings

def test_merge_dedup():
    rows = [{"ticker":"000001","sector":"银行","source_field":"industry"},{"ticker":"000001","sector":"金融","source_field":"sector"}]
    r = merge_sector_mappings(normalized_rows=rows)
    assert r["merged_count"] == 1
