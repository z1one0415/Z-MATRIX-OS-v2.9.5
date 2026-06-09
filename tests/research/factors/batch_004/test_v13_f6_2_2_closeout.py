"""Test F6.2.2 Closeout."""
import json
import subprocess
from pathlib import Path

def test_closeout_runs():
    r = subprocess.run(
        ["python3", "scripts/research/factors/reviews/build_v13_f6_2_2_csv_recovery_closeout.py"],
        capture_output=True, text=True
    )
    assert r.returncode == 0

def test_closeout_json_exists():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_csv_recovery_closeout.json")
    assert p.exists()

def test_closeout_status_complete():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_csv_recovery_closeout.json")
    data = json.loads(p.read_text())
    assert data["status"] == "COMPLETE"
    assert len(data["audits_run"]) == 5
    assert all(a["verdict"] == "PASS" for a in data["audits_run"])
