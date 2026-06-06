"""Tests for SkillOS v1.1-C golden coverage expansion."""

import json, pytest
from pathlib import Path
from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash
from zmatrix.agent.skill_contract_registry import get_skill_contract

P = Path("data/research_db/agent/golden/skillos_v1_1_c_golden_regression_cases_24.json")

@pytest.fixture
def reg():
    return json.loads(P.read_text())

@pytest.fixture
def cases(reg):
    return reg["cases"]


class TestCoverageBasics:
    def test_cases_exist(self, cases):
        assert len(cases) > 0
    def test_case_count_24(self, cases):
        assert len(cases) == 24
    def test_domains_covered_at_least_16(self, cases):
        assert len({c["domain"] for c in cases}) >= 16
    def test_all_skill_ids_registry_exact(self, cases):
        for c in cases:
            assert get_skill_contract(c["skill_id"]) is not None, f"{c['skill_id']} not in registry"
    def test_no_duplicate_case_id(self, cases):
        ids = [c["case_id"] for c in cases]
        assert len(ids) == len(set(ids))

class TestExclusions:
    def test_case_domain_matches_contract_domain(self, cases):
        for c in cases:
            ct = get_skill_contract(c["skill_id"])
            assert ct is not None
            assert c["domain"] == ct["domain"], \
                f"{c['skill_id']}: case.domain={c['domain']} != contract.domain={ct['domain']}"

    def test_domains_covered_are_contract_domains(self, cases):
        domains = {c["domain"] for c in cases}
        assert len(domains) >= 16
        for c in cases:
            ct = get_skill_contract(c["skill_id"])
            assert ct["semantic_category"] != "NARRATIVE_RENDERER", f"{c['skill_id']} is narrative"
    def test_excludes_write_layers(self, cases):
        for c in cases:
            ct = get_skill_contract(c["skill_id"])
            assert not ct.get("write_layers"), f"{c['skill_id']} has write_layers"
    def test_excludes_proposal_required(self, cases):
        for c in cases:
            ct = get_skill_contract(c["skill_id"])
            assert not ct.get("proposal_required"), f"{c['skill_id']} requires proposal"
    def test_risk_level_max_r2(self, cases):
        ranks = {"R0_READ": 0, "R1_ANNOTATE": 1, "R2_DRAFT": 2}
        for c in cases:
            assert ranks.get(c["risk_level"], 99) <= 2

class TestHashes:
    def test_hashes_match(self, cases):
        for c in cases:
            assert compute_input_hash(c["input_payload"]) == c["expected_input_hash"]
            assert compute_output_hash(c["output_payload"]) == c["expected_output_hash"]
    def test_no_dynamic_fields(self, reg):
        text = json.dumps(reg)
        assert "timestamp" not in text.lower()

class TestNoMods:
    def test_audit_no_runtime_reports_write(self):
        source = Path("scripts/skillos/audit_golden_coverage_v1_1_c.py").read_text()
        code = [l for l in source.split("\n") if not l.strip().startswith("#")]
        assert not any("json.dump(" in l for l in code)

    def test_ci_wrapper_runs_v1_1_c_coverage_audit(self):
        content = Path("scripts/skillos/verify_skillos_v1_1_ci_audit.sh").read_text()
        assert "audit_golden_coverage_v1_1_c.py" in content

    def test_no_invoke_skill_import(self):
        import inspect
        import scripts.skillos.build_golden_coverage_v1_1_c as m
        assert "invoke_skill" not in inspect.getsource(m).lower().replace("_", "")

    def test_no_result_envelope_import(self):
        import inspect
        import scripts.skillos.audit_golden_coverage_v1_1_c as m
        assert "result_envelope" not in inspect.getsource(m).lower().replace("_", "")
