"""ZG16 Review UI Contract v6C — CaseForge Draft Review card builder"""
from __future__ import annotations
import uuid

def build_zg16_review_card(chain_result: dict) -> dict:
    ticker = chain_result.get("ticker","")
    return {
        "card_id": f"CARD-{uuid.uuid4().hex[:12]}",
        "title": f"ZG16 Draft Review: {ticker}",
        "subtitle": f"Chain: {chain_result.get('chain_status','UNKNOWN')}",
        "sections": {
            "hypothesis": _section("Hypothesis", chain_result.get("hypothesis_draft",{})),
            "annotation": _section("Annotation", chain_result.get("annotation_draft",{})),
            "analysis_zone": _section("Analysis Zone", chain_result.get("analysis_zone_draft",{})),
            "caseforge_draft": _section("CaseForge Draft", chain_result.get("caseforge_draft_proposal",{})),
        },
        "required_decision": ["APPROVE_DRAFT_TO_PROPOSAL", "REQUEST_MORE_EVIDENCE", "REJECT_DRAFT"],
        "safety_badges": ["STUB_ONLY", "HUMAN_REVIEW_REQUIRED", "NO_TRADE", "NO_PRODUCTION"],
        "evidence_refs": chain_result.get("evidence_refs", []),
        "human_review_required": True,
        "production_allowed": False,
        "trade_allowed": False,
        "verdict_allowed": False,
    }

def _section(title, draft):
    out = draft.get("output", {})
    return {"title": title, "status": draft.get("status","N/A"), "summary": str(out)[:200]}
