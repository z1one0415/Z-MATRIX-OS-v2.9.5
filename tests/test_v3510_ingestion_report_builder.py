from zmatrix.sector_mapping_ingestion.ingestion_report_builder import build_sector_mapping_ingestion_report

def test_ingestion_report_no_runtime():
    r = build_sector_mapping_ingestion_report(data_root="/tmp/nonexistent", replay_rows=[], write_artifact=False)
    assert r["real_trade_allowed"] is False
    assert r["policy_violations"] == []
    assert "ingestion_status" in r
