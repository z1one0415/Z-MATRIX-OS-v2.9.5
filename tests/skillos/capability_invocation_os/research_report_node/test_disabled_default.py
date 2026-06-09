"""Tests for disabled default behavior of Research Report Node."""

from skillos.capability_invocation_os.research_report_node.config import (
    is_research_report_node_enabled,
    is_report_runtime_enabled,
    is_report_adapter_execution_enabled,
    is_report_capability_execution_enabled,
)
from skillos.capability_invocation_os.research_report_node.kill_switch import (
    should_force_disabled,
    should_deny_all_reports,
    should_block_execution,
    should_block_alpha_output,
)
from skillos.capability_invocation_os.research_report_node.report_builder import (
    ResearchReportNode,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
)


def test_config_all_disabled():
    """All config functions return False in P0."""
    assert is_research_report_node_enabled() is False
    assert is_report_runtime_enabled() is False
    assert is_report_adapter_execution_enabled() is False
    assert is_report_capability_execution_enabled() is False


def test_kill_switch_all_active():
    """All kill switches return True in P0."""
    assert should_force_disabled() is True
    assert should_deny_all_reports() is True
    assert should_block_execution() is True
    assert should_block_alpha_output() is True


def test_default_node_returns_noop():
    """Default ResearchReportNode returns DISABLED_DEFAULT_NOOP."""
    node = ResearchReportNode()
    response = node.build_disabled_default_response()
    assert response.decision == ResearchReportDecision.DISABLED_DEFAULT_NOOP
    assert response.readonly_only is True
    assert response.report_enabled is False


def test_should_build_report_false_by_default():
    """_should_build_report returns False when killed."""
    node = ResearchReportNode(fixture_mode=True)
    assert node._should_build_report() is False


def test_build_report_from_b1_returns_noop_when_killed():
    """build_report_from_b1_graph returns noop when killed."""
    node = ResearchReportNode(fixture_mode=True)
    response = node.build_report_from_b1_graph(None)
    assert response.decision == ResearchReportDecision.DISABLED_DEFAULT_NOOP
