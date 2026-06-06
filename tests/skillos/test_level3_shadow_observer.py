"""Tests for SkillOS Level 3 shadow observer."""

import os
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

if "SKILLOS_LEVEL3_ENABLED" in os.environ:
    del os.environ["SKILLOS_LEVEL3_ENABLED"]

from zmatrix.agent.skillos_level3_config import get_level3_config
from zmatrix.agent.skillos_level3_shadow_observer import build_shadow_event, observe_shadow_event
from zmatrix.agent.skillos_level3_redaction import redact_telemetry


def test_build_shadow_event_shape():
    event = build_shadow_event(event_id="e1", skill_id="S.X", input_hash="abc", output_hash="def")
    assert event["event_id"] == "e1"
    assert event["skill_id"] == "S.X"
    assert event["input_hash"] == "abc"
    assert event["output_hash"] == "def"
    assert event["created_by"] == "skillos_level3_shadow_observer"


def test_observer_disabled_returns_continue():
    c = get_level3_config()
    event = build_shadow_event(event_id="t1", skill_id="S.X")
    r = observe_shadow_event(event, c)
    assert r["runtime_action"] == "CONTINUE"
    assert r["written"] is False


def test_observer_disabled_no_write():
    with TemporaryDirectory() as td:
        c = get_level3_config(td)
        event = build_shadow_event(event_id="t1", skill_id="S.X")
        observe_shadow_event(event, c)
        assert not Path(td).exists() or not any(Path(td).iterdir())


def test_observer_enabled_writes_only_tmp_audit_path():
    with TemporaryDirectory() as td:
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
        try:
            c = get_level3_config(td)
            assert c.enabled is True
            event = build_shadow_event(event_id="t2", skill_id="S.X", input_hash="abc")
            r = observe_shadow_event(event, c)
            assert r["written"] is True
            out = Path(td) / "shadow_audit.jsonl"
            assert out.exists()
            content = out.read_text()
            assert "t2" in content
            assert "S.X" in content
        finally:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]


def test_observer_enabled_writes_jsonl():
    with TemporaryDirectory() as td:
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
        try:
            c = get_level3_config(td)
            observe_shadow_event(build_shadow_event(event_id="a", skill_id="S1"), c)
            observe_shadow_event(build_shadow_event(event_id="b", skill_id="S2"), c)
            lines = (Path(td) / "shadow_audit.jsonl").read_text().strip().split("\n")
            assert len(lines) == 2
        finally:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]


def test_observer_rejects_forbidden_telemetry():
    os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
    try:
        c = get_level3_config()
        with pytest.raises(ValueError):
            redact_telemetry({"event_id": "e1", "skill_id": "S.X", "raw_prompt": "hi"})
    finally:
        del os.environ["SKILLOS_LEVEL3_ENABLED"]


def test_writer_failure_does_not_block_runtime():
    os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
    try:
        # Path that cannot be written to (/dev/null/something)
        c = get_level3_config("/dev/null/shadow_audit")
        event = build_shadow_event(event_id="t3", skill_id="S.X")
        r = observe_shadow_event(event, c)
        assert r["runtime_action"] == "CONTINUE"
        assert r["written"] is False
    finally:
        del os.environ["SKILLOS_LEVEL3_ENABLED"]


def test_observer_does_not_mutate_input_event():
    event = build_shadow_event(event_id="t4", skill_id="S.X")
    orig = dict(event)
    os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
    try:
        observe_shadow_event(event, get_level3_config())
    finally:
        del os.environ["SKILLOS_LEVEL3_ENABLED"]
    assert event == orig


def test_observer_no_runtime_warning():
    r = observe_shadow_event(build_shadow_event(event_id="t5", skill_id="S.X"))
    assert r["caller_visible_warning"] is False


def test_observer_enforcement_disabled():
    r = observe_shadow_event(build_shadow_event(event_id="t6", skill_id="S.X"))
    assert r["enforcement"] == "DISABLED"


def test_observer_no_runtime_reports_write():
    src = open("zmatrix/agent/skillos_level3_audit_writer.py").read()
    code = [l for l in src.split("\n") if not l.strip().startswith('#') and 'Never touches' not in l]
    assert "runtime_reports" not in "\n".join(code)


def test_observer_no_production_broker_real_trade():
    for f in ["skillos_level3_config.py", "skillos_level3_audit_writer.py", "skillos_level3_shadow_observer.py"]:
        src = open(f"zmatrix/agent/{f}").read()
        code = [l for l in src.split("\n") if not l.strip().startswith('#') and 'Never touches' not in l and 'no production' not in l.lower()]
        for w in ["production/", "broker_runtime/", "real_trade/"]:
            assert w not in "\n".join(code), f"{f} references {w}"
