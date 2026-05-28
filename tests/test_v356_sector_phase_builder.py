from zmatrix.regime_attribution.sector_phase_builder import build_sector_phase

def test_sector_phase_data_insufficient():
    r = build_sector_phase(sample={})
    assert r["phase"] == "UNKNOWN_SECTOR_PHASE"
    assert r["sector_data_status"] == "DATA_INSUFFICIENT"
    assert r["real_trade_allowed"] is False
