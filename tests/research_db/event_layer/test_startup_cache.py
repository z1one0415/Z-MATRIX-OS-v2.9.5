import tempfile, os, time

def test_save_and_load_cache():
    import zmatrix.runtime.startup_snapshot_cache as sc
    with tempfile.TemporaryDirectory() as td:
        sc.CACHE_ROOT = td
        sc.save_cache("research_startup", {"key": "val"}, stale_allowed=True, max_age_seconds=10)
        data = sc.load_cache("research_startup")
        assert data is not None
        assert data["key"] == "val"
        assert data["production_allowed"] is False

def test_expired_cache_returns_none():
    import zmatrix.runtime.startup_snapshot_cache as sc
    with tempfile.TemporaryDirectory() as td:
        sc.CACHE_ROOT = td
        sc.save_cache("factor_snapshot", {"key": "val"}, stale_allowed=False, max_age_seconds=0)
        data = sc.load_cache("factor_snapshot")
        assert data is None

def test_missing_cache_returns_none():
    import zmatrix.runtime.startup_snapshot_cache as sc
    with tempfile.TemporaryDirectory() as td:
        sc.CACHE_ROOT = td
        data = sc.load_cache("nonexistent")
        assert data is None
