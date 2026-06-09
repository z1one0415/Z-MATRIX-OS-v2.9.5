"""Test F6.2.2 F13 Non-Informative Audit."""
import json
import subprocess
from pathlib import Path

def test_f13_audit_runs():
    r = subprocess.run(
        ["python3", "scripts/research/factors/reviews/audit_v13_f6_2_2_file_based_f13_non_informative.py"],
        capture_output=True, text=True
    )
    assert r.returncode == 0

def test_f13_json_exists():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_file_based_f13_non_informative_audit.json")
    assert p.exists()

def test_f13_all_scores_zero():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_file_based_f13_non_informative_audit.json")
    data = json.loads(p.read_text())
    assert data["all_scores_zero"] is True
    assert data["num_rows"] == 4
    assert data["num_distinct_tickers"] == 4
    assert data["classification"] == "MATERIALIZED_NON_INFORMATIVE"
