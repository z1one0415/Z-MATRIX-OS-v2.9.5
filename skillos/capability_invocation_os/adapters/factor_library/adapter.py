"""Factor Library ReadOnly Adapter — disabled-default P0 facade. No execution."""

from skillos.capability_invocation_os.adapters.factor_library.config import (
    is_factor_library_adapter_enabled,
    is_factor_read_enabled,
)
from skillos.capability_invocation_os.adapters.factor_library.kill_switch import (
    should_force_disabled,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorInvocationRequest,
    FactorInvocationResponse,
    FactorAdapterDecision,
    FactorEvidenceEnvelopeView,
    FactorFilter,
    CandidateMonitorRequest,
)
from skillos.capability_invocation_os.adapters.factor_library.degradation import (
    disabled_default_noop,
)
from skillos.capability_invocation_os.adapters.factor_library.evidence import (
    build_c1_evidence_handoff,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS
import uuid


class FactorLibraryReadOnlyAdapter:
    def __init__(self, fixture_provider=None, fixture_mode: bool = False):
        self._enabled = is_factor_library_adapter_enabled()
        self._killed = should_force_disabled()
        self._fixture_provider = fixture_provider
        self._fixture_mode = fixture_mode

    def _deny_disabled(self) -> FactorInvocationResponse:
        return FactorInvocationResponse(
            response_id=str(uuid.uuid4()),
            decision=FactorAdapterDecision.DISABLED_DEFAULT_NOOP,
            evidence=FactorEvidenceEnvelopeView(
                source_commit="DISABLED",
                request_hash="",
                decision_hash="",
                factor_manifest_hash="",
                validation_snapshot_hash="",
                permission_tier="T0",
                source_class="disabled_default",
            ),
            forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
        )

    def _should_use_fixture(self) -> bool:
        """Fixture mode only when explicitly enabled, provider present, kill switch NOT active."""
        if self._killed:
            return False
        if not self._fixture_mode:
            return False
        if self._fixture_provider is None:
            return False
        return True

    def list_factors(self, filter: FactorFilter = None) -> FactorInvocationResponse:
        if self._should_use_fixture():
            return self._fixture_provider.list_fixture_factors()
        return self._deny_disabled()

    def get_factor_profile(self, factor_id: str) -> FactorInvocationResponse:
        if self._should_use_fixture():
            return self._fixture_provider.get_fixture_profile(factor_id)
        return self._deny_disabled()

    def get_factor_evidence(self, factor_id: str) -> FactorInvocationResponse:
        if self._should_use_fixture():
            return self._fixture_provider.get_fixture_evidence(factor_id)
        return self._deny_disabled()

    def monitor_candidates(self, request: CandidateMonitorRequest = None) -> FactorInvocationResponse:
        if self._should_use_fixture():
            return self._fixture_provider.monitor_fixture_candidates()
        return self._deny_disabled()

    def build_research_context(self, request: FactorInvocationRequest = None) -> FactorInvocationResponse:
        if self._should_use_fixture():
            factor_id = None
            if request and hasattr(request, 'factor_selector') and request.factor_selector:
                factor_id = request.factor_selector.get("factor_id")
            return self._fixture_provider.build_fixture_research_context(factor_id)
        return self._deny_disabled()
