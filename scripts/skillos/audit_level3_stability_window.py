#!/usr/bin/env python3
"""Audit Level 3 stability window. 20 repeated runs. Tmp paths only."""

import os, sys, json
from pathlib import Path
from tempfile import TemporaryDirectory

STABILITY_WINDOW_RUNS = 20

from zmatrix.agent.skillos_level3_config import is_level3_enabled, get_level3_config
from zmatrix.agent.skillos_level3_runtime_adapter import build_runtime_adapter_event, run_level3_runtime_adapter
from zmatrix.agent.skillos_level3_redaction import redact_telemetry


def main():
    errors = []
    sentinel = {"skill_id": "STABILITY.SENTINEL", "status": "DRAFT_CREATED"}

    # 1. Disabled repeated window
    os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)
    dconfig = get_level3_config("nonexistent_tmp_stability")
    for i in range(STABILITY_WINDOW_RUNS):
        ev = build_runtime_adapter_event(event_id=f"ds-{i}", skill_id="S.X")
        r = run_level3_runtime_adapter(ev, result_envelope=sentinel, config=dconfig)
        if r["written"]:
            errors.append(f"disabled run {i} wrote evidence")
        if r["observer_called"]:
            errors.append(f"disabled run {i} called observer")
        if r["runtime_action"] != "CONTINUE":
            errors.append(f"disabled run {i} action={r['runtime_action']}")

    # 2. Enabled repeated window
    with TemporaryDirectory() as td:
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
        try:
            c = get_level3_config(td)
            for i in range(STABILITY_WINDOW_RUNS):
                ev = build_runtime_adapter_event(event_id=f"es-{i}", skill_id="S.X", input_hash=f"in{i}", output_hash=f"out{i}")
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
                if len(lines) != STABILITY_WINDOW_RUNS:
                    errors.append(f"expected {STABILITY_WINDOW_RUNS} lines, got {len(lines)}")
                for j, line in enumerate(lines):
                    ev = json.loads(line)
                    allowed = {"event_id","skill_id","created_by","input_hash","output_hash"}
                    for k in ev:
                        if k not in allowed:
                            errors.append(f"line {j}: forbidden field {k}")
        finally:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]

    # 3. Failure stability window
    os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
    try:
        def fail_obs(e, c=None):
            raise RuntimeError("stability fail")
        for i in range(STABILITY_WINDOW_RUNS):
            ev = build_runtime_adapter_event(event_id=f"fs-{i}", skill_id="S.X")
            r = run_level3_runtime_adapter(ev, observer_fn=fail_obs, result_envelope=sentinel)
            if r["runtime_action"] != "CONTINUE":
                errors.append(f"failure run {i} action={r['runtime_action']}")
            if r["caller_visible_warning"]:
                errors.append(f"failure run {i} warning")
            if r["runtime_blocking"]:
                errors.append(f"failure run {i} blocking")
        if sentinel["status"] != "DRAFT_CREATED":
            errors.append("sentinel mutated during failure window")
    finally:
        del os.environ["SKILLOS_LEVEL3_ENABLED"]

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print("Z_SKILLOS_LEVEL3_STABILITY_WINDOW_FAIL_CI")
        return 1

    print("Z_SKILLOS_LEVEL3_STABILITY_WINDOW_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
