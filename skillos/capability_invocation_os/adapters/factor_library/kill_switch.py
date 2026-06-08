"""Kill switch — all active in P0. Forces disabled."""
def is_master_kill_switch_active() -> bool: return True
def is_factor_adapter_kill_switch_active() -> bool: return True
def is_candidate_monitor_kill_switch_active() -> bool: return True
def is_research_context_kill_switch_active() -> bool: return True
def is_output_filter_kill_switch_active() -> bool: return True
def should_force_disabled() -> bool: return True
