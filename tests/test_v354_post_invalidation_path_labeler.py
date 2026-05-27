from zmatrix.invalidation_anatomy.invalidation_event_builder import build_invalidation_event
from zmatrix.invalidation_anatomy.post_invalidation_path_labeler import label_post_invalidation_path

def test_fast_recovery_label():
    sample = {"paper_id": "p1", "ticker": "000001", "entry_price": 100, "entry_date": "20240101"}
    bars = [{"trade_date": "20240101", "close": 100}, {"trade_date": "20240102", "close": 91}, {"trade_date": "20240103", "close": 96}]
    event = build_invalidation_event(sample=sample, price_bars=bars)
    label = label_post_invalidation_path(event=event, price_bars=bars)
    assert label["path_type"] == "FAST_RECOVERY"
    assert label["must_not_use_as_live_decision"] is True
