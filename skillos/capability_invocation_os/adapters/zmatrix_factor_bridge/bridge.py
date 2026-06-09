from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
)


class A1FactorLibraryBridge:
    def __init__(self, factor_adapter=None, fixture_mode: bool = False):
        from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.config import (
            is_a1_factor_bridge_enabled,
        )
        from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.kill_switch import (
            should_force_disabled,
        )
        self._enabled = is_a1_factor_bridge_enabled()
        self._killed = should_force_disabled()
        self._factor_adapter = factor_adapter
        self._fixture_mode = fixture_mode

    def _should_bridge(self) -> bool:
        if self._killed:
            return False
        if not self._fixture_mode:
            return False
        if self._factor_adapter is None:
            return False
        return True

    def _deny_disabled(self) -> A1FactorBridgeResponse:
        from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.degradation import (
            disabled_default_noop,
        )
        return disabled_default_noop()

    def bridge_factor_response(self, response) -> A1FactorBridgeResponse:
        if not self._should_bridge():
            return self._deny_disabled()

        from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.contracts import (
            validate_factor_response_for_bridge,
        )
        from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.degradation import (
            allow_bridge_readonly_context,
            deny_bridge_factor_denied,
        )
        from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.evidence import (
            build_a1_bridge_evidence,
        )

        decision = validate_factor_response_for_bridge(response)
        if decision.value.startswith("DENY_"):
            return deny_bridge_factor_denied()

        base = allow_bridge_readonly_context()
        evidence = build_a1_bridge_evidence(base)
        return A1FactorBridgeResponse(
            response_id=base.response_id,
            decision=base.decision,
            evidence=evidence,
            forbidden_outputs_removed=base.forbidden_outputs_removed,
            degraded=base.degraded,
        )

    def bridge_factor_profile(self, factor_id: str) -> A1FactorBridgeResponse:
        if not self._should_bridge():
            return self._deny_disabled()

        factor_response = self._factor_adapter.get_factor_profile(factor_id)
        return self.bridge_factor_response(factor_response)

    def bridge_factor_evidence(self, factor_id: str) -> A1FactorBridgeResponse:
        if not self._should_bridge():
            return self._deny_disabled()

        factor_response = self._factor_adapter.get_factor_evidence(factor_id)
        return self.bridge_factor_response(factor_response)

    def build_bridge_context(self, factor_id: str | None = None) -> A1FactorBridgeResponse:
        if not self._should_bridge():
            return self._deny_disabled()

        factor_response = self._factor_adapter.build_research_context(factor_id)
        return self.bridge_factor_response(factor_response)
