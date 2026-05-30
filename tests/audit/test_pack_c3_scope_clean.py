#!/usr/bin/env python3
"""Pack C.3.1: Scope Clean Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_scope_lock_exists():
    assert (WORKSPACE / "docs" / "audit" / "PACK_C3_SCOPE_LOCK.md").exists()

def test_no_cockpit_v2_2_in_upgrade_dir():
    """Cockpit V2.1→V2.2 rename should be reverted"""
    import subprocess
    r = subprocess.run(["git", "diff", "--name-only", "c66f0bf..HEAD"], capture_output=True, text=True, cwd=str(WORKSPACE))
    cockpit_files = [l for l in r.stdout.split("\n") if "Cockpit" in l]
    # Only audit files allowed, no Cockpit renames
    assert not cockpit_files or all("audit" in f for f in cockpit_files), f"Cockpit files in diff: {cockpit_files}"

def test_fix_plan_retained():
    assert (WORKSPACE / "docs" / "audit" / "PACK_C3_BLOCKING_RISK_FIX_PLAN.md").exists()

def test_closeout_still_not_fixed():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C3_CLOSEOUT.md").read_text()
    assert "NOT FIXED" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
