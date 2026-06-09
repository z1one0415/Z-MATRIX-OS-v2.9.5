"""Test F6.2.2 Safety Audit."""
import json
import subprocess
from pathlib import Path

def test_safety_runs():
    r = subprocess.run(
        ["python3", "scripts/research/factors/reviews/audit_v13_f6_2_2_safety.py"],
        capture_output=True, text=True
    )
    assert r.returncode == 0

def test_safety_json_exists():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_safety_audit.json")
    assert p.exists()

def test_safety_zero_violations():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_safety_audit.json")
    data = json.loads(p.read_text())
    assert data["verdict"] == "PASS"
    assert data["violation_count"] == 0
