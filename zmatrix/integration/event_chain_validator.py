"""Event Chain Validator — build and validate sample v3.0-alpha event chain"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.event_store.schemas import EVENT_TYPES

CHAIN_VERSION = "V3_ALPHA_EVENT_CHAIN_SAMPLE_V10"


def _sample_event(event_type: str, ticker: str = "002472",
                  parent_id: str | None = None, source_id: str | None = None) -> dict:
    seed = f"{event_type}|{ticker}|{parent_id or ''}"
    eid = hashlib.sha256(seed.encode()).hexdigest()[:32]
    return {
        "event_id": eid,
        "event_type": event_type,
        "schema_version": "EVENT_STORE_V10",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "producer_module": "zmatrix.integration.event_chain_validator",
        "source_event_id": source_id,
        "parent_event_id": parent_id,
        "payload": {"ticker": ticker, "chain_version": CHAIN_VERSION},
        "safety": {
            "real_trade_allowed": False, "real_z9_write_allowed": False,
            "hermes_memory_write_allowed": False, "append_allowed": False,
        },
    }


def build_sample_v3_alpha_event_chain() -> dict:
    """Build a sample v3.0-alpha event chain.

    PaperLedgerEvent → OutcomeBackfillEvent → MemoryCandidateEvent
    → ApprovalRequestEvent → HumanApprovalEvent
    → PromptPatchEvent → RiskEvent
    """
    paper = _sample_event("PaperLedgerEvent")
    outcome = _sample_event("OutcomeBackfillEvent", parent_id=paper["event_id"])
    memory = _sample_event("MemoryCandidateEvent", parent_id=outcome["event_id"])
    approval_req = _sample_event("ApprovalRequestEvent", parent_id=memory["event_id"])
    human_app = _sample_event("HumanApprovalEvent", parent_id=approval_req["event_id"])
    prompt = _sample_event("PromptPatchEvent", parent_id=human_app["event_id"])
    risk = _sample_event("RiskEvent", parent_id=prompt["event_id"])

    events = [paper, outcome, memory, approval_req, human_app, prompt, risk]
    edges = [
        (paper["event_id"], outcome["event_id"]),
        (outcome["event_id"], memory["event_id"]),
        (memory["event_id"], approval_req["event_id"]),
        (approval_req["event_id"], human_app["event_id"]),
        (human_app["event_id"], prompt["event_id"]),
        (prompt["event_id"], risk["event_id"]),
    ]

    return {
        "chain_version": CHAIN_VERSION,
        "mode": "SAMPLE_ONLY",
        "events": events,
        "lineage_edges": edges,
        "event_types": [e["event_type"] for e in events],
        "append_allowed": False,
        "real_z9_write_allowed": False,
        "hermes_memory_write_allowed": False,
        "real_trade_allowed": False,
    }


def validate_v3_alpha_event_chain(chain: dict) -> dict:
    """Validate a v3.0-alpha event chain."""
    violations = []

    events = chain.get("events", [])
    event_types = chain.get("event_types", [])
    edges = chain.get("lineage_edges", [])
    event_map = {e["event_id"]: e for e in events}
    type_set = set(event_types)

    for e in events:
        eid = e.get("event_id", "")
        if len(eid) != 32 or not all(c in "0123456789abcdef" for c in eid):
            violations.append(f"event_id not 32-char hex: {eid}")
        if e.get("event_type") not in EVENT_TYPES:
            violations.append(f"event_type not in EVENT_TYPES: {e.get('event_type')}")

    # Check MemoryCandidate→ApprovalRequest chain
    if "MemoryCandidateEvent" in type_set and "ApprovalRequestEvent" not in type_set:
        violations.append("MemoryCandidateEvent without ApprovalRequestEvent")
    # Check that event safety blocks auto execution
    for e in events:
        safety = e.get("safety", {})
        if safety.get("real_trade_allowed") is True:
            violations.append(f"{e.get('event_type')} has real_trade_allowed=True")

    for src, dst in edges:
        if src not in event_map:
            violations.append(f"edge source {src[:8]}... not in events")
        if dst not in event_map:
            violations.append(f"edge dest {dst[:8]}... not in events")

    return {
        "chain_version": CHAIN_VERSION,
        "mode": "SAMPLE_ONLY",
        "violations": violations,
        "pass": len(violations) == 0,
        "append_allowed": False,
        "real_z9_write_allowed": False,
        "hermes_memory_write_allowed": False,
        "real_trade_allowed": False,
    }
