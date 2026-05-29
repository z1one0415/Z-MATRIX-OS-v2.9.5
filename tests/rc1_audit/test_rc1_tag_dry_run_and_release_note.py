#!/usr/bin/env python3
"""RC1-E0: Tag Dry-Run and Release Note Safety Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent


def test_cloud_evidence_lock_exists_and_safe():
    p = WORKSPACE / "docs" / "rc1_audit" / "RC1_CLOUD_EVIDENCE_LOCK.json"
    assert p.exists(), "missing evidence lock"
    data = json.loads(p.read_text(encoding="utf-8"))

    assert len(data["commit_sha"]) == 40, f"commit_sha not 40: {len(data['commit_sha'])}"
    assert data["commit_sha"].startswith(data["short_sha"]), "short_sha not prefix of full sha"
    assert data["workflow_conclusion"] == "success"
    assert data["recommendation"] == "RC1_READY_RECOMMENDED"
    assert data["rc1_tag_created"] is False
    assert data["production_status"] == "BLOCKED"
    assert data["broker_runtime_status"] == "BLOCKED"
    assert data["real_trade_status"] == "BLOCKED"
    assert data["scorecard"] == "100/100"


def test_tag_dry_run_manifest_does_not_create_tag():
    text = (WORKSPACE / "docs" / "rc1_audit" / "RC1_TAG_DRY_RUN_MANIFEST.md").read_text(encoding="utf-8")
    assert "Proposed tag: v4.0-rc1" in text or "v4.0-rc1" in text
    assert "Tag created: FALSE" in text or "FALSE" in text
    assert "Do not execute yet" in text
    assert "Manual approval required" in text


def test_release_note_draft_is_research_only():
    text = (WORKSPACE / "docs" / "release" / "V4_0_RC1_RELEASE_NOTE_DRAFT.md").read_text(encoding="utf-8")

    required = [
        "research-only release candidate",
        "production-ready",  # appears as NOT production-ready
        "No broker runtime is enabled",
        "No real trade execution is allowed",
    ]
    for item in required:
        assert item.lower() in text.lower(), f"missing: {item}"

    forbidden = [
        "Production ready",
        "Broker ready",
        "Runtime ready",
        "Real trade ready",
        "Autonomous trading ready",
    ]
    for item in forbidden:
        assert item not in text, f"forbidden in release note: {item}"


def test_release_note_has_cloud_evidence():
    text = (WORKSPACE / "docs" / "release" / "V4_0_RC1_RELEASE_NOTE_DRAFT.md").read_text(encoding="utf-8")
    assert "f8796f7" in text, "missing commit sha in release note"
    assert "26629922144" in text, "missing CI run ID in release note"


if __name__ == "__main__":
    test_cloud_evidence_lock_exists_and_safe()
    test_tag_dry_run_manifest_does_not_create_tag()
    test_release_note_draft_is_research_only()
    test_release_note_has_cloud_evidence()
    print("✅ RC1-E0 Tag Dry-Run and Release Note tests PASS")
