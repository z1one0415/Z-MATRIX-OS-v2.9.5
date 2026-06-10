"""Z9 Review Node configuration — all disabled by default in P0."""


def is_z9_review_node_enabled() -> bool:
    """Whether the Z9 review node is enabled. Always False in P0."""
    return False


def is_review_runtime_enabled() -> bool:
    """Whether the review runtime is enabled. Always False in P0."""
    return False


def is_review_adapter_execution_enabled() -> bool:
    """Whether adapter execution is enabled. Always False in P0."""
    return False


def is_review_capability_execution_enabled() -> bool:
    """Whether capability execution is enabled. Always False in P0."""
    return False


def is_z9_memory_mutation_enabled() -> bool:
    """Whether memory mutation is enabled. Always False in P0."""
    return False


def is_z9_runtime_enabled() -> bool: return False
def is_memory_mutation_enabled() -> bool: return False
def is_adapter_execution_enabled() -> bool: return False
def is_capability_execution_enabled() -> bool: return False
def is_paper_trading_enabled() -> bool: return False
def is_trade_result_review_enabled() -> bool: return False
def is_broker_action_enabled() -> bool: return False
def is_z2_feedback_auto_apply_enabled() -> bool: return False
def is_persistent_memory_write_enabled() -> bool: return False
