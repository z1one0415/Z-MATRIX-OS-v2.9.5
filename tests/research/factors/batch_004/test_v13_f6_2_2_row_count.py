"""Test F6.2.2 Row Count and Coverage Audit."""
import json
import subprocess
from pathlib import Path

def test_row_count_runs():
    r = subprocess.run(
        ["python3", "scripts/research/factors/reviews/audit_v13_f6_2_2_file_based_row_count_and_coverage.py"],
        capture_output=True, text=True
    )
    assert r.returncode == 0

def test_row_count_json_exists():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_file_based_row_count_and_coverage_audit.json")
    assert p.exists()

def test_28_rows_7_factors_4_tickers():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_file_based_row_count_and_coverage_audit.json")
    data = json.loads(p.read_text())
    assert data["total_rows"] == 28
    assert data["row_count_match"] is True
    assert data["factors_match"] is True
    assert data["tickers_match"] is True
    assert data["etf_588000_correctly_absent"] is True
    assert data["all_rebalance_date_2026_05_06"] is True
    assert data["all_signal_role_factors_only"] is True
