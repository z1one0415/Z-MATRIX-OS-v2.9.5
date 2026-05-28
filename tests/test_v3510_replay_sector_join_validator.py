from zmatrix.sector_mapping_ingestion.replay_sector_join_validator import validate_replay_sector_join

def test_join_coverage():
    mapping = {"000001":{"sector":"银行"},"000002":{"sector":"地产"}}
    rows = [{"ticker":"000001"},{"ticker":"000002"},{"ticker":"999999"}]
    r = validate_replay_sector_join(replay_rows=rows, sector_mapping=mapping)
    assert r["join_coverage"] == 2/3
    assert r["join_status"] == "PARTIAL"
