"""Tests for SkillOS v1.0-F golden regression expansion."""

import json
import pytest
from pathlib import Path
from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash
from zmatrix.agent.skill_contract_registry import get_skill_contract

GOLDEN_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "golden" / "skillos_v1_0_f_golden_regression_cases.json"


@pytest.fixture
def regression():
    return json.loads(GOLDEN_PATH.read_text())


@pytest.fixture
def cases(regression):
    return regression["cases"]


class TestRegressionCases:
    def test_regression_cases_exist(self, regression, cases):
        assert len(cases) > 0

    def test_regression_case_count_12(self, cases):
        assert len(cases) == 12

    def test_all_skill_ids_exist_in_contract_registry(self, cases):
        for c in cases:
            contract = get_skill_contract(c["skill_id"])
            assert contract is not None, f"{c['skill_id']}: not in contract registry"

    def test_domains_covered_at_least_8(self, cases):
        domains = {c["domain"] for c in cases}
        assert len(domains) >= 8, f"only {len(domains)} domains covered"

    def test_hashes_match(self, cases):
        for c in cases:
            ih = compute_input_hash(c["input_payload"])
            oh = compute_output_hash(c["output_payload"])
            assert ih == c["expected_input_hash"], f"{c['case_id']}: input hash mismatch"
            assert oh == c["expected_output_hash"], f"{c['case_id']}: output hash mismatch"

    def test_no_dynamic_fields(self, regression):
        text = json.dumps(regression)
        assert "timestamp" not in text.lower()
        assert "generated_at" not in text.lower()

    def test_output_hash_excludes_hash_fields(self, cases):
        for c in cases:
            base_out = c["output_payload"]
            with_hashes = dict(base_out)
            with_hashes["input_hash"] = "abc123abc123"
            with_hashes["output_hash"] = "def456def456"
            assert compute_output_hash(base_out) == compute_output_hash(with_hashes), \
                f"{c['case_id']}: hash fields not excluded"


class TestNoModifications:
    def test_no_invoke_skill_import(self):
        import inspect
        import scripts.skillos.build_golden_regression_cases as m
        source = inspect.getsource(m)
        assert "invoke_skill" not in source.lower().replace("_", "")

    def test_no_result_envelope_import(self):
        import inspect
        import scripts.skillos.build_golden_regression_cases as m
        source = inspect.getsource(m)
        assert "result_envelope" not in source.lower().replace("_", "")

    def test_builder_no_runtime_reports_write(self):
        source = Path("scripts/skillos/build_golden_regression_cases.py").read_text()
        code = [l for l in source.split("\n") if not l.strip().startswith("#")]
        assert not any("json.dump(" in l for l in code)

    def test_auditor_no_runtime_reports_write(self):
        source = Path("scripts/skillos/audit_golden_regression.py").read_text()
        code = [l for l in source.split("\n") if not l.strip().startswith("#")]
        assert not any("json.dump(" in l for l in code)
        assert not any("open(" in l and ("'w'" in l or '"w"' in l) for l in code)
