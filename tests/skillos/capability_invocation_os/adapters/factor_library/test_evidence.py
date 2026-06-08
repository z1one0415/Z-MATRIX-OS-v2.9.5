import pytest
from skillos.capability_invocation_os.adapters.factor_library.evidence import (
    build_request_hash, build_response_hash_placeholder, build_decision_hash,
    build_c1_evidence_handoff,
)
from skillos.capability_invocation_os.adapters.factor_library.models import FactorAdapterDecision

def test_request_hash_deterministic():
    h1 = build_request_hash({"a": 1})
    h2 = build_request_hash({"a": 1})
    assert h1 == h2

def test_placeholder_exists():
    assert build_response_hash_placeholder() == "response_hash_placeholder_p0"

def test_decision_hash_deterministic():
    d = FactorAdapterDecision.DISABLED_DEFAULT_NOOP
    h1 = build_decision_hash(d)
    h2 = build_decision_hash(d)
    assert h1 == h2

def test_c1_handoff_fields_present():
    handoff = build_c1_evidence_handoff("req_hash", "dec_hash")
    assert "source_commit" in handoff
    assert "request_hash" in handoff
    assert "response_hash_placeholder" in handoff
    assert "decision_hash" in handoff
    assert "permission_tier" in handoff
    assert "source_class" in handoff
