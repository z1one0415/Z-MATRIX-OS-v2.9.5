from zmatrix.return_integrity.return_sanity_guard import classify_return_sanity

def test_return_outlier_flag():
    r = classify_return_sanity({"paper_id": "p1", "ticker": "000001", "outcome_status": "READY", "actual_return_t20": 200})
    assert r["is_outlier"] is True
    assert "T20_RETURN_OUTLIER" in r["flags"]
