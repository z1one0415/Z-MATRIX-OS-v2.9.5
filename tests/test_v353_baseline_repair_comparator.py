from zmatrix.paper_repair_replay.baseline_repair_comparator import compare_baseline_vs_repaired

def test_compare_baseline_vs_repaired():
    repaired = {"rows": [{"baseline_return_t20": -20, "simulation": {"simulation_status": "READY", "repaired_return": -8}}, {"baseline_return_t20": 5, "simulation": {"simulation_status": "READY", "repaired_return": 5}}]}
    r = compare_baseline_vs_repaired(repaired_result=repaired)
    assert r["repaired"]["median"] > r["baseline"]["median"]
    assert r["real_trade_allowed"] is False
