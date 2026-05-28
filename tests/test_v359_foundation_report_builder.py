from zmatrix.sector_clock_foundation.foundation_report_builder import build_sector_clock_foundation_report

def test_foundation_report_no_runtime():
    r = build_sector_clock_foundation_report(replay_rows=[], data_root="/tmp/nonexistent")
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    assert r["production_yaml_write_allowed"] is False
    assert r["policy_violations"] == []
    assert "foundation_status" in r
