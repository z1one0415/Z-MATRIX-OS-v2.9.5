import json, subprocess
from pathlib import Path
W = Path(__file__).resolve().parent.parent.parent
def test_normalize_yyyymmdd():
    from scripts.cases.normalize_market_data_dates import normalize
    assert normalize("20240102") == "2024-01-02"
def test_normalize_with_dash():
    assert __import__("scripts.cases.normalize_market_data_dates", fromlist=["normalize"]).normalize("2024-01-02") == "2024-01-02"
def test_invalid_raises():
    import pytest
    from scripts.cases.normalize_market_data_dates import normalize
    with pytest.raises(ValueError): normalize("abc")
def test_audit_json():
    subprocess.run(["python3", str(W/"scripts/cases/normalize_market_data_dates.py")], cwd=str(W), capture_output=True)
    d = json.loads((W/"runtime_reports/cases/v5_date_normalization_audit.json").read_text())
    assert d["normalized_format"] == "YYYY-MM-DD"
    assert d["invalid_date_count"] == 0
