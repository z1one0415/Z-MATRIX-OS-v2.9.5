from zmatrix.return_integrity.robust_metrics import build_robust_return_metrics

def test_robust_metrics_negative_median_positive_mean():
    outcomes = [
        {"outcome_status": "READY", "actual_return_t20": -1},
        {"outcome_status": "READY", "actual_return_t20": -2},
        {"outcome_status": "READY", "actual_return_t20": 20},
    ]
    r = build_robust_return_metrics(outcomes=outcomes, horizon="t20")
    assert r["mean"] > 0
    assert r["median"] < 0
    assert r["valid_return_count"] == 3
