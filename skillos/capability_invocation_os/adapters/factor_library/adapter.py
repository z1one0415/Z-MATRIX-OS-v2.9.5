"""Factor Library ReadOnly Adapter — disabled-default P0 facade. No execution."""
from skillos.capability_invocation_os.adapters.factor_library.config import (
    is_factor_library_adapter_enabled, is_factor_read_enabled,
)
from skillos.capability_invocation_os.adapters.factor_library.kill_switch import should_force_disabled
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorInvocationRequest, FactorInvocationResponse, FactorAdapterDecision,
    FactorEvidenceEnvelopeView, FactorFilter, CandidateMonitorRequest,
)
from skillos.capability_invocation_os.adapters.factor_library.degradation import disabled_default_noop
from skillos.capability_invocation_os.adapters.factor_library.evidence import build_c1_evidence_handoff
from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS
import uuid

class FactorLibraryReadOnlyAdapter:
    def __init__(self):
        self._enabled = is_factor_library_adapter_enabled()
        self._killed = should_force_disabled()

    def _deny_disabled(self, req_id: str) -> FactorInvocationResponse:
        return FactorInvocationResponse(
            response_id=str(uuid.uuid4()),
            decision=FactorAdapterDecision.DISABLED_DEFAULT_NOOP,
            evidence=FactorEvidenceEnvelopeView(),
            forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
            degraded=True,
        )

    def list_factors(self, filter: FactorFilter) -> FactorInvocationResponse:
        return self._deny_disabled("list_factors")

    def get_factor_profile(self, factor_id: str) -> FactorInvocationResponse:
        return self._deny_disabled(factor_id)

    def get_factor_evidence(self, factor_id: str, asof: str = None) -> FactorInvocationResponse:
        return self._deny_disabled(factor_id)

    def monitor_candidates(self, request: CandidateMonitorRequest) -> FactorInvocationResponse:
        return self._deny_disabled("monitor")

    def build_research_context(self, request: FactorInvocationRequest) -> FactorInvocationResponse:
        return self._deny_disabled(request.request_id)
