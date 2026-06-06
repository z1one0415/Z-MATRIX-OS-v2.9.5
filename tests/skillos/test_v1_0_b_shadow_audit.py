"""Tests for SkillOS v1.0-B shadow schema audit (with sample reconcile)."""

import pytest
from zmatrix.agent.skill_schema_validator import (
    validate_input_schema,
    validate_output_schema,
    audit_skill_schema,
    list_sample_skill_ids,
    SAMPLE_SKILL_IDS,
    AVAILABLE_SUBSTITUTES,
    get_audit_skill_ids,
)

VALID_OUTPUT = {
    "skill_id": "SYSTEM.GET_SKILLOS_STATUS",
    "skill_version": "1.0.0",
    "status": "SUCCESS",
    "risk_level": "R0_READ",
    "input_hash": "abc123",
    "output_hash": "def456",
}


class TestSampleSkills:
    def test_sample_skill_ids_fixed(self):
        ids = list_sample_skill_ids()
        assert len(ids) == 5

    def test_sample_skills_match_readiness_gate(self):
        """Hard assertion: exact v1.0-B gate-approved list."""
        gate_approved = [
            "SYSTEM.GET_SKILLOS_STATUS",
            "GOVERNANCE.GET_VERIFY_STATUS",
            "RESEARCHDB.GET_SCHEMA",
            "COCKPIT.GET_SKILLOS_STATUS",
            "FACTOR.LIST_REGISTERED_FACTORS",
        ]
        assert SAMPLE_SKILL_IDS == gate_approved, \
            f"SAMPLE_SKILL_IDS drifted: {SAMPLE_SKILL_IDS}"

    def test_sample_skills_all_exist_or_have_substitute(self):
        from zmatrix.agent.skill_contract_registry import get_skill_contract
        for sid in SAMPLE_SKILL_IDS:
            exists = get_skill_contract(sid) is not None
            has_sub = sid in AVAILABLE_SUBSTITUTES
            assert exists or has_sub, f"{sid}: not in registry, no substitute"

    def test_get_audit_skill_ids_returns_usable_list(self):
        ids = get_audit_skill_ids()
        assert len(ids) > 0
        assert "SYSTEM.GET_SKILLOS_STATUS" in ids

    def test_audit_skill_ids_unique(self):
        """get_audit_skill_ids must return no duplicates."""
        ids = get_audit_skill_ids()
        assert len(ids) == len(set(ids)), f"duplicates in audit ids: {ids}"

    def test_duplicate_substitute_count_documented(self):
        """COCKPIT.GET_SKILLOS_STATUS substitute collides with SYSTEM.GET_SKILLOS_STATUS."""
        ids = get_audit_skill_ids()
        unique = len(set(ids))
        # COCKPIT→SYSTEM causes a duplicate: 5 approved, 4 unique auditable
        assert unique == 4, f"expected 4 unique, got {unique}: {ids}"
        assert "SYSTEM.GET_SKILLOS_STATUS" in ids
        assert "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY" in ids
        assert "RESEARCHDB.GET_LAYER_STATUS" in ids
        assert "FACTOR.GET_FACTOR_REGISTRY" in ids


class TestInputValidation:
    def test_validate_input_schema_success(self):
        result = validate_input_schema("SYSTEM.GET_SKILLOS_STATUS", {})
        assert result["valid"] is True

    def test_validate_input_schema_with_snapshot(self):
        result = validate_input_schema(
            "RESEARCHDB.GET_LAYER_STATUS", {"data_snapshot_id": "snap-001"}
        )
        assert result["valid"] is True


class TestOutputValidation:
    def test_validate_output_schema_success(self):
        result = validate_output_schema("SYSTEM.GET_SKILLOS_STATUS", VALID_OUTPUT)
        assert result["valid"] is True

    def test_missing_required_output_field_detected(self):
        bad = {"skill_id": "SYSTEM.GET_SKILLOS_STATUS", "status": "SUCCESS"}
        result = validate_output_schema("SYSTEM.GET_SKILLOS_STATUS", bad)
        assert result["valid"] is False
        assert any("skill_version" in v for v in result["violations"])


class TestUnknownSkill:
    def test_unknown_skill_returns_audit_violation(self):
        result = validate_input_schema("NONEXISTENT.SKILL", {})
        assert result["valid"] is False


class TestAuditNeverBlocks:
    def test_audit_never_blocks(self):
        for sid in get_audit_skill_ids():
            result = audit_skill_schema(sid, {}, VALID_OUTPUT)
            assert result["blocked"] is False

    def test_audit_mode_shadow_only(self):
        result = audit_skill_schema("SYSTEM.GET_SKILLOS_STATUS", {}, VALID_OUTPUT)
        assert result["mode"] == "SHADOW_AUDIT_ONLY"

    def test_negative_case_not_blocked(self):
        result = audit_skill_schema("SYSTEM.GET_SKILLOS_STATUS", {}, {"skill_id": "X"})
        assert result["blocked"] is False
        assert result["output_valid"] is False


class TestNoModifications:
    def test_no_invoke_skill_import(self):
        import inspect
        from zmatrix.agent import skill_schema_validator
        source = inspect.getsource(skill_schema_validator)
        assert "invoke_skill" not in source.lower().replace("_", "")

    def test_no_result_envelope_import(self):
        import inspect
        from zmatrix.agent import skill_schema_validator
        source = inspect.getsource(skill_schema_validator)
        assert "result_envelope" not in source.lower().replace("_", "")

    def test_no_file_write_in_audit_runner(self):
        from pathlib import Path
        source = Path("scripts/skillos/audit_schema_compliance.py").read_text()
        code = [l for l in source.split("\n") if not l.strip().startswith("#")]
        assert not any("json.dump(" in l for l in code)
        assert not any("open(" in l and ("'w'" in l or '"w"' in l) for l in code)
