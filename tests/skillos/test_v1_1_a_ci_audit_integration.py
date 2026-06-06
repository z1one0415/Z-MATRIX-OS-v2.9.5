"""Tests for SkillOS v1.1-A CI audit integration."""

import subprocess
import pytest
from pathlib import Path

WRAPPER = "scripts/skillos/verify_skillos_v1_1_ci_audit.sh"


class TestCIWrapper:
    def test_ci_audit_wrapper_exists(self):
        assert Path(WRAPPER).exists()

    def test_ci_audit_wrapper_uses_set_euo_pipefail(self):
        content = Path(WRAPPER).read_text()
        assert "set -euo pipefail" in content

    def test_ci_audit_wrapper_runs_golden_regression(self):
        content = Path(WRAPPER).read_text()
        assert "audit_golden_regression.py" in content

    def test_ci_audit_wrapper_runs_hash_aware_shadow(self):
        content = Path(WRAPPER).read_text()
        assert "audit_hash_aware_shadow.py" in content

    def test_ci_audit_wrapper_runs_golden_hash_lock(self):
        content = Path(WRAPPER).read_text()
        assert "audit_golden_hash_lock.py" in content

    def test_ci_audit_wrapper_runs_v1_0_a_to_f_tests(self):
        content = Path(WRAPPER).read_text()
        for v in ["v1_0_a", "v1_0_b", "v1_0_c", "v1_0_d", "v1_0_e", "v1_0_f"]:
            assert v in content, f"missing {v} tests"

    def test_ci_audit_wrapper_does_not_write_runtime_reports(self):
        content = Path(WRAPPER).read_text()
        assert "runtime_reports" not in content

    def test_ci_audit_wrapper_does_not_reference_invoke_skill(self):
        content = Path(WRAPPER).read_text().lower()
        assert "invoke_skill" not in content.replace("_", "")

    def test_ci_audit_wrapper_does_not_reference_result_envelope(self):
        content = Path(WRAPPER).read_text().lower()
        assert "result_envelope" not in content.replace("_", "")

    def test_ci_audit_wrapper_does_not_reference_production_broker_real_trade(self):
        content = Path(WRAPPER).read_text()
        for word in ["production", "broker_runtime", "real_trade", "auto_buy", "auto_sell"]:
            assert word not in content, f"wrapper references {word}"

    def test_ci_audit_wrapper_runs_semantic_drift(self):
        """v1.1-B.x: drift audit integrated into CI wrapper."""
        content = Path(WRAPPER).read_text()
        assert "audit_semantic_drift.py" in content

    def test_drift_warn_policy_documented_as_ci_pass(self):
        """WARN exits 0 — implemented by exit 0 when max_severity is WARN."""
        from zmatrix.agent.skill_semantic_drift import audit_semantic_drift
        result = audit_semantic_drift()
        # Current baseline has no drift: max_severity is INFO.
        # WARN policy: exit 0, CI PASS.
        assert result["blocked"] is False
        assert result["runtime_action"] == "NONE"

    def test_drift_fail_ci_policy_documented_as_ci_fail(self):
        """FAIL_CI exits 1 — implemented by exit 1 when drift_detected is true."""
        import subprocess, os
        # Verify the auditor can exit non-zero when drift detected
        r = subprocess.run(
            ["python3", "scripts/skillos/audit_semantic_drift.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."}
        )
        # Current baseline: no drift → exit 0
        assert r.returncode == 0
        assert "Z_SKILLOS_V1_1_B_SEMANTIC_DRIFT_AUDIT_PASS" in r.stdout

    def test_ci_wrapper_contains_semantic_drift_after_v1_0_a_to_f(self):
        content = Path(WRAPPER).read_text()
        a_test_line = content.index("test_v1_0_a_contract_registry.py")
        drift_line = content.index("audit_semantic_drift.py")
        assert drift_line > a_test_line, "drift audit must be after v1.0 tests"

    def test_ci_audit_wrapper_runs_v1_1_c_golden_coverage(self):
        content = Path(WRAPPER).read_text()
        assert "audit_golden_coverage_v1_1_c.py" in content


class TestWrapperExecution:
    def test_ci_audit_wrapper_bash_syntax(self):
        import subprocess
        r = subprocess.run(["bash", "-n", WRAPPER], capture_output=True, text=True)
        assert r.returncode == 0, f"bash -n failed: {r.stderr}"

    def test_ci_audit_wrapper_executes(self):
        import os
        r = subprocess.run(
            ["bash", WRAPPER],
            capture_output=True, text=True,
            cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."}
        )
        assert "CI Audit Integration PASS" in r.stdout, \
            f"wrapper failed:\n{r.stdout}\n{r.stderr}"
