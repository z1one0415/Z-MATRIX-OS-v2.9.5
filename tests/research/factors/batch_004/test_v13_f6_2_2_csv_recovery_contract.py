"""Test F6.2.2 CSV Recovery Contract builder."""
import json
import subprocess
from pathlib import Path

def test_contract_builder_runs():
    r = subprocess.run(
        ["python3", "scripts/research/factors/reviews/build_v13_f6_2_2_csv_recovery_contract.py"],
        capture_output=True, text=True
    )
    assert r.returncode == 0

def test_contract_json_exists():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_csv_recovery_contract.json")
    assert p.exists()

def test_contract_has_base_commit():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_csv_recovery_contract.json")
    data = json.loads(p.read_text())
    assert data["base_commit"] == "3979f1d"
    assert data["total_rows"] == 28
    assert len(data["factors"]) == 7
    assert "F6_2_CSV_MATERIALIZATION_FILES_MISSING_FROM_WORKTREE" in data["problem"]
