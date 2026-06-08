import pytest
from skillos.capability_invocation_os.adapters.factor_library.kill_switch import (
    is_master_kill_switch_active, is_factor_adapter_kill_switch_active,
    is_candidate_monitor_kill_switch_active, is_research_context_kill_switch_active,
    is_output_filter_kill_switch_active, should_force_disabled,
)

def test_all_kills_active():
    assert is_master_kill_switch_active() is True
    assert is_factor_adapter_kill_switch_active() is True
    assert is_candidate_monitor_kill_switch_active() is True
    assert is_research_context_kill_switch_active() is True
    assert is_output_filter_kill_switch_active() is True

def test_should_force_disabled():
    assert should_force_disabled() is True
