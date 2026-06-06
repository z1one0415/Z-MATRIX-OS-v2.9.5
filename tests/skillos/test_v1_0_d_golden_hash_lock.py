"""Tests for SkillOS v1.0-D golden hash lock."""

import json
import pytest
from pathlib import Path
from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash
from zmatrix.agent.skill_hash_policy import (
    get_hash_policy,
    get_output_hash_excluded_fields,
    is_output_hash_excluded_field,
    HASH_ALGORITHM,
    OUTPUT_HASH_EXCLUDED_FIELDS,
)

GOLDEN_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "golden" / "skillos_v1_0_d_golden_cases.json"


@pytest.fixture
def golden():
    return json.loads(GOLDEN_PATH.read_text())


@pytest.fixture
def golden_cases(golden):
    return golden["cases"]


class TestHashPolicy:
    def test_hash_policy_declares_sha256(self):
        p = get_hash_policy()
        assert p["hash_algorithm"] == "SHA-256"

    def test_hash_policy_declares_canonical_json(self):
        p = get_hash_policy()
        cj = p["canonical_json_policy"]
        assert cj["sort_keys"] is True
        assert cj["separators"] == [",", ":"]
        assert cj["ensure_ascii"] is False

    def test_hash_policy_declares_narrative_exclusion(self):
        assert "narrative" in get_output_hash_excluded_fields()

    def test_hash_policy_excludes_hash_fields(self):
        assert is_output_hash_excluded_field("narrative") is True
        assert is_output_hash_excluded_field("input_hash") is True
        assert is_output_hash_excluded_field("output_hash") is True
        assert is_output_hash_excluded_field("skill_id") is False


class TestGoldenCases:
    def test_golden_cases_exist(self, golden, golden_cases):
        assert len(golden_cases) == 4

    def test_golden_cases_have_no_dynamic_fields(self, golden):
        text = json.dumps(golden)
        assert "timestamp" not in text.lower()
        assert "generated_at" not in text.lower()

    def test_golden_cases_hashes_length_64(self, golden_cases):
        for c in golden_cases:
            assert len(c["expected_input_hash"]) == 64
            assert len(c["expected_output_hash"]) == 64

    def test_golden_input_hashes_match(self, golden_cases):
        for c in golden_cases:
            computed = compute_input_hash(c["input_payload"])
            assert computed == c["expected_input_hash"], f"{c['case_id']}: input hash mismatch"

    def test_golden_output_hashes_match(self, golden_cases):
        for c in golden_cases:
            computed = compute_output_hash(c["output_payload"])
            assert computed == c["expected_output_hash"], f"{c['case_id']}: output hash mismatch"

    def test_narrative_change_does_not_change_output_hash(self, golden_cases):
        base = golden_cases[0]["output_payload"]
        with_narr = dict(base)
        with_narr["narrative"] = "hello world"
        assert compute_output_hash(base) == compute_output_hash(with_narr)

    def test_non_narrative_change_changes_output_hash(self, golden_cases):
        base = golden_cases[0]["output_payload"]
        changed = dict(base)
        changed["status"] = "FAILED"
        assert compute_output_hash(base) != compute_output_hash(changed)

    def test_output_hash_ignores_input_hash_and_output_hash(self):
        base = {"skill_id": "X", "status": "OK"}
        with_hashes = {"skill_id": "X", "status": "OK",
                        "input_hash": "abc123abc123", "output_hash": "def456def456"}
        assert compute_output_hash(base) == compute_output_hash(with_hashes)

    def test_golden_expected_hashes_unchanged_after_exclusion_metadata_patch(self, golden_cases):
        for c in golden_cases:
            ih = compute_input_hash(c["input_payload"])
            oh = compute_output_hash(c["output_payload"])
            assert ih == c["expected_input_hash"], f"{c['case_id']}: input hash changed"
            assert oh == c["expected_output_hash"], f"{c['case_id']}: output hash changed"
            assert len(ih) == 64
            assert len(oh) == 64


class TestNoModifications:
    def test_no_file_write(self):
        import inspect
        from zmatrix.agent import skill_hash_policy
        source = inspect.getsource(skill_hash_policy)
        assert "open(" not in source or "json.dump" not in source

    def test_no_invoke_skill_import(self):
        import inspect
        from zmatrix.agent import skill_hash_policy
        source = inspect.getsource(skill_hash_policy)
        assert "invoke_skill" not in source.lower().replace("_", "")

    def test_no_result_envelope_import(self):
        import inspect
        from zmatrix.agent import skill_hash_policy
        source = inspect.getsource(skill_hash_policy)
        assert "result_envelope" not in source.lower().replace("_", "")
