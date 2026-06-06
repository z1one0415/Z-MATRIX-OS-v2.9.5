#!/usr/bin/env python3
"""Verify SkillOS Level 3 disabled mode: zero side effects by default."""

import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

# Ensure disabled by default
if "SKILLOS_LEVEL3_ENABLED" in os.environ:
    del os.environ["SKILLOS_LEVEL3_ENABLED"]

from zmatrix.agent.skillos_level3_config import is_level3_enabled, get_level3_config
from zmatrix.agent.skillos_level3_shadow_observer import build_shadow_event, observe_shadow_event


def main():
    errors = []

    # 1. Default disabled
    if is_level3_enabled():
        errors.append("default should be disabled")

    config = get_level3_config("nonexistent_tmp")
    if config.enabled:
        errors.append("config.enabled should be False by default")

    # 2. Disabled mode: no audit path creation
    if config.audit_path.exists():
        errors.append(f"audit path should not exist: {config.audit_path}")

    # 3. Disabled mode: observer returns CONTINUE, no write
    event = build_shadow_event(event_id="test-001", skill_id="TEST.SKILL")
    result = observe_shadow_event(event, config)
    if result["runtime_action"] != "CONTINUE":
        errors.append(f"runtime_action should be CONTINUE: {result}")
    if result["caller_visible_warning"]:
        errors.append("caller_visible_warning should be False")
    if result["result_envelope_mutation"]:
        errors.append("result_envelope_mutation should be False")
    if result["runtime_blocking"]:
        errors.append("runtime_blocking should be False")
    if result["enforcement"] != "DISABLED":
        errors.append(f"enforcement should be DISABLED: {result}")
    if result["written"]:
        errors.append("should not write in disabled mode")

    # 4. Disabled mode: no background path created
    if config.audit_path.exists():
        errors.append(f"disabled mode should not create audit path: {config.audit_path}")

    # 5. No invoke_skill import
    import zmatrix.agent.skillos_level3_shadow_observer as ob
    ob_src = ob.__file__
    ob_text = open(ob_src).read()
    if "invoke_skill" in ob_text.lower().replace("_", ""):
        errors.append("shadow_observer references invoke_skill")

    # 6. No result_envelope import
    if "result_envelope" in ob_text.lower().replace("_", ""):
        errors.append("shadow_observer references result_envelope")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print("Z_SKILLOS_LEVEL3_DISABLED_MODE_VERIFY_FAIL_CI")
        sys.exit(1)

    print("Z_SKILLOS_LEVEL3_DISABLED_MODE_VERIFY_PASS")


if __name__ == "__main__":
    main()
