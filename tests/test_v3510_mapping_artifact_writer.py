from zmatrix.sector_mapping_ingestion.mapping_artifact_writer import write_sector_mapping_artifact

def test_write_artifact(tmp_path):
    import os
    r = write_sector_mapping_artifact(sector_mapping={"000001":{"sector":"银行"}}, output_path="/tmp/test_sector_v3510.csv")
    assert r["row_count"] == 1
    os.remove("/tmp/test_sector_v3510.csv")
