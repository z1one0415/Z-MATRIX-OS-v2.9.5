"""ZG16 E2E Stub Draft Chain v5 — Agent Kernel invoke_skill pipeline"""
from __future__ import annotations
import uuid
from zmatrix.agent.skill_invocation import invoke_skill

def _invoke(skill_id, agent_id, cmd_extra, ctx):
    cmd = {
        "command_id": f"zg16-e2e-{uuid.uuid4().hex[:8]}",
        "agent_id": agent_id,
        "requested_skill": skill_id,
        "risk_level": "R2_DRAFT",
        "production_allowed": False,
        "requires_human_review": True,
        "action_intent": "DRAFT",
        **cmd_extra,
    }
    ctx["token_estimate"] = ctx.get("token_estimate", 800)
    return invoke_skill(cmd, ctx)


def run_zg16_e2e_stub_chain(ticker: str, hypothesis_type: str = "PHYSICAL_PRE_SIGNAL", agent_id: str = "z-orchestrator") -> dict:
    if not ticker:
        return {
            "chain_status": "BLOCKED", "quality_status": "DATA_INSUFFICIENT",
            "blocked_reason": "ticker is required",
            "production_allowed": False, "trade_allowed": False,
            "verdict_allowed": False, "external_api_used": False,
            "shadowbroker_deployed": False,
        }

    chain_id = f"CHAIN-{uuid.uuid4().hex[:12]}"

    # Step 1: Hypothesis Draft
    h_result = _invoke("ZG16.CREATE_HYPOTHESIS_DRAFT", agent_id, {"ticker": ticker}, {
        "hypothesis_type": hypothesis_type,
        "involved_layers": ["physical_signal", "narrative_event"],
        "drivers": ["stub physical signal", "stub narrative divergence"],
    })
    if h_result.get("status") == "BLOCKED":
        return _chain_blocked(chain_id, "hypothesis_draft", h_result.get("blocked_reason", ""))

    # Step 2: Annotation Draft
    a_result = _invoke("ZG16.CREATE_RESEARCH_ANNOTATION_DRAFT", agent_id, {}, {
        "target_type": "TICKER", "target_id": ticker,
        "category": "hypothesis",
        "title": f"ZG16 hypothesis draft for {ticker}",
        "body": "Stub annotation generated from ZG16 hypothesis draft. Human review required.",
    })
    if a_result.get("status") == "BLOCKED":
        return _chain_blocked(chain_id, "annotation_draft", a_result.get("blocked_reason", ""))

    # Step 3: Analysis Zone Draft
    z_result = _invoke("ZG16.CREATE_ANALYSIS_ZONE_DRAFT", agent_id, {}, {
        "zone_type": "e2e_stub_chain",
        "target_scope": ticker,
        "title": f"ZG16 E2E analysis for {ticker}",
        "body": f"观察到: {ticker} 在 stub fixture 中有 physical signal 与 narrative divergence。可能意味着: 存在预判信号与叙事不一致。不确定: 真实市场是否已定价。还需要: 真实 PhysicalSignal 数据、NarrativeEvent 日期序列、Outcome 验证。",
    })
    if z_result.get("status") == "BLOCKED":
        return _chain_blocked(chain_id, "analysis_zone_draft", z_result.get("blocked_reason", ""))

    # Step 4: CaseForge Draft Proposal
    c_result = _invoke("ZG16.CREATE_CASEFORGE_DRAFT_PROPOSAL", agent_id, {"ticker": ticker}, {
        "hypothesis_id": h_result.get("output", {}).get("hypothesis_id", ""),
        "annotation_id": a_result.get("output", {}).get("annotation_id", ""),
    })
    if c_result.get("status") == "BLOCKED":
        return _chain_blocked(chain_id, "caseforge_draft", c_result.get("blocked_reason", ""))

    return {
        "chain_id": chain_id,
        "chain_status": "DRAFT_CHAIN_CREATED",
        "quality_status": "STUB_E2E",
        "ticker": ticker,
        "hypothesis_type": hypothesis_type,
        "hypothesis_draft": h_result,
        "annotation_draft": a_result,
        "analysis_zone_draft": z_result,
        "caseforge_draft_proposal": c_result,
        "human_review_required": True,
        "proposal_required": True,
        "closed": False,
        "production_allowed": False,
        "external_api_used": False,
        "shadowbroker_deployed": False,
        "trade_allowed": False,
        "verdict_allowed": False,
        "runtime_ledger_written": False,
        "researchdb_main_write": False,
        "evidence_refs": [],
        "blocked_reason": "",
    }


def _chain_blocked(chain_id, failed_step, reason):
    return {
        "chain_id": chain_id,
        "chain_status": "BLOCKED",
        "quality_status": "SKILL_CHAIN_BLOCKED",
        "blocked_reason": reason,
        "failed_step": failed_step,
        "production_allowed": False,
        "trade_allowed": False,
        "verdict_allowed": False,
        "external_api_used": False,
        "shadowbroker_deployed": False,
        "runtime_ledger_written": False,
        "researchdb_main_write": False,
    }
