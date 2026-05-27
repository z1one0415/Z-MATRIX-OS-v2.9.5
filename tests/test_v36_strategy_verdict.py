from zmatrix.return_integrity.strategy_verdict import build_strategy_verdict

def test_verdict_blocks_negative_median():
    r = build_strategy_verdict(robust_metrics={
        "valid_return_count": 100, "win_rate": 0.47, "mean": 1.5,
        "median": -0.7, "trimmed_mean_5pct": -0.2, "top_1pct_contribution": 0.4,
    })
    assert r["performance_status"] in ("BLOCKED_NEGATIVE_MEDIAN", "BLOCKED_LOW_WIN_RATE", "BLOCKED_OUTLIER_DOMINATED")
    assert r["live_trading_permission"] is False
