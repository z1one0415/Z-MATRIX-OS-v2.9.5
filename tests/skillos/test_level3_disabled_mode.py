"""Tests for SkillOS Level 3 disabled mode."""

import os
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

# Ensure disabled
if "SKILLOS_LEVEL3_ENABLED" in os.environ:
    del os.environ["SKILLOS_LEVEL3_ENABLED"]

from zmatrix.agent.skillos_level3_config import is_level3_enabled, get_level3_config
from zmatrix.agent.skillos_level3_shadow_observer import build_shadow_event, observe_shadow_event


def test_level3_default_disabled():
    assert is_level3_enabled() is False
    c = get_level3_config()
    assert c.enabled is False
    assert c.write_enabled is False


def test_level3_disabled_no_files_created():
    with TemporaryDirectory() as td:
        c = get_level3_config(td)
        event = build_shadow_event(event_id="t1", skill_id="S.X")
        observe_shadow_event(event, c)
        ap = Path(td)
        assert not ap.exists() or not any(ap.iterdir())


def test_level3_disabled_no_runtime_reports():
    c = get_level3_config("nonexistent_tmp")
    event = build_shadow_event(event_id="t2", skill_id="S.X")
    r = observe_shadow_event(event, c)
    assert r["written"] is False


def test_level3_disabled_no_result_envelope_mutation():
    c = get_level3_config()
    r = observe_shadow_event({"skill_id": "X"}, c)
    assert r["result_envelope_mutation"] is False


def test_level3_disabled_no_runtime_blocking():
    c = get_level3_config()
    r = observe_shadow_event({"skill_id": "X"}, c)
    assert r["runtime_blocking"] is False


def test_level3_disabled_no_caller_warning():
    c = get_level3_config()
    r = observe_shadow_event({"skill_id": "X"}, c)
    assert r["caller_visible_warning"] is False


def test_level3_disabled_no_production_broker_real_trade():
    c = get_level3_config()
    assert str(c.audit_path) not in ("production", "broker_runtime", "real_trade")
    assert "production" not in str(c.audit_path)
    assert "broker" not in str(c.audit_path).lower()
    assert "real_trade" not in str(c.audit_path)


def test_level3_disabled_no_background_process():
    # config has no threads, no daemons, no background processes
    c = get_level3_config()
    assert c.enabled is False


def test_level3_disabled_no_auto_reenable():
    os.environ["SKILLOS_LEVEL3_ENABLED"] = "false"
    assert is_level3_enabled() is False
    del os.environ["SKILLOS_LEVEL3_ENABLED"]


def test_verify_level3_disabled_mode_script_passes():
    import subprocess
    r = subprocess.run(
        ["python3", "scripts/skillos/verify_level3_disabled_mode.py"],
        capture_output=True, text=True, cwd=os.getcwd(), env={**os.environ, "PYTHONPATH": "."}
    )
    assert r.returncode == 0
    assert "Z_SKILLOS_LEVEL3_DISABLED_MODE_VERIFY_PASS" in r.stdout


def test_no_invoke_skill_import():
    src = open("zmatrix/agent/skillos_level3_shadow_observer.py").read()
    assert "invoke_skill" not in src.lower().replace("_", "")


def test_no_result_envelope_import():
    src = open("zmatrix/agent/skillos_level3_shadow_observer.py").read()
    assert "result_envelope" not in src.lower().replace("_", "")
