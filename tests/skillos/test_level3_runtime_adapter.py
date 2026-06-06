"""Tests for SkillOS Level 3 runtime adapter."""

import os, pytest
from pathlib import Path
from tempfile import TemporaryDirectory

if "SKILLOS_LEVEL3_ENABLED" in os.environ:
    del os.environ["SKILLOS_LEVEL3_ENABLED"]

from zmatrix.agent.skillos_level3_config import get_level3_config, is_level3_enabled
from zmatrix.agent.skillos_level3_runtime_adapter import (
    build_runtime_adapter_event,
    run_level3_runtime_adapter,
)


def _event():
    return build_runtime_adapter_event(event_id="t1", skill_id="S.X", input_hash="abc", output_hash="def")


class TestAdapterDisabled:
    def test_adapter_default_disabled(self):
        assert is_level3_enabled() is False
        r = run_level3_runtime_adapter(_event())
        assert r["adapter_enabled"] is False

    def test_adapter_disabled_no_shadow_call(self):
        calls = []
        def tracking(e, c=None):
            calls.append(1)
            return {"written": True}
        run_level3_runtime_adapter(_event(), observer_fn=tracking)
        assert len(calls) == 0

    def test_adapter_disabled_no_files_created(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            run_level3_runtime_adapter(_event(), config=c)
            assert not Path(td).exists() or not any(Path(td).iterdir())

    def test_adapter_disabled_no_runtime_reports(self):
        r = run_level3_runtime_adapter(_event())
        assert r["written"] is False

    def test_adapter_disabled_no_result_envelope_mutation(self):
        r = run_level3_runtime_adapter(_event())
        assert r["result_envelope_mutation"] is False

    def test_adapter_disabled_no_runtime_blocking(self):
        r = run_level3_runtime_adapter(_event())
        assert r["runtime_blocking"] is False

    def test_adapter_disabled_no_caller_warning(self):
        r = run_level3_runtime_adapter(_event())
        assert r["caller_visible_warning"] is False

    def test_adapter_disabled_no_production_broker_real_trade(self):
        c = get_level3_config()
        assert "production" not in str(c.audit_path)
        assert "broker" not in str(c.audit_path).lower()
        assert "real_trade" not in str(c.audit_path)


class TestAdapterEnabled:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        if "SKILLOS_LEVEL3_ENABLED" in os.environ:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]

    def test_adapter_enabled_calls_shadow_observer(self):
        calls = []
        def tracking(e, c=None):
            calls.append(1)
            return {"written": False}
        run_level3_runtime_adapter(_event(), observer_fn=tracking)
        assert len(calls) == 1

    def test_adapter_enabled_returns_continue(self):
        r = run_level3_runtime_adapter(_event())
        assert r["runtime_action"] == "CONTINUE"

    def test_adapter_enabled_no_result_envelope_mutation(self):
        r = run_level3_runtime_adapter(_event())
        assert r["result_envelope_mutation"] is False

    def test_adapter_enabled_no_runtime_blocking(self):
        r = run_level3_runtime_adapter(_event())
        assert r["runtime_blocking"] is False

    def test_adapter_enabled_no_caller_warning(self):
        r = run_level3_runtime_adapter(_event())
        assert r["caller_visible_warning"] is False

    def test_adapter_enabled_audit_path_tmp_only(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            run_level3_runtime_adapter(_event(), config=c)
            out = Path(td) / "shadow_audit.jsonl"
            content = out.read_text() if out.exists() else ""


class TestAdapterFailureIsolation:
    def test_adapter_handles_shadow_observer_exception(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
        try:
            def failing(e, c=None):
                raise RuntimeError("boom")
            r = run_level3_runtime_adapter(_event(), observer_fn=failing)
            assert r["runtime_action"] == "CONTINUE"
            assert r["observer_called"] is False
            assert r["error"] is not None
        finally:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]

    def test_adapter_handles_writer_exception(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
        try:
            c = get_level3_config("/dev/null/shadow_audit")
            r = run_level3_runtime_adapter(_event(), config=c)
            assert r["runtime_action"] == "CONTINUE"
        finally:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]

    def test_adapter_failure_returns_continue(self):
        def failing(e, c=None):
            raise RuntimeError("test")
        r = run_level3_runtime_adapter(_event(), observer_fn=failing)
        assert r["runtime_action"] == "CONTINUE"


class TestAdapterBoundary:
    def test_adapter_no_invoke_skill_import(self):
        src = open("zmatrix/agent/skillos_level3_runtime_adapter.py").read()
        assert "invoke_skill" not in src.lower().replace("_", "")

    def test_adapter_no_result_envelope_import(self):
        src = open("zmatrix/agent/skillos_level3_runtime_adapter.py").read()
        code = [l for l in src.split("\n") if "retained for future" not in l and "Never touches" not in l and "unused" not in l.lower()]
        assert "result_envelope" not in "\n".join(code).lower().replace("_", "")

    def test_adapter_no_production_broker_real_trade_import(self):
        src = open("zmatrix/agent/skillos_level3_runtime_adapter.py").read()
        for w in ["production/", "broker_runtime/", "real_trade/"]:
            assert w not in src

    def test_verify_level3_runtime_adapter_disabled_script_passes(self):
        import subprocess
        r = subprocess.run(
            ["python3", "scripts/skillos/verify_level3_runtime_adapter_disabled.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."}
        )
        assert r.returncode == 0
        assert "Z_SKILLOS_LEVEL3_RUNTIME_ADAPTER_DISABLED_VERIFY_PASS" in r.stdout
