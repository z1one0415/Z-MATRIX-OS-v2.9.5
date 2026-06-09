"""Research Report Node configuration — all disabled by default."""


def is_research_report_node_enabled() -> bool:
    """Whether the research report node is enabled. Always False in P0."""
    return False


def is_report_runtime_enabled() -> bool:
    """Whether the report runtime is enabled. Always False in P0."""
    return False


def is_report_adapter_execution_enabled() -> bool:
    """Whether adapter execution is enabled. Always False in P0."""
    return False


def is_report_capability_execution_enabled() -> bool:
    """Whether capability execution is enabled. Always False in P0."""
    return False
