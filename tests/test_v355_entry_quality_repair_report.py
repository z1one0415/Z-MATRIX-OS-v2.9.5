from zmatrix.entry_quality_repair.repair_report_builder import build_entry_quality_repair_report

def test_entry_quality_repair_report_no_runtime():
    joined = [{"paper_id": "p1", "ticker": "000001", "entry_date": "20240101", "actual_return_t20": -2}]
    r = build_entry_quality_repair_report(joined=joined, data_root="/tmp/nonexistent", max_items=1)
    assert r["production_strategy_modified"] is False
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
