"""ZG16 Memory Candidate Adapter v8A — monthly memory candidate, NOT main write"""
from __future__ import annotations
import uuid

def build_monthly_memory_candidate(intake_draft: dict) -> dict:
    return {
        "memory_candidate_id": f"MEMCAND-{uuid.uuid4().hex[:12]}",
        "source_system": "ZG16",
        "candidate_type": "CASE_MEMORY_CANDIDATE",
        "ticker": intake_draft.get("ticker",""),
        "candidate_summary": intake_draft.get("draft_summary",""),
        "why_it_matters": f"ZG16 detected draft chain for {intake_draft.get('ticker','')}. Requires human review before memory internalization.",
        "evidence_refs": [],
        "required_validation": ["REVIEW_BY_HUMAN", "VERIFY_EVIDENCE", "CONFIRM_OUTCOME"],
        "ttl_days": 30,
        "memory_status": "CANDIDATE_ONLY",
        "human_review_required": True,
        "production_allowed": False,
        "memory_main_write": False,
        "researchdb_main_write": False,
        "trade_allowed": False,
        "verdict_allowed": False,
    }
