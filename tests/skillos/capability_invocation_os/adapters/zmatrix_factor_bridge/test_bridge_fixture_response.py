import pytest
from unittest.mock import patch, MagicMock
import uuid

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.bridge import (
    A1FactorLibraryBridge,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeDecision,
    A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.adapters.factor_library.fixture_provider import (
    FactorLibraryFixtureProvider,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorAdapterDecision,
    FactorInvocationResponse,
    FactorEvidenceEnvelopeView,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import (
    BLOCKED_OUTPUTS,
)


class TestBridgeFixtureResponse:

    def _make_adapter_with_fixture(self, factor_id):
        """Create a mock adapter that returns fixture responses."""
        provider = FactorLibraryFixtureProvider()
        fixture_resp = provider.get_fixture_profile(factor_id)
        mock_adapter = MagicMock()
        mock_adapter.get_factor_profile.return_value = fixture_resp
        mock_adapter.get_factor_evidence.return_value = fixture_resp
        mock_adapter.build_research_context.return_value = fixture_resp
        return mock_adapter

    @patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
    def test_explicit_fixture_mode_allows_safe_fixture(self, _mock):
        mock_adapter = self._make_adapter_with_fixture("FAKE_FACTOR_001")
        bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
        resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
        assert resp.decision == A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT
        assert resp.degraded is False

    @patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
    def test_explicit_fixture_mode_denies_pit_failed(self, _mock):
        mock_adapter = self._make_adapter_with_fixture("FAKE_FACTOR_002")
        bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
        resp = bridge.bridge_factor_profile("FAKE_FACTOR_002")
        assert resp.decision == A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED
        assert resp.degraded is True

    @patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
    def test_forbidden_outputs_removed_preserved(self, _mock):
        mock_adapter = self._make_adapter_with_fixture("FAKE_FACTOR_001")
        bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
        resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
        assert len(resp.forbidden_outputs_removed) > 0
        assert "buy_signal" in resp.forbidden_outputs_removed
        assert "alpha_claim" in resp.forbidden_outputs_removed

    @patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
    def test_no_real_source_flag_preserved(self, _mock):
        mock_adapter = self._make_adapter_with_fixture("FAKE_FACTOR_001")
        bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
        resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
        assert isinstance(resp.evidence, A1FactorBridgeEvidence)
        assert resp.evidence.no_real_source_flag is True

    @patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
    def test_source_class_preserved(self, _mock):
        mock_adapter = self._make_adapter_with_fixture("FAKE_FACTOR_001")
        bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
        resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
        assert isinstance(resp.evidence, A1FactorBridgeEvidence)
        assert resp.evidence.source_class == "factor_library_fixture"

    @patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
    def test_p1_fixture_only_preserved(self, _mock):
        mock_adapter = self._make_adapter_with_fixture("FAKE_FACTOR_001")
        bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
        resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
        assert isinstance(resp.evidence, A1FactorBridgeEvidence)
        assert resp.evidence.fixture_source_commit == "P1_FIXTURE_ONLY"

    @patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
    def test_no_alpha_trade_weight_output_in_bridge_response(self, _mock):
        mock_adapter = self._make_adapter_with_fixture("FAKE_FACTOR_001")
        bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
        resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
        forbidden_fields = {
            "alpha_claim", "expected_return_claim", "position_weight",
            "buy_signal", "sell_signal", "order_signal",
            "broker_runtime", "real_trade", "production",
        }
        for field_name in forbidden_fields:
            assert not hasattr(resp, field_name), f"Response should not have {field_name}"
        evidence_dict = resp.evidence.__dict__ if hasattr(resp.evidence, "__dict__") else {}
        for field_name in forbidden_fields:
            assert field_name not in evidence_dict,                 f"Evidence should not have {field_name}"


@patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
def test_source_forbidden_bridge_returns_source_forbidden(_mock):
    """Bridge must return DENY_BRIDGE_SOURCE_FORBIDDEN when source_class is forbidden."""
    provider = FactorLibraryFixtureProvider()
    # Create a fixture response with invalid source_class
    fixture_resp = provider.get_fixture_profile("FAKE_FACTOR_001")
    # Build a mock with wrong source_class
    invalid_resp = FactorInvocationResponse(
        response_id=fixture_resp.response_id,
        decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        evidence=FactorEvidenceEnvelopeView(
            source_commit="P1_FIXTURE_ONLY",
            request_hash="test",
            decision_hash="test",
            factor_manifest_hash="test",
            validation_snapshot_hash="test",
            permission_tier="T0",
            source_class="research_live",
        ),
        forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
    )
    mock_adapter = MagicMock()
    mock_adapter.get_factor_profile.return_value = invalid_resp
    bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
    resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
    assert resp.decision == A1FactorBridgeDecision.DENY_BRIDGE_SOURCE_FORBIDDEN


@patch.object(A1FactorLibraryBridge, "_should_bridge", return_value=True)
def test_output_unsafe_bridge_returns_outputs_unsafe(_mock):
    """Bridge must return DENY_BRIDGE_OUTPUTS_UNSAFE when outputs are unsafe."""
    provider = FactorLibraryFixtureProvider()
    fixture_resp = provider.get_fixture_profile("FAKE_FACTOR_001")
    # Build a response with incomplete forbidden_outputs_removed
    unsafe_resp = FactorInvocationResponse(
        response_id=fixture_resp.response_id,
        decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        evidence=FactorEvidenceEnvelopeView(
            source_commit="P1_FIXTURE_ONLY",
            request_hash="test",
            decision_hash="test",
            factor_manifest_hash="test",
            validation_snapshot_hash="test",
            permission_tier="T0",
            source_class="factor_library_fixture",
        ),
        forbidden_outputs_removed=["buy_signal"],  # incomplete - missing most
    )
    mock_adapter = MagicMock()
    mock_adapter.get_factor_profile.return_value = unsafe_resp
    bridge = A1FactorLibraryBridge(factor_adapter=mock_adapter, fixture_mode=True)
    resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
    assert resp.decision == A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE
