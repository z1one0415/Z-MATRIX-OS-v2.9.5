"""Test F6.2.2 No Hardcoded Ground Truth Audit."""
import json
import subprocess
from pathlib import Path

def test_no_hardcoded_runs():
    r = subprocess.run(
        ["python3", "scripts/research/factors/reviews/audit_v13_f6_2_2_no_hardcoded_ground_truth.py"],
        capture_output=True, text=True
    )
    assert r.returncode == 0

def test_no_hardcoded_json_exists():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_no_hardcoded_ground_truth_audit.json")
    assert p.exists()

def test_scripts_scanned():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_no_hardcoded_ground_truth_audit.json")
    data = json.loads(p.read_text())
    assert len(data["scripts_scanned"]) > 0
    # F6.2.2 scripts were scanned
    f622_scripts = [s for s in data["scripts_scanned"] if "f6_2_2" in s]
    assert len(f622_scripts) >= 5
