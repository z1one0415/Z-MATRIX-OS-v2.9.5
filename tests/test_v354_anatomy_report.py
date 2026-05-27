from zmatrix.invalidation_anatomy.anatomy_report_builder import build_invalidation_anatomy_report

def test_anatomy_report_policy():
    joined = [{"paper_id": "p1", "ticker": "000001", "entry_date": "20240101", "entry_price": 100}]
    r = build_invalidation_anatomy_report(joined=joined, data_root="/tmp/nonexistent", max_items=1)
    assert r["production_strategy_modified"] is False
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
