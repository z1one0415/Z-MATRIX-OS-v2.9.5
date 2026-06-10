"""Tests for Z9 degradation decisions."""
from skillos.capability_invocation_os.review_node.degradation import (
    build_allow_z9_readonly_review_decision as allow_z9_readonly_review,
    build_allow_z9_degraded_review_decision as allow_z9_degraded_review,
    build_deny_z9_source_forbidden_decision as deny_z9_source_forbidden,
    build_deny_z9_trade_result_forbidden_decision as deny_z9_trade_result_forbidden,
    build_deny_z9_memory_mutation_forbidden_decision as deny_z9_memory_mutation_forbidden,
    build_deny_z9_execution_forbidden_decision as deny_z9_execution_forbidden,
    build_disabled_default_noop_decision as disabled_default_noop,
)
from skillos.capability_invocation_os.review_node.models import Z9ReviewDecision

def test_allow_readonly_review():
    result = allow_z9_readonly_review()
    assert result is not None

def test_degraded_review():
    result = allow_z9_degraded_review()
    assert result is not None

def test_source_forbidden():
    result = deny_z9_source_forbidden()
    assert result is not None

def test_trade_result_forbidden():
    result = deny_z9_trade_result_forbidden()
    assert result is not None

def test_memory_mutation_forbidden():
    result = deny_z9_memory_mutation_forbidden()
    assert result is not None

def test_execution_forbidden():
    result = deny_z9_execution_forbidden()
    assert result is not None

def test_noop():
    result = disabled_default_noop()
    assert result is not None

def test_no_builders_raise():
    for builder in [allow_z9_readonly_review, allow_z9_degraded_review, deny_z9_source_forbidden,
                    deny_z9_trade_result_forbidden, deny_z9_memory_mutation_forbidden,
                    deny_z9_execution_forbidden, disabled_default_noop]:
        try:
            builder()
        except Exception:
            assert False, f"{builder.__name__} raised"
