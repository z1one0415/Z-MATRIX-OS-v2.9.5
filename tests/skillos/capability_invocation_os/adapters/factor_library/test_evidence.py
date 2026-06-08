"""Evidence tests — hash-only, no file write, C1 handoff."""
import pytest
import ast
import os
from skillos.capability_invocation_os.adapters.factor_library.evidence import (
    build_request_hash, build_response_hash_placeholder, build_decision_hash,
    build_c1_evidence_handoff, build_factor_evidence_view,
)
from skillos.capability_invocation_os.adapters.factor_library.models import FactorAdapterDecision


def test_request_hash_deterministic():
    h1 = build_request_hash({"a": 1})
    h2 = build_request_hash({"a": 1})
    assert h1 == h2


def test_placeholder_exists():
    assert build_response_hash_placeholder() == "response_hash_placeholder_p0"


def test_decision_hash_deterministic():
    d = FactorAdapterDecision.DISABLED_DEFAULT_NOOP
    h1 = build_decision_hash(d)
    h2 = build_decision_hash(d)
    assert h1 == h2


def test_c1_handoff_has_required_fields():
    handoff = build_c1_evidence_handoff("req_hash", "dec_hash")
    required = [
        "source_commit", "request_hash", "response_hash_placeholder",
        "decision_hash", "factor_manifest_hash", "validation_snapshot_hash",
        "guardrail_profile_hash", "application_contract_hash",
        "permission_tier", "source_class", "rollback_marker", "privacy_marker",
    ]
    for field in required:
        assert field in handoff, f"Missing field: {field}"


def test_factor_evidence_view_accepts_source_commit():
    view = build_factor_evidence_view(source_commit="abc123")
    assert view.source_commit == "abc123"


def test_no_file_write_or_runtime_reports_in_evidence_source():
    path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..',
                        'skillos', 'capability_invocation_os', 'adapters',
                        'factor_library', 'evidence.py')
    with open(path) as f:
        content = f.read()
    assert 'open(' not in content
    assert '.write(' not in content
    assert 'runtime_reports' not in content
    assert 'runtime_audit' not in content
    assert 'research.factor_library' not in content
