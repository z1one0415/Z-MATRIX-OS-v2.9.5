from skillos.capability_invocation_os.runtime.composition import validate_chain, detect_forbidden_composition, detect_conflict, plan_evidence_handoff
from skillos.capability_invocation_os.runtime.models import InvocationRequest
class TestP1CompositionGuard:
    def test_multi_denied(self): assert validate_chain([InvocationRequest(),InvocationRequest()]).action == "DENY"
    def test_empty_denied(self): assert validate_chain([]).action == "DENY"
    def test_conflict_detected(self): assert detect_conflict([InvocationRequest(),InvocationRequest(caller_role="other")]) is True
    def test_handoff_plan(self): assert plan_evidence_handoff([InvocationRequest()]) == 1
