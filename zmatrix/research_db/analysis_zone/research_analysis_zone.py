"""Research Analysis Zone v1.2 — STUB_ONLY"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

FORBIDDEN_WORDS = frozenset({
    "必涨","必跌","立即买入","立即卖出","系统确认","稳赚",
    "BUY","SELL","STRONG_BUY","STRONG_SELL","TRADE_SIGNAL",
    "production_ready","auto_execute","立即建仓","全仓买入",
})

def create_analysis_zone(zone_type, target_scope, title, body, drivers=None, uncertainties=None, required_evidence=None, created_by_agent="") -> dict:
    upper = body.upper()
    for word in FORBIDDEN_WORDS:
        if word.upper() in upper: raise ValueError(f"Analysis zone contains forbidden word: {word}")
    return {
        "zone_id": f"ZONE-{uuid.uuid4().hex[:12]}",
        "zone_type": zone_type, "target_scope": target_scope,
        "title": title, "body": body,
        "drivers": drivers or [], "uncertainties": uncertainties or [],
        "required_evidence": required_evidence or [],
        "severity": "LOW", "confidence": 0.0, "ttl_days": 30,
        "created_by_agent": created_by_agent,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "human_review_required": True, "production_allowed": False,
    }

def validate_analysis_zone(zone: dict) -> dict:
    errors = []
    if not zone.get("title"): errors.append("title required")
    if not zone.get("uncertainties"): errors.append("uncertainties required")
    if zone.get("production_allowed"): errors.append("production_allowed must be false")
    return {"valid": len(errors)==0, "errors": errors}
