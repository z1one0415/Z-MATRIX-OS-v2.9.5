"""Tests for SkillOS v1.1-B semantic drift audit."""

import json
import pytest
import copy
from pathlib import Path
from zmatrix.agent.skill_semantic_drift import (
    load_baseline_snapshot,
    build_current_snapshot,
    compare_snapshots,
    audit_semantic_drift,
    canonical_json_hash,
)

BASELINE_PATH = Path("data/research_db/agent/baselines/skillos_v1_1_b_semantic_drift_baseline.json")


class TestBaseline:
    def test_baseline_snapshot_exists(self):
        assert BASELINE_PATH.exists()

    def test_baseline_snapshot_has_no_dynamic_fields(self):
        text = BASELINE_PATH.read_text()
        assert "timestamp" not in text.lower()
        assert "generated_at" not in text.lower()


class TestCurrentSnapshot:
    def test_current_snapshot_shape(self):
        current = build_current_snapshot()
        for key in ["contract_registry", "hash_policy", "golden_hash_lock", "golden_regression"]:
            assert key in current, f"missing key: {key}"

    def test_current_snapshot_has_schema_projection(self):
        current = build_current_snapshot()
        cr = current["contract_registry"]
        assert "schema_projection_sha256" in cr
        assert len(cr["schema_projection_sha256"]) == 64


class TestDriftDetection:
    def test_current_baseline_no_drift(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        result = compare_snapshots(baseline, current)
        assert result["drift_detected"] is False
        assert result["max_severity"] == "INFO"

    def test_contract_count_drift_detected(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        mutated = copy.deepcopy(current)
        mutated["contract_registry"]["contract_count"] = 999
        result = compare_snapshots(baseline, mutated)
        assert result["drift_detected"] is True
        assert result["max_severity"] == "FAIL_CI"

    def test_schema_projection_drift_detected(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        mutated = copy.deepcopy(current)
        mutated["contract_registry"]["schema_projection_sha256"] = "deadbeef" * 8
        result = compare_snapshots(baseline, mutated)
        assert result["drift_detected"] is True

    def test_hash_policy_drift_detected(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        mutated = copy.deepcopy(current)
        mutated["hash_policy"]["sha256"] = "deadbeef" * 8
        result = compare_snapshots(baseline, mutated)
        assert result["drift_detected"] is True

    def test_golden_case_drift_detected(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        mutated = copy.deepcopy(current)
        mutated["golden_hash_lock"]["sha256"] = "deadbeef" * 8
        result = compare_snapshots(baseline, mutated)
        assert result["drift_detected"] is True

    def test_regression_coverage_loss_detected(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        mutated = copy.deepcopy(current)
        mutated["golden_regression"]["case_count"] = 1
        result = compare_snapshots(baseline, mutated)
        assert result["drift_detected"] is True

    def test_regression_coverage_increase_warn(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        mutated = copy.deepcopy(current)
        mutated["golden_regression"]["case_count"] = 999
        result = compare_snapshots(baseline, mutated)
        assert result["drift_detected"] is False  # WARN is not drift
        reg = [t for t in result["targets"] if t["target"] == "golden_regression"][0]
        assert reg["severity"] == "WARN"

    def test_regression_domain_increase_warn(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        mutated = copy.deepcopy(current)
        mutated["golden_regression"]["domains_covered"] = 99
        result = compare_snapshots(baseline, mutated)
        reg = [t for t in result["targets"] if t["target"] == "golden_regression"][0]
        assert reg["severity"] == "WARN"

    def test_regression_same_count_hash_change_fail_ci(self):
        baseline = load_baseline_snapshot()
        current = build_current_snapshot()
        mutated = copy.deepcopy(current)
        # Same count, same domains, but hash changed
        mutated["golden_regression"]["sha256"] = "deadbeef" * 8
        result = compare_snapshots(baseline, mutated)
        assert result["drift_detected"] is True
        reg = [t for t in result["targets"] if t["target"] == "golden_regression"][0]
        assert reg["severity"] == "FAIL_CI"

    def test_severity_never_fail_closed(self):
        result = audit_semantic_drift()
        assert result["max_severity"] in ("INFO", "WARN", "FAIL_CI")
        assert result["max_severity"] != "FAIL_CLOSED"

    def test_audit_never_blocks(self):
        result = audit_semantic_drift()
        assert result["blocked"] is False
        assert result["runtime_action"] == "NONE"


class TestNoModifications:
    def test_auditor_no_runtime_reports_write(self):
        source = Path("scripts/skillos/audit_semantic_drift.py").read_text()
        code = [l for l in source.split("\n") if not l.strip().startswith("#")]
        assert not any("json.dump(" in l for l in code)
        assert not any("open(" in l and ("'w'" in l or '"w"' in l) for l in code)

    def test_no_invoke_skill_import(self):
        import inspect
        from zmatrix.agent import skill_semantic_drift
        source = inspect.getsource(skill_semantic_drift)
        assert "invoke_skill" not in source.lower().replace("_", "")

    def test_no_result_envelope_import(self):
        import inspect
        from zmatrix.agent import skill_semantic_drift
        source = inspect.getsource(skill_semantic_drift)
        assert "result_envelope" not in source.lower().replace("_", "")

    def test_cli_passes_current_baseline(self):
        import subprocess, os
        r = subprocess.run(
            ["python3", "scripts/skillos/audit_semantic_drift.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."}
        )
        assert "Z_SKILLOS_V1_1_B_SEMANTIC_DRIFT_AUDIT_PASS" in r.stdout
        assert r.returncode == 0
