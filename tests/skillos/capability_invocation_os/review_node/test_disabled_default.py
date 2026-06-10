"""Tests for Z9 disabled-default config, kill switch, and default behavior."""
from skillos.capability_invocation_os.review_node.config import (
    is_z9_review_node_enabled, is_z9_runtime_enabled, is_memory_mutation_enabled,
    is_adapter_execution_enabled, is_capability_execution_enabled,
    is_paper_trading_enabled, is_trade_result_review_enabled,
    is_broker_action_enabled, is_z2_feedback_auto_apply_enabled,
    is_persistent_memory_write_enabled,
)
from skillos.capability_invocation_os.review_node.kill_switch import (
    is_master_kill_switch_active, is_z9_review_node_kill_switch_active,
    is_z9_memory_mutation_kill_switch_active, is_z9_trade_review_kill_switch_active,
    should_force_disabled,
)
from skillos.capability_invocation_os.review_node.review_builder import Z9ReviewNode

def test_all_config_enabled_false():
    assert is_z9_review_node_enabled() is False
    assert is_z9_runtime_enabled() is False
    assert is_memory_mutation_enabled() is False
    assert is_adapter_execution_enabled() is False
    assert is_capability_execution_enabled() is False
    assert is_paper_trading_enabled() is False
    assert is_trade_result_review_enabled() is False
    assert is_broker_action_enabled() is False
    assert is_z2_feedback_auto_apply_enabled() is False
    assert is_persistent_memory_write_enabled() is False

def test_all_kill_switches_active():
    assert is_master_kill_switch_active() is True
    assert is_z9_review_node_kill_switch_active() is True
    assert is_z9_memory_mutation_kill_switch_active() is True
    assert is_z9_trade_review_kill_switch_active() is True
    assert should_force_disabled() is True

def test_default_node_returns_disabled_noop():
    node = Z9ReviewNode()
    resp = node.build_disabled_default_response()
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"
    assert resp.degraded is True

def test_fixture_mode_false_noop():
    node = Z9ReviewNode(fixture_mode=False)
    resp = node.build_review_from_z2_snapshot(None)
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"
