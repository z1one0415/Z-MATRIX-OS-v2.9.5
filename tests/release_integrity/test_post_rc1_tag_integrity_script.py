#!/usr/bin/env python3
"""PRI-1: Tag Integrity Script Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

TARGET = "f8796f714740b5e8c76ab53d768888a8de87dfdd"

def test_tag_integrity_script_exists():
    assert (WORKSPACE / "scripts" / "verify_post_rc1_tag_integrity.sh").exists()

def test_script_contains_tag_and_target():
    c = (WORKSPACE / "scripts" / "verify_post_rc1_tag_integrity.sh").read_text()
    assert "v4.0-rc1" in c
    assert TARGET in c
    assert "local tag" in c.lower()
    assert "remote tag" in c.lower()
    assert "target" in c.lower()

def test_local_tag_exists():
    import subprocess
    r = subprocess.run(["git", "tag", "--list", "v4.0-rc1"], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert "v4.0-rc1" in r.stdout

def test_tag_target_matches():
    import subprocess
    r = subprocess.run(["git", "rev-list", "-n", "1", "v4.0-rc1"], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.stdout.strip() == TARGET, f"tag target mismatch: {r.stdout.strip()}"

if __name__ == "__main__":
    test_tag_integrity_script_exists()
    test_script_contains_tag_and_target()
    test_local_tag_exists()
    test_tag_target_matches()
    print("✅ PRI-1 Tag Integrity tests PASS")
