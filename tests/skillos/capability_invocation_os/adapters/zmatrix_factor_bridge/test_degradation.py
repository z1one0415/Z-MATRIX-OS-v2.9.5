import pytest
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.degradation import (
    allow_bridge_readonly_context,
    allow_bridge_evidence_summary,
    deny_bridge_source_forbidden,
    deny_bridge_real_source_forbidden,
    deny_bridge_outputs_unsafe,
    deny_bridge_execution_forbidden,
    deny_bridge_factor_denied,
    disabled_default_noop,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeDecision,
)


BUILDERS = [
    (allow_bridge_readonly_context, A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT, False),
    (allow_bridge_evidence_summary, A1FactorBridgeDecision.ALLOW_BRIDGE_EVIDENCE_SUMMARY, False),
    (deny_bridge_source_forbidden, A1FactorBridgeDecision.DENY_BRIDGE_SOURCE_FORBIDDEN, True),
    (deny_bridge_real_source_forbidden, A1FactorBridgeDecision.DENY_BRIDGE_REAL_SOURCE_FORBIDDEN, True),
    (deny_bridge_outputs_unsafe, A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE, True),
    (deny_bridge_execution_forbidden, A1FactorBridgeDecision.DENY_BRIDGE_EXECUTION_FORBIDDEN, True),
    (deny_bridge_factor_denied, A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED, True),
    (disabled_default_noop, A1FactorBridgeDecision.DISABLED_DEFAULT_NOOP, True),
]


def test_all_builders_return_correct_decision():
    for builder_fn, expected_decision, expected_degraded in BUILDERS:
        resp = builder_fn()
        assert isinstance(resp, A1FactorBridgeResponse)
        assert resp.decision == expected_decision, f"{builder_fn.__name__}: expected {expected_decision}, got {resp.decision}"
        assert resp.degraded == expected_degraded, f"{builder_fn.__name__}: expected degraded={expected_degraded}"


def test_no_builder_raises():
    for builder_fn, _, _ in BUILDERS:
        try:
            resp = builder_fn()
            assert isinstance(resp, A1FactorBridgeResponse)
        except Exception as e:
            pytest.fail(f"{builder_fn.__name__} raised {e}")


def test_no_fail_closed_all_return_structured():
    for builder_fn, _, _ in BUILDERS:
        resp = builder_fn()
        assert isinstance(resp, A1FactorBridgeResponse)
        assert resp.response_id != ""


def test_denied_factor_degraded():
    resp = deny_bridge_factor_denied()
    assert resp.decision == A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED
    assert resp.degraded is True
