#!/usr/bin/env python3
"""Verify Level 3 invoke_skill disabled mode: zero side effects."""

import os, sys
from pathlib import Path

if "SKILLOS_LEVEL3_ENABLED" in os.environ:
    del os.environ["SKILLOS_LEVEL3_ENABLED"]

from zmatrix.agent.skillos_level3_config import is_level3_enabled
from zmatrix.agent.skill_invocation import _observe_level3_non_blocking


def main():
    errors = []

    if is_level3_enabled():
        errors.append("default should be disabled")

    # Basic result to observe
    test_result = {"skill_id": "T.SKILL", "status": "DRAFT_CREATED"}

    # 1. Disabled mode: must not raise
    try:
        _observe_level3_non_blocking(skill_id="T.SKILL", result=test_result)
    except Exception as e:
        errors.append(f"disabled mode should not raise: {e}")

    # 2. Disabled mode: must not modify result
    result_before = dict(test_result)
    _observe_level3_non_blocking(skill_id="T.SKILL", result=test_result)
    if test_result != result_before:
        errors.append("disabled mode should not modify result")

    # 3. Source check: no result_envelope mutation
    src = open("zmatrix/agent/skill_invocation.py").read()
    if "result_envelope_mutation" in src and "result_envelope_mutation" in src.split("return result")[0]:
        errors.append("invoke_skill sets result_envelope_mutation")

    # 4. Source check: no runtime blocking
    if "runtime_blocking" in src and "runtime_blocking" in src.split("return result")[0]:
        errors.append("invoke_skill sets runtime_blocking")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print("Z_SKILLOS_LEVEL3_INVOKE_SKILL_DISABLED_VERIFY_FAIL_CI")
        sys.exit(1)

    print("Z_SKILLOS_LEVEL3_INVOKE_SKILL_DISABLED_VERIFY_PASS")


if __name__ == "__main__":
    main()
