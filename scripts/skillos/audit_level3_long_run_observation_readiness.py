#!/usr/bin/env python3
"""Audit Level 3 long-run observation readiness. 50 repeated runs. Tmp paths only."""

import os, sys, json
from pathlib import Path
from tempfile import TemporaryDirectory

LONG_RUN_RUNS = 50

from zmatrix.agent.skillos_level3_config import get_level3_config
from zmatrix.agent.skillos_level3_runtime_adapter import build_runtime_adapter_event, run_level3_runtime_adapter


def main():
    errors = []
    sentinel = {"skill_id": "LONGRUN.SENTINEL", "status": "DRAFT_CREATED"}

    # 1. Disabled long-run window
    os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)
    dcfg = get_level3_config("nonexistent_long_disabled")
    for i in range(LONG_RUN_RUNS):
        ev = build_runtime_adapter_event(event_id=f"ld-{i}", skill_id="S.X")
        r = run_level3_runtime_adapter(ev, result_envelope=sentinel, config=dcfg)
        if r["written"]:
            errors.append(f"disabled run {i} wrote")

    # 2. Enabled long-run window
    with TemporaryDirectory() as td:
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
        try:
            c = get_level3_config(td)
            for i in range(LONG_RUN_RUNS):
                ev = build_runtime_adapter_event(event_id=f"le-{i}", skill_id="S.X", input_hash=f"in{i}", output_hash=f"out{i}")
                r = run_level3_runtime_adapter(ev, result_envelope=sentinel, config=c)
                if not r["written"]:
                    errors.append(f"enabled run {i} no write")
                if r["caller_visible_warning"]:
                    errors.append(f"enabled run {i} warning")
                if r["runtime_blocking"]:
                    errors.append(f"enabled run {i} blocking")
                if r["enforcement"] != "DISABLED":
                    errors.append(f"enabled run {i} enforcement={r['enforcement']}")

            audit_file = Path(td) / "shadow_audit.jsonl"
            if not audit_file.exists():
                errors.append("audit file not created")
            else:
                lines = audit_file.read_text().strip().split("\n")
                if len(lines) != LONG_RUN_RUNS:
                    errors.append(f"expected {LONG_RUN_RUNS} lines, got {len(lines)}")
        finally:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]

    # 3. Failure long-run window
    os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
    try:
        def fail_obs(e, c=None):
            raise RuntimeError("long fail")
        for i in range(LONG_RUN_RUNS):
            ev = build_runtime_adapter_event(event_id=f"lf-{i}", skill_id="S.X")
            r = run_level3_runtime_adapter(ev, observer_fn=fail_obs, result_envelope=sentinel)
            if r["runtime_action"] != "CONTINUE":
                errors.append(f"fail run {i} action={r['runtime_action']}")
    finally:
        del os.environ["SKILLOS_LEVEL3_ENABLED"]

    if sentinel["status"] != "DRAFT_CREATED":
        errors.append("sentinel mutated during long run")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print("Z_SKILLOS_LEVEL3_LONG_RUN_OBSERVATION_READINESS_FAIL_CI")
        return 1

    print("Z_SKILLOS_LEVEL3_LONG_RUN_OBSERVATION_READINESS_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
