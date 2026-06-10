"""Z9 Review Node kill switch — all return True (killed) in P0."""


def should_force_disabled() -> bool:
    """Kill switch: force the review node to disabled state. Always True in P0."""
    return True


def should_deny_all_reviews() -> bool:
    """Kill switch: deny all review generation. Always True in P0."""
    return True


def should_block_execution() -> bool:
    """Kill switch: block any execution path. Always True in P0."""
    return True


def should_block_memory_mutation() -> bool:
    """Kill switch: block any memory mutation. Always True in P0."""
    return True


def should_block_trade_result() -> bool:
    """Kill switch: block any trade result. Always True in P0."""
    return True


def is_z9_memory_mutation_kill_switch_active() -> bool: return True
def is_z9_trade_review_kill_switch_active() -> bool: return True

def is_master_kill_switch_active() -> bool: return True
def is_z9_review_node_kill_switch_active() -> bool: return True
