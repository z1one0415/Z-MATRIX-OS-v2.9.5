"""Source Health Registry v1.2 — track data source reliability"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json, os

HEALTH_LEDGER_PATH = os.environ.get("Z_SOURCE_HEALTH_LEDGER_PATH",
    os.path.join(os.path.dirname(__file__),"..","..","data","research_db","governance","source_health_ledger.jsonl"))

@dataclass
class SourceHealthEntry:
    source_id: str
    source_name: str = ""
    ok_count: int = 0
    error_count: int = 0
    last_ok: str = ""
    last_error: str = ""
    last_error_msg: str = ""
    last_duration_ms: int = 0
    avg_duration_ms: int = 0
    last_row_count: int = 0
    freshness_status: str = "UNKNOWN"
    usable_now: bool = True
    blocked_reason: str = ""
    production_allowed: bool = False


def record_source_ok(source_id: str, row_count: int = 0, duration_ms: int = 0) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "source_id": source_id, "source_name": source_id,
        "ok_count": 1, "error_count": 0,
        "last_ok": now, "last_error": "", "last_error_msg": "",
        "last_duration_ms": duration_ms, "avg_duration_ms": duration_ms,
        "last_row_count": row_count,
        "freshness_status": "FRESH" if row_count > 0 else "EMPTY",
        "usable_now": True, "blocked_reason": "",
        "production_allowed": False,
    }
    os.makedirs(os.path.dirname(HEALTH_LEDGER_PATH), exist_ok=True)
    with open(HEALTH_LEDGER_PATH, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    return entry


def record_source_error(source_id: str, error_msg: str = "") -> dict:
    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "source_id": source_id, "source_name": source_id,
        "ok_count": 0, "error_count": 1,
        "last_ok": "", "last_error": now, "last_error_msg": error_msg,
        "last_duration_ms": 0, "avg_duration_ms": 0,
        "last_row_count": 0,
        "freshness_status": "ERROR",
        "usable_now": False, "blocked_reason": error_msg,
        "production_allowed": False,
    }
    os.makedirs(os.path.dirname(HEALTH_LEDGER_PATH), exist_ok=True)
    with open(HEALTH_LEDGER_PATH, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    return entry


def get_source_health(source_id: str) -> dict | None:
    if not os.path.exists(HEALTH_LEDGER_PATH):
        return None
    entries = []
    with open(HEALTH_LEDGER_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                e = json.loads(line)
                if e.get("source_id") == source_id:
                    entries.append(e)
    if not entries:
        return None
    latest = entries[-1]
    return {
        "source_id": latest["source_id"],
        "ok_count": sum(e.get("ok_count",0) for e in entries),
        "error_count": sum(e.get("error_count",0) for e in entries),
        "last_ok": latest.get("last_ok",""),
        "last_error": latest.get("last_error",""),
        "freshness_status": latest.get("freshness_status",""),
        "usable_now": latest.get("usable_now", True),
        "blocked_reason": latest.get("blocked_reason",""),
    }


def is_source_usable(source_id: str) -> bool:
    health = get_source_health(source_id)
    if health is None:
        return False
    return health.get("usable_now", False) and health.get("freshness_status") != "ERROR"


def list_all_sources() -> list[dict]:
    if not os.path.exists(HEALTH_LEDGER_PATH):
        return []
    sources = {}
    with open(HEALTH_LEDGER_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                e = json.loads(line)
                sid = e["source_id"]
                if sid not in sources:
                    sources[sid] = {**e, "ok_count": 0, "error_count": 0}
                sources[sid]["ok_count"] += e.get("ok_count", 0)
                sources[sid]["error_count"] += e.get("error_count", 0)
    return list(sources.values())
