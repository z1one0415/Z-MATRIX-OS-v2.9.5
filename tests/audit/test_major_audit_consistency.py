#!/usr/bin/env python3
"""Major Audit Consistency Tests — sub-audit vs closeout alignment"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_closeout_cannot_pass_if_sub_audit_blocked():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_A_CLOSEOUT.md").read_text()
    # Check freeze audit
    freeze = (WORKSPACE / "docs" / "audit" / "ARCHITECTURE_FREEZE_AUDIT_REPORT.md").read_text()
    if "BLOCKED" in freeze:
        assert "PASS" not in text or "BLOCKED" in text, "Closeout PASS but freeze BLOCKED"

def test_test_quality_subreport_matches_closeout():
    tq = (WORKSPACE / "docs" / "audit" / "TEST_QUALITY_AUDIT_REPORT.md").read_text()
    closeout = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_A_CLOSEOUT.md").read_text()
    if "REVIEW_HIGH" in tq:
        assert "REVIEW_HIGH" in closeout, "Closeout missing REVIEW_HIGH"

def test_architecture_freeze_verdict_consistent():
    freeze = (WORKSPACE / "docs" / "audit" / "ARCHITECTURE_FREEZE_AUDIT_REPORT.md").read_text()
    closeout = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_A_CLOSEOUT.md").read_text()
    freeze_verdict = "PASS" if "**PASS**" in freeze else "BLOCKED"
    assert freeze_verdict in closeout or "BLOCKED_FOR_TRIAGE" in closeout

def test_hash_fix_note_exists():
    assert (WORKSPACE / "docs" / "audit" / "GOLDEN_PATH_HASH_STABILITY_FIX_NOTE.md").exists()

def test_hash_fix_registered_in_closeout():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_A_CLOSEOUT.md").read_text()
    assert "Code Change" in text or "code-change" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])

def test_architecture_package_math_consistent():
    text = (WORKSPACE / "docs" / "audit" / "ARCHITECTURE_FREEZE_AUDIT_REPORT.md").read_text()
    # CORE + OPTIONAL + SPECIALIZED must equal classified total
    import re
    core = int(re.search(r'CORE:\s*(\d+)', text).group(1))
    opt = int(re.search(r'OPTIONAL:\s*(\d+)', text).group(1))
    spec = int(re.search(r'SPECIALIZED:\s*(\d+)', text).group(1))
    classified = int(re.search(r'Classified capability packages:\s*\*?\*?(\d+)', text).group(1))
    assert core + opt + spec == classified, f"{core}+{opt}+{spec}={core+opt+spec} != {classified}"
    # Must not contain contradictory arithmetic
    assert "20 (7 CORE + 10 OPTIONAL + 4 SPECIALIZED)" not in text, "Arithmetic contradiction found"
