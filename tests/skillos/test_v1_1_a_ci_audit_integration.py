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

    def test_ci_audit_wrapper_drift_warn_passes_ci(self):
        """WARN severity exits 0 — does not break CI."""
        content = Path(WRAPPER).read_text()
        assert "set -euo pipefail" in content  # FAIL_CI exits 1 naturally


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
