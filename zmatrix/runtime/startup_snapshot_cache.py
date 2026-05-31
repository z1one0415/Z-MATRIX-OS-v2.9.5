"""Startup Snapshot Cache v1.2 — load last snapshot on system init"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
import json, os

CACHE_ROOT = os.environ.get("Z_STARTUP_CACHE_PATH",
    os.path.join(os.path.dirname(__file__),"..","..","data","research_db","cache"))

CACHE_FILES = {
    "research_startup": "research_startup_cache.json",
    "cockpit_snapshot": "cockpit_snapshot_cache.json",
    "factor_snapshot": "last_valid_factor_snapshot.json",
    "caseforge_snapshot": "last_valid_caseforge_snapshot.json",
    "zc35_snapshot": "last_valid_zc35_snapshot.json",
}

def _cache_path(name: str) -> str:
    return os.path.join(CACHE_ROOT, CACHE_FILES.get(name, f"{name}.json"))


def load_cache(name: str) -> dict | None:
    """Load a cached snapshot. Returns None if missing or expired."""
    path = _cache_path(name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        data = json.load(f)
    if not data.get("stale_allowed", True):
        try:
            cached_at = datetime.fromisoformat(data.get("cached_at", ""))
            age = (datetime.now(timezone.utc) - cached_at).total_seconds()
            if age > data.get("max_age_seconds", 3600):
                return None
        except (ValueError, TypeError):
            return None
    return data


def save_cache(name: str, data: dict, stale_allowed: bool = False, max_age_seconds: int = 3600) -> None:
    """Save a snapshot to cache."""
    payload = {
        **data,
        "cached_at": datetime.now(timezone.utc).isoformat(),
        "stale_allowed": stale_allowed,
        "max_age_seconds": max_age_seconds,
        "production_allowed": False,
    }
    os.makedirs(CACHE_ROOT, exist_ok=True)
    with open(_cache_path(name), 'w') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def get_cache_status(name: str) -> dict:
    data = load_cache(name)
    if data is None:
        return {"status": "MISSING", "stale_allowed": False}
    return {
        "status": "STALE_CACHE" if not data.get("stale_allowed", True) else "AVAILABLE",
        "cached_at": data.get("cached_at",""),
        "age_seconds": data.get("age_seconds",0),
        "stale_allowed": data.get("stale_allowed",True),
    }
