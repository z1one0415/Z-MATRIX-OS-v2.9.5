"""ZG16 System Integration Cockpit v9 — unified system status snapshot"""
from __future__ import annotations

def build_zg16_system_status(ticker: str = "600519") -> dict:
    from .zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    from .zg16_cockpit_read_model import build_zg16_cockpit_read_model
    from .zg16_query_bridge import get_zg16_research_summary
    from .zg16_skill_router import _ROUTE_MAP

    chain = run_zg16_e2e_stub_chain(ticker)
    cockpit = build_zg16_cockpit_read_model(ticker)
    summary = get_zg16_research_summary()

    return {
        "ticker": ticker,
        "zg16_stage_status": "G16_1_to_8_STUB_INTEGRATION",
        "agent_kernel_status": "ZK_READY_FOR_ZG16_STUB_INTEGRATION",
        "query_bridge_status": "G16_3_QUERY_BRIDGE_READY",
        "skill_invocation_status": "G16_4_SKILL_INVOCATION_BRIDGE_READY",
        "e2e_chain_status": chain.get("chain_status",""),
        "cockpit_read_model_status": "G16_6_COCKPIT_READ_MODEL_READY",
        "autocaseforge_intake_status": "G16_7_INTAKE_READY",
        "memory_candidate_status": "G16_8_CANDIDATE_READY",

        "available_read_models": ["cockpit_read_model","agent_read_adapter","review_ui_contract"],
        "available_agent_skills": list(_ROUTE_MAP.keys()),
        "available_review_contracts": ["review_card","autocaseforge_intake","memory_candidate"],

        "runtime_ledgers_empty": True,
        "external_api_used": False,
        "shadowbroker_deployed": False,
        "production_allowed": False,
        "broker_runtime_allowed": False,
        "real_trade_allowed": False,
        "trade_allowed": False,
        "verdict_allowed": False,

        "next_allowed_steps": ["G16-10 full closeout", "merge readiness audit"],
        "forbidden_steps": ["external API", "ShadowBroker deploy", "production", "broker", "real trade", "autonomous runtime"],
        "known_limitations": ["Stub only", "Fixture data only", "No real ingestion", "No persistence to main ledger"],
    }
