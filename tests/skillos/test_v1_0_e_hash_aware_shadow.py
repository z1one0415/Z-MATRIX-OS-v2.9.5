"""Tests for SkillOS v1.0-E hash-aware shadow audit."""

import json
import pytest
from pathlib import Path
from zmatrix.agent.skill_hash_aware_auditor import (
    audit_hash_aware_skill,
    audit_hash_aware_batch,
)

GOLDEN_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "golden" / "skillos_v1_0_d_golden_cases.json"


@pytest.fixture
def golden_cases():
    return json.loads(GOLDEN_PATH.read_text())["cases"]


class TestAuditResult:
    def test_hash_aware_audit_result_shape(self, golden_cases):
        c = golden_cases[0]
        r = audit_hash_aware_skill(c["skill_id"], c["input_payload"], c["output_payload"])
        assert r["skill_id"] == c["skill_id"]
        assert r["mode"] == "HASH_AWARE_SHADOW_AUDIT"
        assert r["blocked"] is False
        assert r["enforcement"] == "DISABLED"
        assert len(r["input_hash"]) == 64
        assert len(r["output_hash"]) == 64

    def test_hash_aware_audit_schema_valid(self, golden_cases):
        c = golden_cases[0]
        r = audit_hash_aware_skill(c["skill_id"], c["input_payload"], c["output_payload"])
        assert r["schema_input_valid"] is True
        assert r["schema_output_valid"] is True

    def test_hash_aware_audit_golden_hash_match(self, golden_cases):
        for c in golden_cases:
            r = audit_hash_aware_skill(c["skill_id"], c["input_payload"], c["output_payload"])
            assert r["golden_input_match"] is True, f"{c['case_id']}: input mismatch"
            assert r["golden_output_match"] is True, f"{c['case_id']}: output mismatch"

    def test_hash_aware_audit_detects_output_hash_mismatch(self, golden_cases):
        c = golden_cases[0]
        bad_out = dict(c["output_payload"])
        bad_out["status"] = "FAILED"
        r = audit_hash_aware_skill(c["skill_id"], c["input_payload"], bad_out)
        assert r["golden_output_match"] is False
        assert r["blocked"] is False  # never blocks

    def test_hash_aware_audit_detects_schema_violation(self, golden_cases):
        c = golden_cases[0]
        bad_out = {"skill_id": c["skill_id"]}  # missing required fields
        r = audit_hash_aware_skill(c["skill_id"], c["input_payload"], bad_out)
        assert r["schema_output_valid"] is False
        assert r["blocked"] is False

    def test_hash_aware_audit_never_blocks(self, golden_cases):
        for c in golden_cases:
            r = audit_hash_aware_skill(c["skill_id"], c["input_payload"], c["output_payload"])
            assert r["blocked"] is False


class TestBatchAudit:
    def test_batch_audit_summary(self, golden_cases):
        batch = audit_hash_aware_batch(golden_cases)
        assert batch["case_count"] == 4
        assert batch["blocked_count"] == 0
        assert batch["enforcement"] == "DISABLED"
        assert batch["all_pass"] is True


class TestNoModifications:
    def test_cli_no_file_write(self):
        source = Path("scripts/skillos/audit_hash_aware_shadow.py").read_text()
        code = [l for l in source.split("\n") if not l.strip().startswith("#")]
        assert not any("json.dump(" in l for l in code)
        assert not any("open(" in l and ("'w'" in l or '"w"' in l) for l in code)

    def test_no_invoke_skill_import(self):
        import inspect
        from zmatrix.agent import skill_hash_aware_auditor
        source = inspect.getsource(skill_hash_aware_auditor)
        assert "invoke_skill" not in source.lower().replace("_", "")

    def test_no_result_envelope_import(self):
        import inspect
        from zmatrix.agent import skill_hash_aware_auditor
        source = inspect.getsource(skill_hash_aware_auditor)
        assert "result_envelope" not in source.lower().replace("_", "")

    def test_boundary_reconcile_documents_policy_exception(self):
        """Verify D.1 policy patch document exists and explains the hash field exclusion."""
        doc = Path("docs/skillos/Z_SKILLOS_V1_0_D_1_HASH_FIELD_EXCLUSION_POLICY_PATCH.md")
        assert doc.exists(), "D.1 policy patch doc missing"
        content = doc.read_text()
        assert "input_hash" in content
        assert "output_hash" in content
        assert "circular" in content
