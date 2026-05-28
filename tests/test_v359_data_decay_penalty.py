from zmatrix.sector_clock_foundation.data_decay_penalty import calculate_data_decay_penalty

def test_decay_data_insufficient():
    r = calculate_data_decay_penalty(matrix_type="B", age_days=None, ttl_days=None)
    assert r["decay_status"] == "DECAY_DATA_INSUFFICIENT"
    assert r["production_weight_adjustment_allowed"] is False
