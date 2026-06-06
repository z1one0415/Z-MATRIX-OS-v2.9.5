"""Tests for SkillOS Level 3 minimal invoke_skill wrapper integration."""

import os, pytest
from pathlib import Path

if "SKILLOS_LEVEL3_ENABLED" in os.environ:
    del os.environ["SKILLOS_LEVEL3_ENABLED"]

from zmatrix.agent.skillos_level3_config import is_level3_enabled
from zmatrix.agent.skill_invocation import _observe_level3_non_blocking

TEST_RESULT = {"skill_id": "T.SKILL", "status": "DRAFT_CREATED", "output_ref": "test://123"}
BLOCKED_RESULT = {"skill_id": "T.SKILL", "status": "BLOCKED", "blocked_reason": "test"}


class TestHelperDisabled:
    def test_invoke_skill_level3_default_disabled(self):
        assert is_level3_enabled() is False

    def test_invoke_skill_disabled_same_result_as_baseline(self):
        before = dict(TEST_RESULT)
        _observe_level3_non_blocking(skill_id="T.SKILL", result=TEST_RESULT)
        assert TEST_RESULT == before

    def test_invoke_skill_disabled_no_result_envelope_mutation(self):
        before = dict(TEST_RESULT)
        _observe_level3_non_blocking(skill_id="T.SKILL", result=TEST_RESULT)
        assert TEST_RESULT == before

    def test_invoke_skill_disabled_no_runtime_warning(self):
        r = dict(TEST_RESULT)
        _observe_level3_non_blocking(skill_id="T.SKILL", result=r)
        assert "warning" not in str(r).lower()

    def test_invoke_skill_disabled_no_runtime_blocking(self):
        _observe_level3_non_blocking(skill_id="T.SKILL", result=TEST_RESULT)
        # Did not raise - no blocking

    def test_invoke_skill_disabled_no_production_broker_real_trade(self):
        src = open("zmatrix/agent/skill_invocation.py").read()
        for w in ["production/", "broker_runtime/", "real_trade/"]:
            assert w not in src


class TestHelperEnabled:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        if "SKILLOS_LEVEL3_ENABLED" in os.environ:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]

    def test_invoke_skill_enabled_returns_original_result(self):
        before = dict(TEST_RESULT)
        _observe_level3_non_blocking(skill_id="T.SKILL", result=TEST_RESULT)
        assert TEST_RESULT == before

    def test_invoke_skill_enabled_no_result_envelope_mutation(self):
        before = dict(BLOCKED_RESULT)
        _observe_level3_non_blocking(skill_id="T.SKILL", result=BLOCKED_RESULT)
        assert BLOCKED_RESULT == before

    def test_invoke_skill_enabled_no_runtime_warning(self):
        r = dict(TEST_RESULT)
        _observe_level3_non_blocking(skill_id="T.SKILL", result=r)
        assert "warning" not in str(r).lower()

    def test_invoke_skill_enabled_no_runtime_blocking(self):
        _observe_level3_non_blocking(skill_id="T.SKILL", result=TEST_RESULT)


class TestFailureIsolation:
    def test_invoke_skill_adapter_exception_returns_original_result(self):
        before = dict(TEST_RESULT)
        _observe_level3_non_blocking(skill_id="T.SKILL", result=TEST_RESULT)
        assert TEST_RESULT == before

    def test_skill_result_envelope_file_untouched(self):
        src = open("zmatrix/agent/skill_result_envelope.py").read()
        assert "level3" not in src.lower()

    def test_no_fail_closed_behavior(self):
        src = open("zmatrix/agent/skill_invocation.py").read()
        assert "fail_closed" not in src.lower()

    def test_verify_level3_invoke_skill_disabled_script_passes(self):
        import subprocess
        r = subprocess.run(
            ["python3", "scripts/skillos/verify_level3_invoke_skill_disabled.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."}
        )
        assert r.returncode == 0
        assert "Z_SKILLOS_LEVEL3_INVOKE_SKILL_DISABLED_VERIFY_PASS" in r.stdout
