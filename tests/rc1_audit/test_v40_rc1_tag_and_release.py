#!/usr/bin/env python3
"""V4.0-RC1: Tagging & Release Note Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent


def test_rc1_manifest_exists_and_is_research_only():
    text = (WORKSPACE / "docs" / "release" / "V4_0_RC1_MANIFEST.md").read_text(encoding="utf-8")
    assert "v4.0-rc1" in text
    assert "Research-only" in text
    assert "BLOCKED" in text
    assert "Tag created" in text


def test_rc1_release_note_disclaims_production():
    text = (WORKSPACE / "docs" / "release" / "V4_0_RC1_RELEASE_NOTE.md").read_text(encoding="utf-8")
    t = text.lower()
    assert "not production-ready" in t
    assert "does not enable broker" in t
    assert "does not allow real trade" in t
    assert "Paper-only: TRUE" in text
    assert "Human review required: TRUE" in text


def test_cloud_lock_records_tag_but_not_production():
    data = json.loads((WORKSPACE / "docs" / "rc1_audit" / "RC1_CLOUD_EVIDENCE_LOCK.json").read_text(encoding="utf-8"))
    assert data["rc1_tag_created"] is True
    assert data["rc1_tag"] == "v4.0-rc1"
    assert data["rc1_tag_target"] == "f8796f714740b5e8c76ab53d768888a8de87dfdd"
    assert data["production_status"] == "BLOCKED"
    assert data["broker_runtime_status"] == "BLOCKED"
    assert data["real_trade_status"] == "BLOCKED"


def test_release_docs_do_not_claim_runtime_or_production_ready():
    files = [
        "docs/release/V4_0_RC1_MANIFEST.md",
        "docs/release/V4_0_RC1_RELEASE_NOTE.md",
        "docs/rc1_audit/RC1_READINESS_AUDIT_REPORT.md",
    ]
    combined = "\n".join((WORKSPACE / p).read_text(encoding="utf-8") for p in files)
    for forbidden in [
        "Production: READY",
        "Broker/runtime: READY",
        "Real trade: READY",
        "Autonomous trading ready",
        "production_allowed=True",
        "broker_order_allowed=True",
        "real_trade_allowed=True",
        "runtime_enabled=True",
    ]:
        assert forbidden not in combined, f"Forbidden: {forbidden}"


if __name__ == "__main__":
    test_rc1_manifest_exists_and_is_research_only()
    test_rc1_release_note_disclaims_production()
    test_cloud_lock_records_tag_but_not_production()
    test_release_docs_do_not_claim_runtime_or_production_ready()
    print("✅ V4.0-RC1 Tag & Release tests PASS")
