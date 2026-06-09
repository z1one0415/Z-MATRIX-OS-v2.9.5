"""Test F6.2.2 ETF Exclusion Audit."""
import json
import subprocess
from pathlib import Path

def test_etf_exclusion_runs():
    r = subprocess.run(
        ["python3", "scripts/research/factors/reviews/audit_v13_f6_2_2_file_based_etf_exclusion.py"],
        capture_output=True, text=True
    )
    assert r.returncode == 0

def test_etf_exclusion_json_exists():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_file_based_etf_exclusion_audit.json")
    assert p.exists()

def test_etf_588000_excluded():
    p = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit/v13_f6_2_2_file_based_etf_exclusion_audit.json")
    data = json.loads(p.read_text())
    assert data["etf_excluded_from_fundamental"] is True
    assert "588000" in data["tickers_in_price_label"]
    assert "588000" not in data["tickers_in_fundamental"]
