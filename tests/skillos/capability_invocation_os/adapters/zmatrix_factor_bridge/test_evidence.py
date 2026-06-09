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
    assert evidence.fixture_source_commit in ("P1_FIXTURE_ONLY", "DISABLED_DEFAULT")


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
from unittest.mock import MagicMock
import uuid


def test_bridge_evidence_inherits_fixture_source_fields():
    """Bridge evidence must inherit source_class, no_real_source_flag, fixture_source_commit from source factor."""
    from skillos.capability_invocation_os.adapters.factor_library.models import (
        FactorInvocationResponse,
        FactorAdapterDecision,
        FactorEvidenceEnvelopeView,
    )
    from skillos.capability_invocation_os.adapters.factor_library.constants import (
        BLOCKED_OUTPUTS,
    )

    source_evidence = FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        request_hash="test_req_hash_abc123",
        decision_hash="test_dec_hash_xyz",
        factor_manifest_hash="test_factor_manifest",
        validation_snapshot_hash="test_val_snap",
        permission_tier="T1",
        source_class="factor_library_fixture",
        rollback_marker=False,
    )
    source_response = FactorInvocationResponse(
        response_id=str(uuid.uuid4()),
        decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        evidence=source_evidence,
        forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
    )

    resp = allow_bridge_readonly_context()
    evidence = build_a1_bridge_evidence(resp, source_factor_response=source_response)

    assert evidence.source_class == "factor_library_fixture"
    assert evidence.no_real_source_flag is True
    assert evidence.fixture_source_commit in ("P1_FIXTURE_ONLY", "DISABLED_DEFAULT")
    assert evidence.request_hash == "test_req_hash_abc123"
    assert evidence.permission_tier == "T1"


def test_bridge_evidence_has_factor_and_bridge_decision_hashes():
    """Bridge evidence must populate both factor_decision_hash and bridge_decision_hash."""
    from skillos.capability_invocation_os.adapters.factor_library.models import (
        FactorInvocationResponse,
        FactorAdapterDecision,
        FactorEvidenceEnvelopeView,
    )
    from skillos.capability_invocation_os.adapters.factor_library.constants import (
        BLOCKED_OUTPUTS,
    )

    source_evidence = FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        source_class="factor_library_fixture",
    )
    source_response = FactorInvocationResponse(
        response_id=str(uuid.uuid4()),
        decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        evidence=source_evidence,
        forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
    )

    resp = allow_bridge_readonly_context()
    evidence = build_a1_bridge_evidence(resp, source_factor_response=source_response)

    assert isinstance(evidence.factor_decision_hash, str)
    assert len(evidence.factor_decision_hash) == 64
    assert isinstance(evidence.bridge_decision_hash, str)
    assert len(evidence.bridge_decision_hash) == 64
    assert evidence.factor_decision_hash != ""


def test_c1_handoff_preserves_source_and_hash_fields():
    """C1 handoff must contain inherited source_class, no_real_source_flag, decision hashes."""
    from skillos.capability_invocation_os.adapters.factor_library.models import (
        FactorInvocationResponse,
        FactorAdapterDecision,
        FactorEvidenceEnvelopeView,
    )
    from skillos.capability_invocation_os.adapters.factor_library.constants import (
        BLOCKED_OUTPUTS,
    )

    source_evidence = FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        source_class="factor_library_fixture",
    )
    source_response = FactorInvocationResponse(
        response_id=str(uuid.uuid4()),
        decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        evidence=source_evidence,
        forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
    )

    resp = allow_bridge_readonly_context()
    bridge_evidence = build_a1_bridge_evidence(resp, source_factor_response=source_response)
    bridge_response = A1FactorBridgeResponse(
        response_id=resp.response_id,
        decision=resp.decision,
        evidence=bridge_evidence,
        forbidden_outputs_removed=resp.forbidden_outputs_removed,
        degraded=resp.degraded,
    )
    handoff = build_a1_bridge_c1_handoff(bridge_response)

    assert handoff["source_class"] == "factor_library_fixture"
    assert handoff["no_real_source_flag"] is True
    assert handoff["fixture_source_commit"] == "P1_FIXTURE_ONLY"
    assert handoff["factor_decision_hash"] != ""
    assert handoff["bridge_decision_hash"] != ""
    assert handoff["c1_handoff_marker"] is True


def test_c1_handoff_uses_existing_bridge_response_evidence():
    """When bridge response already has evidence, C1 handoff must use it, not default."""
    resp = allow_bridge_readonly_context()
    pre_built = A1FactorBridgeEvidence(
        source_commit="P1_FIXTURE_ONLY", source_class="factor_library_fixture",
        no_real_source_flag=True, fixture_source_commit="P1_FIXTURE_ONLY",
        request_hash="abc123", response_hash_placeholder="resp_ph",
        factor_decision_hash="factor_hash",
        bridge_decision_hash=build_a1_bridge_decision_hash(resp.decision),
        permission_tier="T1", forbidden_outputs_removed_hash="forbidden_hash",
        rollback_marker=False, privacy_marker=True, c1_handoff_marker=True,
    )
    br = A1FactorBridgeResponse(response_id=resp.response_id, decision=resp.decision,
        evidence=pre_built, forbidden_outputs_removed=resp.forbidden_outputs_removed,
        degraded=resp.degraded)
    h = build_a1_bridge_c1_handoff(br)
    assert h["source_class"] == "factor_library_fixture"
    assert h["fixture_source_commit"] == "P1_FIXTURE_ONLY"
    assert h["request_hash"] == "abc123"
    assert h["source_class"] != "factor_library_disabled_default"


def test_c1_handoff_with_source_factor_response_overrides_placeholder():
    """Passing source_factor_response to handoff must inherit P1_FIXTURE_ONLY fields."""
    from skillos.capability_invocation_os.adapters.factor_library.models import (
        FactorInvocationResponse, FactorAdapterDecision, FactorEvidenceEnvelopeView,
    )
    from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS
    import uuid
    src_ev = FactorEvidenceEnvelopeView(source_commit="P1_FIXTURE_ONLY", source_class="factor_library_fixture")
    src_resp = FactorInvocationResponse(response_id=str(uuid.uuid4()),
        decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        evidence=src_ev, forbidden_outputs_removed=list(BLOCKED_OUTPUTS))
    resp = allow_bridge_readonly_context()
    h = build_a1_bridge_c1_handoff(resp, source_factor_response=src_resp)
    assert h["source_class"] == "factor_library_fixture"
    assert h["no_real_source_flag"] is True
    assert h["fixture_source_commit"] == "P1_FIXTURE_ONLY"
    assert h["factor_decision_hash"] != ""


def test_c1_handoff_placeholder_only_when_no_source_or_evidence():
    """DISABLED_DEFAULT placeholder only when no source and no evidence exist."""
    resp = allow_bridge_readonly_context()
    h = build_a1_bridge_c1_handoff(resp)
    assert h["source_class"] == "factor_library_disabled_default"
    assert h["fixture_source_commit"] == "DISABLED_DEFAULT"
    assert h["no_real_source_flag"] is True
    assert h["c1_handoff_marker"] is True
