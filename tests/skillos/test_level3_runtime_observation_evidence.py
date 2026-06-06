"""Tests for SkillOS Level 3 runtime observation evidence."""

import os, json, pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from zmatrix.agent.skillos_level3_config import get_level3_config
from zmatrix.agent.skillos_level3_runtime_adapter import build_runtime_adapter_event, run_level3_runtime_adapter
from zmatrix.agent.skillos_level3_redaction import redact_telemetry

SENTINEL = {"skill_id": "T.SENTINEL", "status": "DRAFT_CREATED"}


class TestEvidenceBasics:
    def test_evidence_audit_script_passes(self):
        import subprocess
        r = subprocess.run(
            ["python3", "scripts/skillos/audit_level3_runtime_observation_evidence.py"],
            capture_output=True, text=True, cwd=os.getcwd(),
            env={**os.environ, "PYTHONPATH": "."},
        )
        assert r.returncode == 0, f"audit failed:\n{r.stderr}"
        assert "Z_SKILLOS_LEVEL3_RUNTIME_OBSERVATION_EVIDENCE_PASS" in r.stdout

    def test_disabled_mode_remains_zero_side_effect(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)
        c = get_level3_config("nonexistent_tmp")
        ev = build_runtime_adapter_event(event_id="dz", skill_id="S.X")
        r = run_level3_runtime_adapter(ev, config=c)
        assert r["written"] is False


class TestEnabledEvidence:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_enabled_mode_writes_tmp_audit_evidence(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            ev = build_runtime_adapter_event(event_id="ee", skill_id="S.X")
            r = run_level3_runtime_adapter(ev, result_envelope=SENTINEL, config=c)
            assert r["written"] is True
            assert (Path(td) / "shadow_audit.jsonl").exists()

    def test_enabled_evidence_schema_allowed_only(self):
        with TemporaryDirectory() as td:
            c = get_level3_config(td)
            ev = build_runtime_adapter_event(event_id="sc", skill_id="S.X", input_hash="a", output_hash="b")
            run_level3_runtime_adapter(ev, config=c)
            out = json.loads((Path(td) / "shadow_audit.jsonl").read_text())
            allowed = {"event_id","skill_id","created_by","input_hash","output_hash"}
            for k in out:
                assert k in allowed, f"forbidden field: {k}"

    def test_enabled_evidence_rejects_forbidden_fields(self):
        with pytest.raises(ValueError):
            redact_telemetry({"event_id":"e","skill_id":"S","raw_prompt":"x"})


class TestSafetyDuringEvidence:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_result_envelope_unchanged(self):
        with TemporaryDirectory() as td:
            orig = dict(SENTINEL)
            ev = build_runtime_adapter_event(event_id="ru", skill_id="S.X")
            run_level3_runtime_adapter(ev, result_envelope=SENTINEL, config=get_level3_config(td))
            assert SENTINEL == orig

    def test_no_caller_visible_warning_during_evidence(self):
        with TemporaryDirectory() as td:
            r = run_level3_runtime_adapter(build_runtime_adapter_event(event_id="nw", skill_id="S.X"), config=get_level3_config(td))
            assert r["caller_visible_warning"] is False

    def test_no_runtime_blocking_during_evidence(self):
        with TemporaryDirectory() as td:
            r = run_level3_runtime_adapter(build_runtime_adapter_event(event_id="nb", skill_id="S.X"), config=get_level3_config(td))
            assert r["runtime_blocking"] is False

    def test_enforcement_disabled_during_evidence(self):
        with TemporaryDirectory() as td:
            r = run_level3_runtime_adapter(build_runtime_adapter_event(event_id="ne", skill_id="S.X"), config=get_level3_config(td))
            assert r["enforcement"] == "DISABLED"


class TestFailureIsolation:
    def setup_method(self):
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"

    def teardown_method(self):
        os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)

    def test_adapter_failure_returns_continue(self):
        def fail(e, c=None):
            raise RuntimeError("adapt fail")
        r = run_level3_runtime_adapter(build_runtime_adapter_event(event_id="af", skill_id="S.X"), observer_fn=fail)
        assert r["runtime_action"] == "CONTINUE"


class TestBoundary:
    def test_no_runtime_reports_written(self):
        src = open("scripts/skillos/audit_level3_runtime_observation_evidence.py").read()
        assert "runtime_reports" not in src.replace("(", " ").split("runtime_reports(")[0]

    def test_no_production_broker_real_trade(self):
        src = open("scripts/skillos/audit_level3_runtime_observation_evidence.py").read()
        for w in ["production/", "broker_runtime/", "real_trade/"]:
            assert w not in src

    def test_no_level4_warning_terms_introduced(self):
        src = open("scripts/skillos/audit_level3_runtime_observation_evidence.py").read()
        assert "soft_warning" not in src.lower()

    def test_no_fail_closed_terms_introduced(self):
        src = open("scripts/skillos/audit_level3_runtime_observation_evidence.py").read()
        assert "fail_closed" not in src.lower()
