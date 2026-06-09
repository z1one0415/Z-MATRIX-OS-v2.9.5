import pytest
import os

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.evidence import (
    build_a1_bridge_request_hash,
    build_a1_bridge_decision_hash,
    build_a1_bridge_evidence,
    build_a1_bridge_c1_handoff,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeDecision,
    A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.degradation import (
    allow_bridge_readonly_context,
)


def test_request_hash_deterministic():
    hash1 = build_a1_bridge_request_hash({"key": "value"})
    hash2 = build_a1_bridge_request_hash({"key": "value"})
    assert isinstance(hash1, str)
    assert len(hash1) == 64
    assert hash1 == hash2


def test_bridge_decision_hash_deterministic():
    decision = A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT
    hash1 = build_a1_bridge_decision_hash(decision)
    hash2 = build_a1_bridge_decision_hash(decision)
    assert isinstance(hash1, str)
    assert len(hash1) == 64
    assert hash1 == hash2


def test_evidence_includes_fixture_source_commit():
    resp = allow_bridge_readonly_context()
    evidence = build_a1_bridge_evidence(resp)
    assert isinstance(evidence, A1FactorBridgeEvidence)
    assert evidence.fixture_source_commit == "P1_FIXTURE_ONLY"


def test_evidence_includes_no_real_source_flag():
    resp = allow_bridge_readonly_context()
    evidence = build_a1_bridge_evidence(resp)
    assert evidence.no_real_source_flag is True


def test_c1_handoff_marker_present():
    resp = allow_bridge_readonly_context()
    handoff = build_a1_bridge_c1_handoff(resp)
    assert handoff["c1_handoff_marker"] is True
    assert handoff["privacy_marker"] is True
    assert handoff["rollback_marker"] is False
    assert "fixture_source_commit" in handoff


def test_no_file_write_in_evidence_source():
    """Scan evidence.py source for file I/O calls."""
    evidence_path = os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..", "..", "..",
        "skillos", "capability_invocation_os", "adapters",
        "zmatrix_factor_bridge", "evidence.py",
    )
    evidence_path = os.path.normpath(evidence_path)
    with open(evidence_path) as f:
        content = f.read()
    assert "open(" not in content
    assert ".write(" not in content
