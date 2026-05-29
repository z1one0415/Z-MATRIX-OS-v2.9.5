#!/usr/bin/env python3
"""V4.0-RC1: GitHub Release Draft Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_release_draft_exists():
    assert (WORKSPACE / "docs" / "release" / "V4_0_RC1_GITHUB_RELEASE_DRAFT.md").exists()

def test_release_draft_is_research_only():
    text = (WORKSPACE / "docs" / "release" / "V4_0_RC1_GITHUB_RELEASE_DRAFT.md").read_text()
    assert "Research-only Release Candidate" in text
    assert "not production-ready" in text
    assert "does not enable broker runtime" in text
    assert "does not allow real trade execution" in text

def test_release_draft_has_safety_gates():
    text = (WORKSPACE / "docs" / "release" / "V4_0_RC1_GITHUB_RELEASE_DRAFT.md").read_text()
    assert "Production: BLOCKED" in text
    assert "Broker/runtime: BLOCKED" in text
    assert "Real trade: BLOCKED" in text
    assert "Paper-only: TRUE" in text
    assert "Human review required: TRUE" in text

def test_release_draft_has_target_evidence():
    text = (WORKSPACE / "docs" / "release" / "V4_0_RC1_GITHUB_RELEASE_DRAFT.md").read_text()
    assert "v4.0-rc1" in text
    assert "f8796f714740b5e8c76ab53d768888a8de87dfdd" in text
    assert "26629922144" in text
    assert "POST_RC1_INTEGRITY_PASS" in text

def test_release_draft_no_production_claims():
    text = (WORKSPACE / "docs" / "release" / "V4_0_RC1_GITHUB_RELEASE_DRAFT.md").read_text()
    for f in ["Production: READY","Broker/runtime: READY","Real trade: READY","Autonomous trading ready","production_allowed=True","broker_order_allowed=True","real_trade_allowed=True","runtime_enabled=True"]:
        assert f not in text

if __name__ == "__main__":
    test_release_draft_exists()
    test_release_draft_is_research_only()
    test_release_draft_has_safety_gates()
    test_release_draft_has_target_evidence()
    test_release_draft_no_production_claims()
    print("✅ V4.0-RC1 GitHub Release Draft tests PASS")
