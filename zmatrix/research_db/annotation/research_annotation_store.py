"""Research Annotation Store v1.2 — STUB_ONLY"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import uuid

VALID_CATEGORIES = {"observation","hypothesis","warning","contradiction","review_needed","data_quality","behavior_pattern"}
VALID_TARGETS = {"TICKER","CASE","EVENT","FACTOR","INDUSTRY","CHAIN","ACCOUNT_PERIOD","WATCH_AREA","REPORT"}

def create_annotation(target_type, target_id, category, title, body, source_agent_id="", ttl_days=30) -> dict:
    if target_type not in VALID_TARGETS: raise ValueError(f"Invalid target_type: {target_type}")
    if category not in VALID_CATEGORIES: raise ValueError(f"Invalid category: {category}")
    now = datetime.now(timezone.utc)
    return {
        "annotation_id": f"ANN-{uuid.uuid4().hex[:12]}",
        "target_type": target_type, "target_id": target_id, "category": category,
        "title": title, "body": body, "source_agent_id": source_agent_id,
        "ttl_days": ttl_days, "created_at": now.isoformat(),
        "expires_at": (now + timedelta(days=ttl_days)).isoformat(),
        "severity": "LOW", "confidence": 0.0,
        "human_review_required": True, "production_allowed": False,
    }

def is_expired(annotation: dict) -> bool:
    try:
        expires = datetime.fromisoformat(annotation.get("expires_at", ""))
        return datetime.now(timezone.utc) > expires
    except (ValueError, TypeError): return False
