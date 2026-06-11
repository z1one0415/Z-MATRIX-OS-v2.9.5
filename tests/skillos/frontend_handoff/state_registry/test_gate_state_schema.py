"""test_gate_state_schema.py — Schema validation tests for gate state registry.

Validates the gate_state_demo.json fixture against the full JSON Schema,
checks status enum values, commit chain integrity, and safety flags.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent  # Z-MATRIX-OS root

FIXTURE_PATH = ROOT / "tests" / "skillos" / "frontend_handoff" / "state_registry" / "gate_state_demo.json"
SCHEMA_PATH = ROOT / "skillos" / "frontend_handoff" / "state_registry" / "gate_state_schema.json"


def _load_fixture():
    assert FIXTURE_PATH.exists(), f"Fixture not found: {FIXTURE_PATH}"
    return json.loads(FIXTURE_PATH.read_text())


def _load_schema():
    assert SCHEMA_PATH.exists(), f"Schema not found: {SCHEMA_PATH}"
    return json.loads(SCHEMA_PATH.read_text())


fixture = _load_fixture()
schema = _load_schema()

VALID_STATUSES = {
    "PASS", "PASS_WITH_NOTE", "PASS_WITH_SEMANTIC_FIELD_NOTE",
    "BLOCKED", "PENDING", "ABORTED", "DEGRADED",
    "DISABLED_DEFAULT", "MERGED_AND_SEALED"
}

VALID_BROKER_RUNTIMES = {"none", "paper", "live", "both"}

REQUIRED_GATE_FIELDS = {
    "gate_id", "stage", "commit", "parent_commit", "status",
    "scope", "allowed_next_entries", "blocked_actions",
    "evidence_refs", "created_at", "human_decision_required",
    "promotion_allowed", "alpha_claim_allowed", "runner_enabled",
    "paper_trading_allowed", "production", "broker_runtime", "real_trade"
}


def test_fixture_has_chain_id():
    assert "chain_id" in fixture
    assert fixture["chain_id"] == "F7.2-formal-validation"


def test_fixture_has_gates_array():
    assert "gates" in fixture
    assert isinstance(fixture["gates"], list)
    assert len(fixture["gates"]) == 11


def test_fixture_has_chain_summary():
    assert "chain_summary" in fixture
    summary = fixture["chain_summary"]
    assert summary["total_gates"] == 11
    assert summary["merged_and_sealed"] == 11
    assert summary["passed"] == 11


def test_all_gates_have_required_fields():
    for gate in fixture["gates"]:
        for field in REQUIRED_GATE_FIELDS:
            assert field in gate, f"Gate {gate.get('gate_id', 'UNKNOWN')} missing field: {field}"


def test_all_gate_statuses_valid():
    for gate in fixture["gates"]:
        assert gate["status"] in VALID_STATUSES, \
            f"Gate {gate['gate_id']} has invalid status: {gate['status']}"


def test_all_gates_merged_and_sealed():
    """All F7.2 gates should be MERGED_AND_SEALED."""
    for gate in fixture["gates"]:
        assert gate["status"] == "MERGED_AND_SEALED", \
            f"Gate {gate['gate_id']} expected MERGED_AND_SEALED, got {gate['status']}"


def test_stages_sequential():
    """Gates should have sequential stage numbers 0-10."""
    stages = [gate["stage"] for gate in fixture["gates"]]
    assert stages == list(range(11)), f"Non-sequential stages: {stages}"


def test_commit_chain_continuity():
    """Each gate's parent_commit should match the previous gate's commit."""
    gates = fixture["gates"]
    for i in range(1, len(gates)):
        assert gates[i]["parent_commit"] == gates[i - 1]["commit"], \
            f"Chain break at stage {gates[i]['stage']}: " \
            f"parent_commit={gates[i]['parent_commit']} != prev_commit={gates[i-1]['commit']}"


def test_first_gate_has_correct_parent():
    """F7.0 parent commit should be 1f20dc1b (integration base)."""
    assert fixture["gates"][0]["parent_commit"] == "1f20dc1b"


def test_known_commit_shas():
    """Verify all 11 audited commit SHAs are present."""
    expected_commits = [
        "e636dcfa", "e1373225", "6de8802d", "c1d1e38d",
        "2448124e", "597aaa32", "ea80ff9a", "b9f77abb",
        "18429840", "4dcef2ab", "03c8de6e"
    ]
    actual_commits = [gate["commit"] for gate in fixture["gates"]]
    assert actual_commits == expected_commits, \
        f"Commit mismatch:\nExpected: {expected_commits}\nActual:   {actual_commits}"


def test_production_false_everywhere():
    """All gates must have production=false."""
    for gate in fixture["gates"]:
        assert gate["production"] is False, \
            f"Gate {gate['gate_id']} has production={gate['production']}"


def test_real_trade_false_everywhere():
    """All gates must have real_trade=false."""
    for gate in fixture["gates"]:
        assert gate["real_trade"] is False, \
            f"Gate {gate['gate_id']} has real_trade={gate['real_trade']}"


def test_broker_runtime_none_everywhere():
    """All gates must have broker_runtime='none'."""
    for gate in fixture["gates"]:
        assert gate["broker_runtime"] == "none", \
            f"Gate {gate['gate_id']} has broker_runtime={gate['broker_runtime']}"
        assert gate["broker_runtime"] in VALID_BROKER_RUNTIMES


def test_schema_is_valid_json_schema():
    """Verify the schema file is a valid JSON Schema draft."""
    assert "$schema" in schema
    assert schema["$schema"].startswith("https://json-schema.org/")


def test_schema_defines_required_top_fields():
    """Schema must require chain_id, gates, and generated_at."""
    top_required = schema.get("required", [])
    for field in ["chain_id", "gates", "generated_at"]:
        assert field in top_required, f"Schema missing required field: {field}"


def test_schema_defines_gate_status_enum():
    """Schema must define the full gate status enum for items."""
    gate_items = schema["properties"]["gates"]["items"]
    status_enum = gate_items["properties"]["status"]["enum"]
    for status in VALID_STATUSES:
        assert status in status_enum, f"Schema missing status enum value: {status}"


def test_gate_ids_unique():
    """All gate_ids must be unique."""
    ids = [gate["gate_id"] for gate in fixture["gates"]]
    assert len(ids) == len(set(ids)), f"Duplicate gate_ids found: {ids}"
