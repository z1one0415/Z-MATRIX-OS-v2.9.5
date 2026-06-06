"""Tests for SkillOS v1.0-C pure hash scaffold."""

import pytest
from zmatrix.agent.skill_hashing import (
    canonical_json,
    compute_sha256,
    compute_input_hash,
    compute_output_hash,
    build_hash_audit_record,
)


class TestCanonicalJson:
    def test_canonical_json_stable_key_order(self):
        a = canonical_json({"b": 1, "a": 2})
        b = canonical_json({"a": 2, "b": 1})
        assert a == b
        assert a == '{"a":2,"b":1}'

    def test_canonical_json_no_dynamic_fields(self):
        out = canonical_json({"x": 1})
        assert "datetime" not in out.lower()
        assert "timestamp" not in out.lower()


class TestHashing:
    def test_compute_sha256_length_64(self):
        h = compute_sha256("hello")
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_input_hash_stable(self):
        h1 = compute_input_hash({"x": 1})
        h2 = compute_input_hash({"x": 1})
        assert h1 == h2
        assert len(h1) == 64

    def test_output_hash_stable(self):
        out = {"skill_id": "X", "skill_version": "1.0.0", "status": "SUCCESS"}
        h1 = compute_output_hash(out)
        h2 = compute_output_hash(out)
        assert h1 == h2

    def test_hash_equal_for_reordered_dict(self):
        h1 = compute_input_hash({"a": 1, "b": 2})
        h2 = compute_input_hash({"b": 2, "a": 1})
        assert h1 == h2

    def test_hash_diff_for_changed_value(self):
        h1 = compute_input_hash({"a": 1, "b": 2})
        h2 = compute_input_hash({"a": 1, "b": 3})
        assert h1 != h2

    def test_output_hash_strips_narrative(self):
        out_with = {"skill_id": "X", "narrative": "hello world", "status": "OK"}
        out_without = {"skill_id": "X", "status": "OK"}
        assert compute_output_hash(out_with) == compute_output_hash(out_without)


class TestAuditRecord:
    def test_hash_audit_record_shape(self):
        rec = build_hash_audit_record("SYS.X", {}, {"skill_id": "SYS.X"})
        assert rec["skill_id"] == "SYS.X"
        assert rec["mode"] == "PURE_HASH_SCAFFOLD"
        assert rec["blocked"] is False
        assert rec["enforcement"] == "DISABLED"
        assert rec["hash_algorithm"] == "SHA-256"
        assert len(rec["input_hash"]) == 64
        assert len(rec["output_hash"]) == 64

    def test_hash_audit_record_never_blocks(self):
        rec = build_hash_audit_record("SYS.X", {}, {})
        assert rec["blocked"] is False

    def test_hash_audit_record_detects_narrative(self):
        rec = build_hash_audit_record("SYS.X", {}, {"skill_id": "X", "narrative": "hi"})
        assert rec["narrative_stripped"] is True


class TestNoModifications:
    def test_no_invoke_skill_import(self):
        import inspect
        from zmatrix.agent import skill_hashing
        source = inspect.getsource(skill_hashing)
        assert "invoke_skill" not in source.lower().replace("_", "")

    def test_no_result_envelope_import(self):
        import inspect
        from zmatrix.agent import skill_hashing
        source = inspect.getsource(skill_hashing)
        assert "result_envelope" not in source.lower().replace("_", "")

    def test_audit_hash_cli_no_file_write(self):
        from pathlib import Path
        source = Path("scripts/skillos/audit_schema_hashes.py").read_text()
        code = [l for l in source.split("\n") if not l.strip().startswith("#")]
        assert not any("json.dump(" in l for l in code)
        assert not any("open(" in l and ("'w'" in l or '"w"' in l) for l in code)
