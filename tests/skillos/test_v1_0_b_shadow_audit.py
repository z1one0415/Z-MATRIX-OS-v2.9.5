"""Tests for SkillOS v1.0-B shadow schema audit."""

import pytest
from zmatrix.agent.skill_schema_validator import (
    validate_input_schema,
    validate_output_schema,
    audit_skill_schema,
    list_sample_skill_ids,
    SAMPLE_SKILL_IDS,
)

SAMPLE_COUNT = 5
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
        assert len(ids) == SAMPLE_COUNT
        assert ids == SAMPLE_SKILL_IDS
        assert all(isinstance(sid, str) for sid in ids)

    def test_sample_skills_all_exist_in_registry(self):
        for sid in SAMPLE_SKILL_IDS:
            result = validate_input_schema(sid, {})
            assert "skill_id" in result, f"{sid}: no skill_id in result"


class TestInputValidation:
    def test_validate_input_schema_success(self):
        result = validate_input_schema("SYSTEM.GET_SKILLOS_STATUS", {})
        assert result["valid"] is True
        assert result["violations"] == []
        assert result["mode"] == "SHADOW_AUDIT_ONLY"

    def test_validate_input_schema_with_snapshot(self):
        result = validate_input_schema(
            "RESEARCHDB.GET_LAYER_STATUS", {"data_snapshot_id": "snap-001"}
        )
        assert result["valid"] is True


class TestOutputValidation:
    def test_validate_output_schema_success(self):
        result = validate_output_schema("SYSTEM.GET_SKILLOS_STATUS", VALID_OUTPUT)
        assert result["valid"] is True
        assert result["violations"] == []

    def test_missing_required_output_field_detected(self):
        bad_output = {"skill_id": "SYSTEM.GET_SKILLOS_STATUS", "status": "SUCCESS"}
        result = validate_output_schema("SYSTEM.GET_SKILLOS_STATUS", bad_output)
        assert result["valid"] is False
        assert len(result["violations"]) > 0
        missing_skill_version = any("skill_version" in v for v in result["violations"])
        assert missing_skill_version, f"expected violation about skill_version, got: {result['violations']}"


class TestUnknownSkill:
    def test_unknown_skill_returns_audit_violation(self):
        result = validate_input_schema("NONEXISTENT.SKILL", {})
        assert result["valid"] is False
        assert any("not found" in v.lower() for v in result["violations"])


class TestAuditNeverBlocks:
    def test_audit_never_blocks(self):
        for sid in SAMPLE_SKILL_IDS:
            result = audit_skill_schema(sid, {}, VALID_OUTPUT)
            assert result["blocked"] is False, f"{sid}: blocked={result['blocked']}"
            assert result["enforcement"] == "DISABLED", f"{sid}: enforcement={result['enforcement']}"

    def test_audit_mode_shadow_only(self):
        result = audit_skill_schema("SYSTEM.GET_SKILLOS_STATUS", {}, VALID_OUTPUT)
        assert result["mode"] == "SHADOW_AUDIT_ONLY"

    def test_negative_case_not_blocked(self):
        bad_output = {"skill_id": "X"}
        result = audit_skill_schema("SYSTEM.GET_SKILLOS_STATUS", {}, bad_output)
        assert result["blocked"] is False  # never blocks
        assert result["output_valid"] is False  # but detects violation


class TestNoModifications:
    def test_no_invoke_skill_import(self):
        """Verify validator has no reference to invoke_skill."""
        import inspect
        from zmatrix.agent import skill_schema_validator
        source = inspect.getsource(skill_schema_validator)
        assert "invoke_skill" not in source.lower().replace("_", ""), \
            "validator references invoke_skill"

    def test_no_result_envelope_import(self):
        """Verify validator has no reference to result_envelope."""
        import inspect
        from zmatrix.agent import skill_schema_validator
        source = inspect.getsource(skill_schema_validator)
        assert "result_envelope" not in source.lower().replace("_", ""), \
            "validator references result_envelope"

    def test_no_file_write_in_audit_runner(self):
        """Verify audit runner has no file-write operations."""
        from pathlib import Path
        source = Path("scripts/skillos/audit_schema_compliance.py").read_text()
        # Check for json.dump (exclude this test file self-reference)
        code_lines = [l for l in source.split('\n') if not l.strip().startswith('#')]
        has_dump = any('json.dump(' in l for l in code_lines)
        has_open_w = any("open(" in l and ("'w'" in l or '"w"' in l) for l in code_lines)
        assert not has_dump, "audit runner has json.dump"
        assert not has_open_w, "audit runner opens file for writing"
