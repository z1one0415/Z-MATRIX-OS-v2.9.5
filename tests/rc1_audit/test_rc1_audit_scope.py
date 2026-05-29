#!/usr/bin/env python3
"""RA-0: Audit Scope + Baseline Manifest Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_scope_lock_exists():
    p = WORKSPACE / "docs" / "rc1_audit" / "RC1_AUDIT_SCOPE_LOCK.md"
    assert p.exists()
    content = p.read_text()
    assert "RA-0" in content
    assert "RA-8" in content
    assert "READ_ONLY" in content
    assert "FALSE" in content or "false" in content.lower()

def test_baseline_manifest():
    p = WORKSPACE / "docs" / "rc1_audit" / "RC1_BASELINE_MANIFEST.json"
    assert p.exists()
    m = json.loads(p.read_text())
    assert m["baseline_commit"] == "0ccf235"
    assert m["rc1_status"] == "NOT_APPROVED"
    assert m["production_status"] == "BLOCKED"
    assert m["audit_mode"] == "READ_ONLY"
    assert m["rc1_tag_allowed"] == False

def test_acceptance_matrix():
    p = WORKSPACE / "docs" / "rc1_audit" / "RC1_AUDIT_ACCEPTANCE_MATRIX.md"
    assert p.exists()
    content = p.read_text()
    for phase in ["RA-0","RA-1","RA-2","RA-3","RA-4","RA-5","RA-6","RA-7","RA-8"]:
        assert phase in content, f"missing {phase}"

def test_verify_script_exists():
    p = WORKSPACE / "scripts" / "verify_rc1_audit_scope.sh"
    assert p.exists()

if __name__ == "__main__":
    test_scope_lock_exists()
    test_baseline_manifest()
    test_acceptance_matrix()
    test_verify_script_exists()
    print("✅ RA-0 Audit Scope tests PASS")
