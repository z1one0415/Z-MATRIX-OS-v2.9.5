from zmatrix.governance_closeout.matrix_clock_alignment_precheck import precheck_matrix_clock_alignment

def test_clock_data_insufficient():
    r = precheck_matrix_clock_alignment()
    assert r["clock_alignment_status"] == "DATA_INSUFFICIENT"
    assert r["data_decay_penalty_required"] is True
