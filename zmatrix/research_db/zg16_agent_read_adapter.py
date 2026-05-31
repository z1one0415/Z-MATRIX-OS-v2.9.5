"""ZG16 Agent Read Model Adapter v6B — compressed summary for Agent consumption"""
from __future__ import annotations

def get_zg16_agent_summary(ticker: str) -> dict:
    from .zg16_cockpit_read_model import build_zg16_cockpit_read_model
    cockpit = build_zg16_cockpit_read_model(ticker)
    return {
        "ticker": ticker,
        "summary": f"ZG16 stub chain for {ticker}: {cockpit.get('zg16_status','')}. Source readiness: {cockpit.get('source_readiness','')}.",
        "known_facts": [
            f"ZG16 draft chain status: {cockpit.get('zg16_status','')}",
            f"Latest hypothesis: {cockpit.get('latest_hypothesis_summary','')}",
        ],
        "uncertainties": ["All data is stub/fixture. No real market data ingested."],
        "required_followups": ["Add real PhysicalSignal data", "Add NarrativeEvent date series"],
        "available_skills": ["ZG16.CREATE_HYPOTHESIS_DRAFT", "ZG16.CREATE_RESEARCH_ANNOTATION_DRAFT"],
        "blocked_actions": ["REAL_TRADE", "EXTERNAL_API", "WRITE_RESEARCHDB_MAIN"],
        "human_review_required": True,
        "token_estimate": 120,
        "production_allowed": False,
        "trade_allowed": False,
        "verdict_allowed": False,
    }

def get_zg16_agent_next_actions(ticker: str) -> dict:
    from .zg16_cockpit_read_model import build_zg16_cockpit_read_model
    cockpit = build_zg16_cockpit_read_model(ticker)
    return {
        "ticker": ticker,
        "actions": [
            {"id": "R1", "label": "Review Hypothesis Draft", "type": "HUMAN_REVIEW", "skill_id": "ZG16.CREATE_HYPOTHESIS_DRAFT"},
            {"id": "R2", "label": "Add Physical Signal", "type": "DATA_INPUT", "skill_id": "ZG16.LOAD_PHYSICAL_SIGNAL_FIXTURE"},
            {"id": "R3", "label": "Submit CaseForge Draft", "type": "PROPOSAL_REQUIRED", "skill_id": "ZG16.CREATE_CASEFORGE_DRAFT_PROPOSAL"},
        ],
        "human_review_required": True,
        "production_allowed": False,
        "token_estimate": 60,
    }
