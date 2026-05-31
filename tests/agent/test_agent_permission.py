# allowlist: forbidden-token-definition
"""Tests for agent_permission — risk-level gate evaluator"""
from __future__ import annotations

from zmatrix.agent.agent_permission import evaluate_agent_permission


VIEW_ONLY_AGENT = {
    "agent_id": "z-orchestrator",
    "permission_level": "VIEW_ONLY",
    "max_risk_level": "R2_DRAFT",
    "requires_human_review": True,
}

CODE_PATCH_AGENT = {
    "agent_id": "openclaw-engineering",
    "permission_level": "CODE_PATCH_PROPOSER",
    "max_risk_level": "R4_CODE_PATCH_PROPOSAL",
    "requires_human_review": True,
}


def _cmd(**overrides):
    base = {
        "command_id": "cmd-1",
        "agent_id": "z-orchestrator",
        "risk_level": "R0_READ",
        "production_allowed": False,
        "requires_human_review": True,
    }
    base.update(overrides)
    return base


class TestEvaluateAgentPermission:

    def test_view_only_agent_r3_command_rejects(self):
        result = evaluate_agent_permission(VIEW_ONLY_AGENT, _cmd(risk_level="R3_WRITE_RESEARCH_DB"))
        assert result["allowed"] is False
        assert any("VIEW_ONLY" in r for r in result["blocked_reasons"])

    def test_view_only_agent_r0_command_allows(self):
        result = evaluate_agent_permission(VIEW_ONLY_AGENT, _cmd(risk_level="R0_READ"))
        assert result["allowed"] is True
        assert result["blocked_reasons"] == []

    def test_r3_command_requires_human_review(self):
        result = evaluate_agent_permission(VIEW_ONLY_AGENT, _cmd(risk_level="R3_WRITE_RESEARCH_DB"))
        assert result["requires_human_review"] is True

    def test_r9_command_always_blocked(self):
        result = evaluate_agent_permission(CODE_PATCH_AGENT, _cmd(risk_level="R9_FORBIDDEN"))
        assert result["allowed"] is False
        assert any("R9_FORBIDDEN" in r for r in result["blocked_reasons"])

    def test_production_allowed_true_in_command_blocked(self):
        result = evaluate_agent_permission(VIEW_ONLY_AGENT, _cmd(production_allowed=True))
        assert result["allowed"] is False
        assert any("production_allowed" in r for r in result["blocked_reasons"])

    def test_r4_command_with_human_review_false_blocked(self):
        cmd = _cmd(
            risk_level="R4_CODE_PATCH_PROPOSAL",
            requires_human_review=False,
        )
        result = evaluate_agent_permission(CODE_PATCH_AGENT, cmd)
        assert result["allowed"] is False
        assert any("requires_human_review" in r for r in result["blocked_reasons"])
