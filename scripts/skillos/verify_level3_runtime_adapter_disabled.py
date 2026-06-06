#!/usr/bin/env python3
"""Verify SkillOS Level 3 runtime adapter disabled mode: zero side effects."""

import os, sys
from pathlib import Path
from tempfile import TemporaryDirectory

if "SKILLOS_LEVEL3_ENABLED" in os.environ:
    del os.environ["SKILLOS_LEVEL3_ENABLED"]

from zmatrix.agent.skillos_level3_config import is_level3_enabled, get_level3_config
from zmatrix.agent.skillos_level3_runtime_adapter import build_runtime_adapter_event, run_level3_runtime_adapter


def main():
    errors = []

    # 1. Default disabled
    if is_level3_enabled():
        errors.append("default should be disabled")

    config = get_level3_config()
    if config.enabled:
        errors.append("config.enabled should be False")

    # 2. Disabled: observer not called
    event = build_runtime_adapter_event(event_id="t1", skill_id="S.X")
    r = run_level3_runtime_adapter(event)
    if r["observer_called"]:
        errors.append("observer called in disabled mode")
    if r["written"]:
        errors.append("should not write in disabled mode")

    # 3. Disabled: no audit path creation
    with TemporaryDirectory() as td:
        c = get_level3_config(td)
        run_level3_runtime_adapter(event, config=c)
        if Path(td).exists() and any(Path(td).iterdir()):
            errors.append("disabled mode created audit path")

    # 4. Disabled: result checks
    for key, expected in [("runtime_action", "CONTINUE"), ("caller_visible_warning", False),
                           ("result_envelope_mutation", False), ("runtime_blocking", False),
                           ("enforcement", "DISABLED")]:
        if r[key] != expected:
            errors.append(f"{key} should be {expected}, got {r[key]}")

    # 5. Adapter failure (enabled mode) returns CONTINUE
    os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
    def failing_observer(event, config=None):
        raise RuntimeError("test failure")
    r2 = run_level3_runtime_adapter(event, observer_fn=failing_observer)
    del os.environ["SKILLOS_LEVEL3_ENABLED"]
    if r2["runtime_action"] != "CONTINUE":
        errors.append(f"adapter failure should return CONTINUE: {r2}")
    if r2["error"] is None:
        errors.append("adapter failure should record error")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print("Z_SKILLOS_LEVEL3_RUNTIME_ADAPTER_DISABLED_VERIFY_FAIL_CI")
        sys.exit(1)

    print("Z_SKILLOS_LEVEL3_RUNTIME_ADAPTER_DISABLED_VERIFY_PASS")


if __name__ == "__main__":
    main()
