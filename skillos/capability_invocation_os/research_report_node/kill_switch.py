"""Research Report Node kill switch — all return True (killed) in P0."""


def should_force_disabled() -> bool:
    """Kill switch: force the report node to disabled state. Always True in P0."""
    return True


def should_deny_all_reports() -> bool:
    """Kill switch: deny all report generation. Always True in P0."""
    return True


def should_block_execution() -> bool:
    """Kill switch: block any execution path. Always True in P0."""
    return True


def should_block_alpha_output() -> bool:
    """Kill switch: block any alpha-related output. Always True in P0."""
    return True
