#!/usr/bin/env python3
"""Audit Level 3 runtime observation evidence. Tmp paths only. No real runtime writes."""

import os, sys, json
from pathlib import Path
from tempfile import TemporaryDirectory

from zmatrix.agent.skillos_level3_config import is_level3_enabled, get_level3_config
from zmatrix.agent.skillos_level3_runtime_adapter import build_runtime_adapter_event, run_level3_runtime_adapter
from zmatrix.agent.skillos_level3_shadow_observer import build_shadow_event, observe_shadow_event
from zmatrix.agent.skillos_level3_audit_writer import write_shadow_audit_event
from zmatrix.agent.skillos_level3_redaction import redact_telemetry


def main():
    errors = []
    sentinel = {"skill_id": "EVIDENCE.SENTINEL", "status": "DRAFT_CREATED"}

    # 1. Disabled mode: zero side effects
    os.environ.pop("SKILLOS_LEVEL3_ENABLED", None)
    dconfig = get_level3_config("nonexistent_tmp_disabled")
    devent = build_runtime_adapter_event(event_id="dis-test", skill_id="S.X")
    dr = run_level3_runtime_adapter(devent, config=dconfig)
    if dr["written"]:
        errors.append("disabled wrote evidence")
    if dr["observer_called"]:
        errors.append("disabled called observer")

    # 2. Enabled mode: writes only to tmp audit path
    with TemporaryDirectory() as td:
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
        try:
            c = get_level3_config(td)
            event = build_runtime_adapter_event(event_id="ev-001", skill_id="S.X", input_hash="abc", output_hash="def")
            r = run_level3_runtime_adapter(event, result_envelope=sentinel, config=c)
            if not r["written"]:
                errors.append("enabled evidence not written")
            audit_file = Path(td) / "shadow_audit.jsonl"
            if not audit_file.exists():
                errors.append("audit file not created")
            else:
                line = audit_file.read_text().strip()
                ev = json.loads(line)
                allowed = {"event_id","skill_id","created_by","input_hash","output_hash"}
                for k in ev:
                    if k not in allowed:
                        errors.append(f"forbidden evidence field: {k}")
            # sentinel unchanged
            if sentinel["status"] != "DRAFT_CREATED":
                errors.append("sentinel mutated")
            # no warning/blocking
            if r["caller_visible_warning"]:
                errors.append("caller warning")
            if r["runtime_blocking"]:
                errors.append("runtime blocking")
            if r["enforcement"] != "DISABLED":
                errors.append("enforcement not DISABLED")
            if r["runtime_action"] != "CONTINUE":
                errors.append("runtime_action not CONTINUE")
        finally:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]

    # 3. Failure isolation
    os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
    try:
        def failing(e, c=None):
            raise RuntimeError("evidence fail")
        fr = run_level3_runtime_adapter(build_runtime_adapter_event(event_id="fail", skill_id="S.X"), observer_fn=failing)
        if fr["runtime_action"] != "CONTINUE":
            errors.append("failure not CONTINUE")
    finally:
        del os.environ["SKILLOS_LEVEL3_ENABLED"]

    # 4. Forbidden field rejected
    try:
        redact_telemetry({"event_id":"e","skill_id":"S.X","raw_prompt":"bad"})
        errors.append("forbidden field not rejected")
    except ValueError:
        pass  # expected

    # 5. Repeated stability
    with TemporaryDirectory() as td:
        os.environ["SKILLOS_LEVEL3_ENABLED"] = "true"
        try:
            c = get_level3_config(td)
            for i in range(3):
                ev = build_runtime_adapter_event(event_id=f"rep-{i}", skill_id="R.SKILL")
                r = run_level3_runtime_adapter(ev, config=c)
                if not r["written"]:
                    errors.append("repeated run missing write")
        finally:
            del os.environ["SKILLOS_LEVEL3_ENABLED"]

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print("Z_SKILLOS_LEVEL3_RUNTIME_OBSERVATION_EVIDENCE_FAIL_CI")
        return 1

    print("Z_SKILLOS_LEVEL3_RUNTIME_OBSERVATION_EVIDENCE_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
