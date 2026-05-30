#!/usr/bin/env python3
"""Major Audit Phase Closeout Freeze Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_closeout_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PHASE_CLOSEOUT.md").exists()
def test_final_verdict_md_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_FINAL_VERDICT.md").exists()
def test_freeze_manifest_exists(): assert (WORKSPACE / "docs" / "audit" / "RESEARCH_OS_V3_AUDIT_FREEZE_MANIFEST.md").exists()
def test_verify_script_exists(): assert (WORKSPACE / "scripts" / "audit" / "verify_major_audit_phase_closeout.sh").exists()

def test_status_is_frozen():
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    assert v["status"] == "RESEARCH_OS_V3_MAJOR_AUDIT_PHASE_FROZEN"
    assert v["p0"] == 0
    assert v["p1_blocking"] == 0
    assert v["core_modules_reaudited"] == 7

def test_all_blocked():
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    for key in ["production", "broker_runtime", "real_trade"]:
        assert v[key] == "BLOCKED"

def test_no_production_claims():
    combined = "\n".join([
        (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PHASE_CLOSEOUT.md").read_text(),
        (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_FINAL_VERDICT.md").read_text(),
        (WORKSPACE / "docs" / "audit" / "RESEARCH_OS_V3_AUDIT_FREEZE_MANIFEST.md").read_text(),
    ])
    for fb in ["Production Ready", "Broker Ready", "Runtime Ready", "Real Trade Ready"]:
        assert fb not in combined

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])

def test_verdict_json_exists(): assert (WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").exists()

def test_verdict_freeze_commit_matches_head():
    import subprocess, json
    head = subprocess.run(["git","rev-parse","--short","HEAD"], capture_output=True, text=True, cwd=str(WORKSPACE)).stdout.strip()
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    assert v["freeze_commit"] == head, f"JSON freeze_commit {v['freeze_commit']} != HEAD {head}"

def test_verdict_c5_1_commit(): 
    import json
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    assert v["c5_1_commit"] == "496330f"

def test_manifest_freeze_commit_matches_json():
    import json
    manifest = (WORKSPACE / "docs" / "audit" / "RESEARCH_OS_V3_AUDIT_FREEZE_MANIFEST.md").read_text()
    v = json.loads((WORKSPACE / "runtime_reports" / "audit" / "major_audit_final_verdict.json").read_text())
    fc = v["freeze_commit"]
    assert fc in manifest, f"Manifest missing freeze_commit {fc}"
