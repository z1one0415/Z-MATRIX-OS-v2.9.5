def test_annotation_store_draft_only():
    from zmatrix.research_db.annotation.research_annotation_store import create_annotation
    a = create_annotation("TICKER", "600519", "observation", "Test", "Test body")
    assert a["production_allowed"] is False
    assert a["human_review_required"] is True

def test_annotation_ttl_expiry():
    from zmatrix.research_db.annotation.research_annotation_store import create_annotation, is_expired
    a = create_annotation("TICKER", "600519", "observation", "T", "B", ttl_days=0)
    assert a["ttl_days"] == 0
