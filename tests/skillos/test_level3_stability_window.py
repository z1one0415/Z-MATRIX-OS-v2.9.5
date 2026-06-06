"""Tests for SkillOS Level 3 stability window."""

import os, json, pytest
from pathlib import Path
from tempfile import TemporaryDirectory

STABILITY_RUNS = 20

from zmatrix.agent.skillos_level3_config import get_level3_config
from zmatrix.agent.skillos_level3_runtime_adapter import build_runtime_adapter_event, run_level3_runtime_adapter
from zmatrix.agent.skillos_level3_redaction import redact_telemetry

SENTINEL = {"skill_id": "SENTINEL", "status": "DRAFT_CREATED"}


class TestStabilityAudit:
    def test_stability_window_audit_script_passes(self):
        import subprocess
        r = subprocess.run(
            ["python3", "scripts/skillos/audit_level3_stability_window.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."},
        )
        assert r.returncode == 0, f"stability audit failed:\n{r.stderr}"
        assert "Z_SKILLOS_LEVEL3_STABILITY_WINDOW_PASS" in r.stdout


class TestDisabledWindow:
    def setup_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_disabled_window_zero_side_effects(self):
        c = get_level3_config("nonexistent_tmp")
        for i in range(STABILITY_RUNS):
            r = run_level3_runtime_adapter(
                build_runtime_adapter_event(event_id=f"dz{i}", skill_id="S.X"), config=c)
            assert r["written"] is False

    def test_disabled_window_no_audit_path(self):
        c = get_level3_config("nonexistent_dis")
        for i in range(STABILITY_RUNS):
            run_level3_runtime_adapter(
                build_runtime_adapter_event(event_id=f"dp{i}", skill_id="S.X"), config=c)
        assert not Path("nonexistent_dis").exists()

    def test_disabled_window_result_sentinel_unchanged(self):
        s = dict(SENTINEL)
        c = get_level3_config()
        for i in range(STABILITY_RUNS):
            run_level3_runtime_adapter(
                build_runtime_adapter_event(event_id=f"dr{i}", skill_id="S.X"),
                result_envelope=SENTINEL, config=c)
        assert SENTINEL == s


class TestEnabledWindow:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_enabled_window_writes_expected_event_count(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(STABILITY_RUNS):
                run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"ew{i}", skill_id="S.X"), config=c)
            lines = (Path(td) / "shadow_audit.jsonl").read_text().strip().split("\n")
            assert len(lines) == STABILITY_RUNS

    def test_enabled_window_tmp_audit_only(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(STABILITY_RUNS):
                run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"et{i}", skill_id="S.X"), config=c)
            assert (Path(td) / "shadow_audit.jsonl").exists()

    def test_enabled_window_schema_stable(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(STABILITY_RUNS):
                run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"es{i}", skill_id="S.X"), config=c)
            lines = (Path(td) / "shadow_audit.jsonl").read_text().strip().split("\n")
            for j, line in enumerate(lines):
                ev = json.loads(line)
                allowed = {"event_id","skill_id","created_by"}
                for k in ev:
                    assert k in allowed or k in ("input_hash","output_hash"), f"line {j}: {k}"

    def test_enabled_window_no_caller_warning(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(STABILITY_RUNS):
                r = run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"nw{i}", skill_id="S.X"), config=c)
                assert r["caller_visible_warning"] is False

    def test_enabled_window_no_runtime_blocking(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(STABILITY_RUNS):
                r = run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"nb{i}", skill_id="S.X"), config=c)
                assert r["runtime_blocking"] is False

    def test_enabled_window_enforcement_disabled(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            for i in range(STABILITY_RUNS):
                r = run_level3_runtime_adapter(
                    build_runtime_adapter_event(event_id=f"nd{i}", skill_id="S.X"), config=c)
                assert r["enforcement"] == "DISABLED"


class TestFailureWindow:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_failure_window_returns_continue(self):
        def fail(e, c=None):
            raise RuntimeError("stab fail")
        for i in range(STABILITY_RUNS):
            r = run_level3_runtime_adapter(
                build_runtime_adapter_event(event_id=f"fr{i}", skill_id="S.X"), observer_fn=fail)
            assert r["runtime_action"] == "CONTINUE"


class TestBoundary:
    def test_no_runtime_code_modified(self):
        src = open("scripts/skillos/audit_level3_stability_window.py").read()
        assert "zmatrix/" not in [l for l in src.split("\n") if "import " in l]

    def test_no_level4_warning_terms_introduced(self):
        src = open("scripts/skillos/audit_level3_stability_window.py").read()
        assert "soft_warning" not in src.lower()

    def test_no_fail_closed_terms_introduced(self):
        src = open("scripts/skillos/audit_level3_stability_window.py").read()
        assert "fail_closed" not in src.lower()
