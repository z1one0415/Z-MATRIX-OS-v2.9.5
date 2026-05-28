from zmatrix.sector_clock_foundation.matrix_clock_metadata import build_matrix_clock_metadata

def test_matrix_clock_metadata_missing():
    r = build_matrix_clock_metadata(matrix_type="B", matrix_name="B_MATRIX", as_of_date=None)
    assert r["freshness_status"] == "MISSING"
    assert r["metadata_ready"] is False
    assert r["real_trade_allowed"] is False
