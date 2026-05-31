"""ZG16 AutoCaseForge Draft Intake Adapter v7A — intake draft, NOT main write"""
from __future__ import annotations
import uuid

def build_autocaseforge_intake_draft(review_card: dict) -> dict:
    return {
        "intake_id": f"INTAKE-{uuid.uuid4().hex[:12]}",
        "source_system": "ZG16",
        "source_chain_id": review_card.get("card_id",""),
        "case_type": "DRAFT",
        "ticker": review_card.get("title","").replace("ZG16 Draft Review: ",""),
        "draft_title": review_card.get("title",""),
        "draft_summary": review_card.get("subtitle",""),
        "hypothesis_section": review_card.get("sections",{}).get("hypothesis",{}),
        "annotation_section": review_card.get("sections",{}).get("annotation",{}),
        "analysis_zone_section": review_card.get("sections",{}).get("analysis_zone",{}),
        "caseforge_section": review_card.get("sections",{}).get("caseforge_draft",{}),
        "required_human_decision": review_card.get("required_decision",[]),
        "proposal_required": True,
        "human_review_required": True,
        "production_allowed": False,
        "trade_allowed": False,
        "verdict_allowed": False,
        "autocaseforge_main_write": False,
        "runtime_ledger_written": False,
    }
