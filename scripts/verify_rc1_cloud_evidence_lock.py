#!/usr/bin/env python3
"""Verify RC1 Cloud Evidence Lock — all required fields present and correct."""
import json, sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
LOCK_PATH = WORKSPACE / "docs" / "rc1_audit" / "RC1_CLOUD_EVIDENCE_LOCK.json"

def verify():
    assert LOCK_PATH.exists(), f"missing: {LOCK_PATH}"
    data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    # Required identity fields
    assert data["repo_full_name"], "repo_full_name empty"
    assert "/" in data["repo_full_name"], "repo_full_name not owner/repo format"
    assert len(data["commit_sha"]) == 40, f"commit_sha not 40 chars: {len(data['commit_sha'])}"
    assert data["commit_sha"].startswith(data["short_sha"]), f"short_sha {data['short_sha']} not prefix of {data['commit_sha']}"
    assert data["commit_url"], "commit_url empty"
    assert "github.com" in data["commit_url"], "commit_url not github"

    # Required CI fields
    assert data["workflow_run_id"], "workflow_run_id empty"
    assert data["workflow_run_url"], "workflow_run_url empty"
    assert data["workflow_conclusion"] == "success", f"conclusion not success: {data['workflow_conclusion']}"

    # Required safety fields
    assert data["recommendation"] == "RC1_READY_RECOMMENDED"
    assert data["rc1_tag_created"] is False, "rc1_tag_created must be false"
    assert data["production_status"] == "BLOCKED"
    assert data["broker_runtime_status"] == "BLOCKED"
    assert data["real_trade_status"] == "BLOCKED"

    # Scorecard
    assert data["scorecard"] == "100/100"

    print("✅ RC1 cloud evidence lock PASS")
    print(f"   repo: {data['repo_full_name']}")
    print(f"   commit: {data['short_sha']}")
    print(f"   ci: run {data['workflow_run_id']} → {data['workflow_conclusion']}")

if __name__ == "__main__":
    verify()
