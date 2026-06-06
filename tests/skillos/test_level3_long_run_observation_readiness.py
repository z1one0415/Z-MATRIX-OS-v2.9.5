"""Tests for SkillOS Level 3 long-run observation readiness."""

import os, json, pytest
from pathlib import Path
from tempfile import TemporaryDirectory

LONG_RUN_RUNS = 50

from zmatrix.agent.skillos_level3_config import get_level3_config
from zmatrix.agent.skillos_level3_runtime_adapter import build_runtime_adapter_event, run_level3_runtime_adapter

SENTINEL = {"skill_id": "SENTINEL", "status": "DRAFT_CREATED"}


class TestAudit:
    def test_long_run_audit_script_passes(self):
        import subprocess
        r = subprocess.run(
            ["python3", "scripts/skillos/audit_level3_long_run_observation_readiness.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."},
        )
        assert r.returncode == 0, f"long run audit failed:\n{r.stderr}"
        assert "Z_SKILLOS_LEVEL3_LONG_RUN_OBSERVATION_READINESS_PASS" in r.stdout


class TestDisabledLongRun:
    def setup_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_disabled_no_side_effects(self):
        c = get_level3_config("nonexistent_long")
        for i in range(LONG_RUN_RUNS):
            r = run_level3_runtime_adapter(
                build_runtime_adapter_event(event_id=f"ld{i}", skill_id="S.X"), config=c)
            assert r["written"] is False

    def test_disabled_sentinel_unchanged(self):
        s = dict(SENTINEL)
        c = get_level3_config()
        for i in range(LONG_RUN_RUNS):
            run_level3_runtime_adapter(
                build_runtime_adapter_event(event_id=f"ls{i}", skill_id="S.X"),
                result_envelope=SENTINEL, config=c)
        assert SENTINEL == s


class TestEnabledLongRun:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_enabled_writes_expected_count(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(LONG_RUN_RUNS):
                run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"ew{i}", skill_id="S.X"), config=c)
            lines = (Path(td) / "shadow_audit.jsonl").read_text().strip().split("\n")
            assert len(lines) == LONG_RUN_RUNS

    def test_enabled_tmp_audit_only(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(LONG_RUN_RUNS):
                run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"et{i}", skill_id="S.X"), config=c)
            assert (Path(td) / "shadow_audit.jsonl").exists()

    def test_enabled_no_warning(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(LONG_RUN_RUNS):
                r = run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"nw{i}", skill_id="S.X"), config=c)
                assert r["caller_visible_warning"] is False

    def test_enabled_no_blocking(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(LONG_RUN_RUNS):
                r = run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"nb{i}", skill_id="S.X"), config=c)
                assert r["runtime_blocking"] is False

    def test_enabled_enforcement_disabled(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(LONG_RUN_RUNS):
                r = run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"nd{i}", skill_id="S.X"), config=c)
                assert r["enforcement"] == "DISABLED"


class TestFailureLongRun:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_failure_returns_continue(self):
        def fail(e, c=None):
            raise RuntimeError("long")
        for i in range(LONG_RUN_RUNS):
            r = run_level3_runtime_adapter(
                build_runtime_adapter_event(event_id=f"fr{i}", skill_id="S.X"), observer_fn=fail)
            assert r["runtime_action"] == "CONTINUE"
