"""test_blocked_actions.py — All blocked_actions lists non-empty, promotion=false everywhere.

Verifies that (except F7.0 which can be empty), every gate has a non-empty
blocked_actions list, and promotion_allowed/alpha_claim_allowed are false
across the entire F7.2 gate chain.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent  # Z-MATRIX-OS root

FIXTURE_PATH = ROOT / "tests" / "skillos" / "frontend_handoff" / "state_registry" / "gate_state_demo.json"

fixture = json.loads(FIXTURE_PATH.read_text())


def test_fixture_loaded():
    assert "gates" in fixture
    assert len(fixture["gates"]) == 11


def test_f7_blocked_actions_non_empty():
    """All gates except F7.0 (stage 0) must have non-empty blocked_actions."""
    for gate in fixture["gates"]:
        if gate["gate_id"] == "F7.0-logical-reconcile":
            # F7.0 is pre-F7.2 and may have empty blocked_actions
            assert gate["blocked_actions"] == [], \
                f"F7.0 expected empty blocked_actions, got {gate['blocked_actions']}"
        else:
            assert len(gate["blocked_actions"]) > 0, \
                f"Gate {gate['gate_id']} has empty blocked_actions list"


def test_promotion_allowed_false_everywhere():
    """promotion_allowed must be false for all gates."""
    for gate in fixture["gates"]:
        assert gate["promotion_allowed"] is False, \
            f"Gate {gate['gate_id']} has promotion_allowed={gate['promotion_allowed']}"


def test_alpha_claim_allowed_false_everywhere():
    """alpha_claim_allowed must be false for all gates."""
    for gate in fixture["gates"]:
        assert gate["alpha_claim_allowed"] is False, \
            f"Gate {gate['gate_id']} has alpha_claim_allowed={gate['alpha_claim_allowed']}"


def test_paper_trading_allowed_false_everywhere():
    """paper_trading_allowed must be false for all gates."""
    for gate in fixture["gates"]:
        assert gate["paper_trading_allowed"] is False, \
            f"Gate {gate['gate_id']} has paper_trading_allowed={gate['paper_trading_allowed']}"


def test_runner_enabled_only_stage_6():
    """runner_enabled should only be true at stage 6 (F7.2-val-readonly)."""
    for gate in fixture["gates"]:
        if gate["stage"] == 6:
            assert gate["runner_enabled"] is True, \
                f"Stage 6 gate {gate['gate_id']} should have runner_enabled=true"
        else:
            assert gate["runner_enabled"] is False, \
                f"Gate {gate['gate_id']} (stage {gate['stage']}) should have runner_enabled=false, got {gate['runner_enabled']}"


def test_human_decision_required_distribution():
    """Verify expected human_decision_required flags across the chain."""
    # Gates requiring human decision: F7.2-planning, exec-plan, exec-auth, final-exec-auth,
    # human-val-auth, val-audit, human-interpret, decision-gate
    # NOT requiring: F7.0 (sealed), val-readonly (automated), safety-patch (automated)
    expected_human = {
        "F7.0-logical-reconcile": False,
        "F7.2-planning-review": True,
        "F7.2-execution-plan": True,
        "F7.2-execution-auth": True,
        "F7.2-final-exec-auth": True,
        "F7.2-human-val-auth": True,
        "F7.2-val-readonly": False,
        "F7.2-val-audit": True,
        "F7.2-safety-patch": False,
        "F7.2-human-interpret": True,
        "F7.2-decision-gate": True,
    }
    for gate in fixture["gates"]:
        expected = expected_human[gate["gate_id"]]
        assert gate["human_decision_required"] == expected, \
            f"Gate {gate['gate_id']} human_decision_required={gate['human_decision_required']}, expected={expected}"


def test_blocked_actions_include_core_safety():
    """Core blocked actions (factor_promotion, alpha_claim) must appear in all non-F7.0 gates."""
    for gate in fixture["gates"]:
        if gate["gate_id"] == "F7.0-logical-reconcile":
            continue
        blocked = gate["blocked_actions"]
        assert "factor_promotion" in blocked, \
            f"Gate {gate['gate_id']} missing 'factor_promotion' in blocked_actions: {blocked}"
        assert "alpha_claim" in blocked, \
            f"Gate {gate['gate_id']} missing 'alpha_claim' in blocked_actions: {blocked}"


def test_final_gate_blocks_everything():
    """F7.2-decision-gate should block all actions including paper_trading."""
    final = fixture["gates"][-1]
    assert final["gate_id"] == "F7.2-decision-gate"
    assert "paper_trading" in final["blocked_actions"], \
        f"Final gate missing 'paper_trading' in blocked_actions: {final['blocked_actions']}"
    assert "production_deploy" in final["blocked_actions"], \
        f"Final gate missing 'production_deploy' in blocked_actions: {final['blocked_actions']}"
    assert len(final["allowed_next_entries"]) == 0, "Final gate should have no allowed_next_entries"


