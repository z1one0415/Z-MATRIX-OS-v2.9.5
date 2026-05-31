"""ZG16 Cockpit Read Model v6A — read-only cockpit data contract"""
from __future__ import annotations

def build_zg16_cockpit_read_model(ticker: str) -> dict:
    if not ticker:
        return _status("DATA_INSUFFICIENT", "ticker is required")

    from .zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    from .zg16_query_bridge import get_zg16_source_readiness

    readiness = get_zg16_source_readiness("fixture")
    chain = run_zg16_e2e_stub_chain(ticker)

    return {
        "ticker": ticker,
        "zg16_status": "DRAFT_CHAIN_AVAILABLE" if chain.get("chain_status") == "DRAFT_CHAIN_CREATED" else "NO_DRAFT_CHAIN",
        "source_readiness": readiness,
        "latest_hypothesis_summary": _extract_summary(chain.get("hypothesis_draft", {})),
        "annotation_summary": _extract_summary(chain.get("annotation_draft", {})),
        "analysis_zone_summary": _extract_summary(chain.get("analysis_zone_draft", {})),
        "caseforge_draft_summary": _extract_summary(chain.get("caseforge_draft_proposal", {})),
        "next_required_human_action": "REVIEW_DRAFT_CHAIN" if chain.get("chain_status") == "DRAFT_CHAIN_CREATED" else "ADD_DATA",
        "risk_flags": [],
        "data_freshness": "STUB",
        "quality_status": "STUB_ONLY",
        "human_review_required": True,
        "production_allowed": False,
        "external_api_used": False,
        "shadowbroker_deployed": False,
        "trade_allowed": False,
        "verdict_allowed": False,
    }

def _status(status, reason):
    return {"ticker":"","zg16_status":status,"blocked_reason":reason,"production_allowed":False,"trade_allowed":False,"verdict_allowed":False}

def _extract_summary(draft: dict) -> str:
    out = draft.get("output", {})
    if isinstance(out, dict):
        return out.get("title", out.get("hypothesis_type", out.get("body", "N/A")))
    return "N/A"
