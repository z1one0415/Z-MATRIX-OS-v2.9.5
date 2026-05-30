#!/usr/bin/env python3
"""Major Audit Phase Closeout Freeze Tests — no self-referential commit hash"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_closeout_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PHASE_CLOSEOUT.md").exists()
def test_verdict_json_exists(): assert (WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").exists()

def test_freeze_subject_commit_is_3374fb2():
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    assert v["freeze_subject_commit"] == "3374fb2"

def test_c5_1_commit_is_496330f():
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    assert v["c5_1_commit"] == "496330f"

def test_no_self_referential_commit_hash():
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    assert v["evidence_lock_commit_policy"] == "recorded_by_git_history_not_self_referenced"

def test_status_is_frozen():
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    assert v["status"] == "RESEARCH_OS_V3_MAJOR_AUDIT_PHASE_FROZEN"
    assert v["p0"] == 0
    assert v["p1_blocking"] == 0

def test_all_blocked():
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    for key in ["production", "broker_runtime", "real_trade"]:
        assert v[key] == "BLOCKED"

def test_manifest_matches_json():
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    manifest = (WORKSPACE / "docs" / "audit" / "RESEARCH_OS_V3_AUDIT_FREEZE_MANIFEST.md").read_text()
    assert v["freeze_subject_commit"] in manifest
    assert "no self-referential" in manifest

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
