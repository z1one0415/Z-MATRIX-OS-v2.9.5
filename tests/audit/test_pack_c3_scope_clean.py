#!/usr/bin/env python3
"""Pack C.3.1: Scope Clean Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_scope_lock_exists():
    assert (WORKSPACE / "docs" / "audit" / "PACK_C3_SCOPE_LOCK.md").exists()

def test_no_cockpit_v2_2_in_upgrade_dir():
    """Cockpit V2.2 rename should be reverted. V2.1 restoration is OK."""
    import subprocess
    r = subprocess.run(["git", "diff", "--name-only", "2a33d35..HEAD"], capture_output=True, text=True, cwd=str(WORKSPACE))
    cockpit_v22 = [l for l in r.stdout.split("\n") if "Cockpit_V2_2" in l]
    assert not cockpit_v22, f"V2.2 still present: {cockpit_v22}"

def test_fix_plan_retained():
    assert (WORKSPACE / "docs" / "audit" / "PACK_C3_BLOCKING_RISK_FIX_PLAN.md").exists()

def test_closeout_still_not_fixed():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C3_CLOSEOUT.md").read_text()
    assert "NOT FIXED" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
