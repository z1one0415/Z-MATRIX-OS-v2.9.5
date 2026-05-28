from zmatrix.sector_clock_foundation.sector_phase_builder import classify_sector_phase

def test_sector_phase_unknown():
    r = classify_sector_phase(features={"feature_status":"INSUFFICIENT"})
    assert r["sector_phase"] == "UNKNOWN_SECTOR_PHASE"
    assert r["real_trade_allowed"] is False
