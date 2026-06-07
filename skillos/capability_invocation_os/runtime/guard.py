"""10-stage guard pipeline skeleton — disabled returns CONTINUE/DENY_NOOP."""
from skillos.capability_invocation_os.runtime.models import InvocationRequest, GuardResult

def run_guard_pipeline(request: InvocationRequest) -> GuardResult:
    stages = ["preflight", "capability_lookup", "contract_validation", "permission_check",
              "risk_tier_check", "composition_check", "side_effect_check",
              "evidence_capture_plan", "postcondition_check", "rollback_degrade_plan"]
    return GuardResult(action="CONTINUE", stage_results=[f"{s}: disabled" for s in stages], degraded=True)

def is_guard_enabled(config) -> bool:
    try:
        return getattr(config, "runtime_enabled", False) is True
    except Exception:
        return False
