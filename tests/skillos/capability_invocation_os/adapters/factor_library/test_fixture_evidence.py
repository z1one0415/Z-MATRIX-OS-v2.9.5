"""Tests for fixture evidence — 5 tests."""

from skillos.capability_invocation_os.adapters.factor_library.evidence import (
    build_fixture_evidence,
)
from skillos.capability_invocation_os.adapters.factor_library.fixtures import (
    FIXTURE_FACTOR_SAFE_VALIDATED,
    FIXTURE_FACTOR_DENIED_PIT_FAILED,
    ALL_FIXTURE_SCENARIOS,
)


def test_evidence_fields_complete():
    """Evidence dict must have all required fields."""
    evidence = build_fixture_evidence(FIXTURE_FACTOR_SAFE_VALIDATED)
    required_fields = [
        "fixture_source_commit",
        "source_class",
        "request_hash",
        "response_hash_placeholder",
        "decision_hash",
        "factor_manifest_hash",
        "validation_snapshot_hash",
        "guardrail_profile_hash",
        "application_contract_hash",
        "permission_tier",
        "rollback_marker",
        "privacy_marker",
        "no_real_source_flag",
    ]
    for field in required_fields:
        assert field in evidence, f"Missing field: {field}"


def test_request_hash_deterministic():
    """Same fixture must produce same request_hash every time."""
    ev1 = build_fixture_evidence(FIXTURE_FACTOR_SAFE_VALIDATED)
    ev2 = build_fixture_evidence(FIXTURE_FACTOR_SAFE_VALIDATED)
    assert ev1["request_hash"] == ev2["request_hash"]
    assert len(ev1["request_hash"]) == 64  # SHA-256 hex


def test_decision_hash_deterministic():
    """Same decision must produce same decision_hash every time."""
    ev1 = build_fixture_evidence(FIXTURE_FACTOR_SAFE_VALIDATED)
    ev2 = build_fixture_evidence(FIXTURE_FACTOR_SAFE_VALIDATED)
    assert ev1["decision_hash"] == ev2["decision_hash"]
    # Different decisions produce different hashes
    ev3 = build_fixture_evidence(FIXTURE_FACTOR_DENIED_PIT_FAILED)
    assert ev3["decision_hash"] != ev1["decision_hash"]


def test_factor_evidence_hashes_present():
    """All factor-related hashes must be non-empty strings."""
    for scenario in ALL_FIXTURE_SCENARIOS:
        evidence = build_fixture_evidence(scenario)
        assert evidence["factor_manifest_hash"], "factor_manifest_hash empty"
        assert evidence["validation_snapshot_hash"], "validation_snapshot_hash empty"
        assert evidence["guardrail_profile_hash"], "guardrail_profile_hash empty"
        assert evidence["application_contract_hash"], "application_contract_hash empty"


def test_c1_handoff_fields_present():
    """Evidence must contain C1 handoff compatible fields."""
    evidence = build_fixture_evidence(FIXTURE_FACTOR_SAFE_VALIDATED)
    # C1 handoff requires these fields
    assert evidence["permission_tier"] == "T0"
    assert evidence["rollback_marker"] is False
    assert evidence["privacy_marker"] is True
    assert evidence["no_real_source_flag"] is True
    assert evidence["fixture_source_commit"] == "P1_FIXTURE_ONLY"
    assert evidence["source_class"] == "factor_library_fixture"
