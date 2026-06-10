"""Z9 Review Node degradation builders — one per decision type."""

import uuid

from skillos.capability_invocation_os.review_node.models import Z9ReviewDecision


def build_allow_z9_readonly_review_decision() -> Z9ReviewDecision:
    """Build ALLOW_Z9_READONLY_REVIEW decision."""
    return Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


def build_allow_z9_degraded_review_decision() -> Z9ReviewDecision:
    """Build ALLOW_Z9_DEGRADED_REVIEW decision."""
    return Z9ReviewDecision.ALLOW_Z9_DEGRADED_REVIEW


def build_deny_z9_source_forbidden_decision() -> Z9ReviewDecision:
    """Build DENY_Z9_SOURCE_FORBIDDEN decision."""
    return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN


def build_deny_z9_real_source_forbidden_decision() -> Z9ReviewDecision:
    """Build DENY_Z9_REAL_SOURCE_FORBIDDEN decision."""
    return Z9ReviewDecision.DENY_Z9_REAL_SOURCE_FORBIDDEN


def build_deny_z9_outputs_unsafe_decision() -> Z9ReviewDecision:
    """Build DENY_Z9_OUTPUTS_UNSAFE decision."""
    return Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE


def build_deny_z9_trade_result_forbidden_decision() -> Z9ReviewDecision:
    """Build DENY_Z9_TRADE_RESULT_FORBIDDEN decision."""
    return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN


def build_deny_z9_evidence_incomplete_decision() -> Z9ReviewDecision:
    """Build DENY_Z9_EVIDENCE_INCOMPLETE decision."""
    return Z9ReviewDecision.DENY_Z9_EVIDENCE_INCOMPLETE


def build_deny_z9_memory_mutation_forbidden_decision() -> Z9ReviewDecision:
    """Build DENY_Z9_MEMORY_MUTATION_FORBIDDEN decision."""
    return Z9ReviewDecision.DENY_Z9_MEMORY_MUTATION_FORBIDDEN


def build_deny_z9_execution_forbidden_decision() -> Z9ReviewDecision:
    """Build DENY_Z9_EXECUTION_FORBIDDEN decision."""
    return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN


def build_disabled_default_noop_decision() -> Z9ReviewDecision:
    """Build DISABLED_DEFAULT_NOOP decision."""
    return Z9ReviewDecision.DISABLED_DEFAULT_NOOP
