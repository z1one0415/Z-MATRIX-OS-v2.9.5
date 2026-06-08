"""Evidence — hash-only, in-memory, no file writes. C1 handoff fields present."""
import hashlib, json
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorEvidenceEnvelopeView, FactorAdapterDecision, BLOCKED_OUTPUTS,
)

def build_request_hash(request) -> str:
    return hashlib.sha256(json.dumps(str(request), sort_keys=True).encode()).hexdigest()

def build_response_hash_placeholder() -> str:
    return "response_hash_placeholder_p0"

def build_decision_hash(decision: FactorAdapterDecision) -> str:
    return hashlib.sha256(decision.value.encode()).hexdigest()

def build_factor_evidence_view(source_commit: str = "") -> FactorEvidenceEnvelopeView:
    return FactorEvidenceEnvelopeView(source_commit=source_commit)

def build_c1_evidence_handoff(request_hash: str, decision_hash: str, commit: str = "") -> dict:
    return {
        "source_commit": commit or "p0_placeholder",
        "request_hash": request_hash,
        "response_hash_placeholder": build_response_hash_placeholder(),
        "decision_hash": decision_hash,
        "factor_manifest_hash": "p0_placeholder",
        "validation_snapshot_hash": "p0_placeholder",
        "guardrail_profile_hash": "p0_placeholder",
        "application_contract_hash": "p0_placeholder",
        "permission_tier": "T0",
        "source_class": "factor_library",
        "rollback_marker": False,
        "privacy_marker": True,
    }
