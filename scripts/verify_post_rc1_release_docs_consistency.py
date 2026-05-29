#!/usr/bin/env python3
"""PRI-2: Post-RC1 Release Docs Consistency Audit"""
import json
from pathlib import Path

def verify():
    manifest = Path("docs/release/V4_0_RC1_MANIFEST.md").read_text(encoding="utf-8")
    note = Path("docs/release/V4_0_RC1_RELEASE_NOTE.md").read_text(encoding="utf-8")
    audit = Path("docs/rc1_audit/RC1_READINESS_AUDIT_REPORT.md").read_text(encoding="utf-8")
    lock = json.loads(Path("docs/rc1_audit/RC1_CLOUD_EVIDENCE_LOCK.json").read_text(encoding="utf-8"))

    combined = "\n".join([manifest, note, audit])

    required = [
        "v4.0-rc1",
        "f8796f714740b5e8c76ab53d768888a8de87dfdd",
        "26629922144",
        "success",
        "100/100",
        "RC1_READY_RECOMMENDED",
        "Production: BLOCKED",
        "Broker/runtime: BLOCKED",
        "Real trade: BLOCKED",
        "Paper-only: TRUE",
        "Human review required: TRUE",
    ]
    for item in required:
        assert item in combined, f"Missing: {item}"

    assert lock["rc1_tag_created"] is True
    assert lock["rc1_tag"] == "v4.0-rc1"
    assert lock["rc1_tag_target"] == "f8796f714740b5e8c76ab53d768888a8de87dfdd"
    assert lock["workflow_conclusion"] == "success"
    assert lock["production_status"] == "BLOCKED"
    assert lock["broker_runtime_status"] == "BLOCKED"
    assert lock["real_trade_status"] == "BLOCKED"

    forbidden = [
        "Production: READY",
        "Broker/runtime: READY",
        "Real trade: READY",
        "production_allowed=True",
        "broker_order_allowed=True",
        "real_trade_allowed=True",
        "runtime_enabled=True",
        "Autonomous trading ready",
    ]
    for item in forbidden:
        assert item not in combined, f"Forbidden: {item}"

    print("✅ Post-RC1 release docs consistency PASS")

if __name__ == "__main__":
    verify()
