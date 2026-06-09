"""V13.GCORE.3 — Skeleton Guard as pytest."""
import subprocess, sys
from pathlib import Path

def test_no_skeleton_in_gcore():
    script = Path(__file__).resolve().parent.parent / "scripts" / "audit_no_skeleton_in_gcore.py"
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert result.returncode == 0, f"Skeleton guard failed:\n{result.stdout}\n{result.stderr}"
