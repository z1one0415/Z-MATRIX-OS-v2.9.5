from zmatrix.regime_observation.matrix_clock_metadata_auditor import audit_matrix_clock_metadata

def test_clock_data_insufficient():
    r = audit_matrix_clock_metadata(rows=[{"paper_id":"p1"}])
    assert r["matrix_clock_status"] == "MATRIX_CLOCK_DATA_INSUFFICIENT"
    assert r["data_decay_penalty_required"] is True
