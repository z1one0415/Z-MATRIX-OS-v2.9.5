"""10-stage guard pipeline — disabled returns CONTINUE, exceptions degrade."""
from skillos.capability_invocation_os.runtime.models import InvocationRequest, GuardResult
from skillos.capability_invocation_os.runtime.config import is_runtime_enabled

def run_guard_pipeline(request, registry=None, config=None, sink=None):
    stages = ["preflight","capability_lookup","contract_validation","permission_check",
              "risk_tier_check","composition_check","side_effect_check",
              "evidence_capture_plan","postcondition_check","rollback_degrade_plan"]
    if config and not is_runtime_enabled(config):
        return GuardResult(action="CONTINUE", stage_results=[f"{s}: disabled" for s in stages], degraded=True)
    try:
        results = [f"{s}: not_implemented" for s in stages]
        return GuardResult(action="CONTINUE", stage_results=results, degraded=True)
    except Exception:
        return GuardResult(action="DEGRADE_MANUAL_REVIEW", stage_results=["exception: degraded"], degraded=True)

def is_guard_enabled(config):
    try: return getattr(config, "runtime_enabled", False) is True
    except: return False
