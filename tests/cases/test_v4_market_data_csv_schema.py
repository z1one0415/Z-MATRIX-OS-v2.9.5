"""Test V4 CSV schema validator."""
import json, subprocess
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent
SCRIPT = WORKSPACE / "scripts" / "cases" / "validate_market_data_csv_schema.py"

def test_validator_runs_without_data():
    """Should succeed when no CSV files exist (graceful no-op)."""
    r = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode == 0, r.stderr

def test_validator_rejects_synthetic():
    """Validator must reject source_type=SYNTHETIC."""
    import csv, io
    processed = WORKSPACE / "data" / "research_db" / "market_data" / "processed"
    bad_csv = processed / "_test_bad.csv"
    fieldnames = ["ticker","trade_date","open","high","low","close","volume","amount","source_name","source_type","source_file","source_hash","as_of_date","adjusted"]
    writer = csv.DictWriter(io.StringIO(), fieldnames=fieldnames)
    # Create a temp file with SYNTHETIC type
    content = "ticker,trade_date,open,high,low,close,volume,amount,source_name,source_type,source_file,source_hash,as_of_date,adjusted\n"
    content += "600519,2024-01-02,1690,1715,1685,1700,2345678,3987654321,test,SYNTHETIC,test.csv,<sha256>,2026-05-31,true\n"
    bad_csv.write_text(content)
    r = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True, cwd=str(WORKSPACE))
    bad_csv.unlink()  # clean up
    assert r.returncode != 0, "Should reject SYNTHETIC source_type"

def test_validator_rejects_no_hash():
    """Validator must reject missing source_hash."""
    processed = WORKSPACE / "data" / "research_db" / "market_data" / "processed"
    bad_csv = processed / "_test_nohash.csv"
    content = "ticker,trade_date,open,high,low,close,volume,amount,source_name,source_type,source_file,source_hash,as_of_date,adjusted\n"
    content += "600519,2024-01-02,1690,1715,1685,1700,2345678,3987654321,test,LOCAL_USER_PROVIDED,test.csv,,2026-05-31,true\n"
    bad_csv.write_text(content)
    r = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True, cwd=str(WORKSPACE))
    bad_csv.unlink()
    assert r.returncode != 0, "Should reject empty source_hash"

def test_processed_cleanup():
    """Ensure no test files left in processed/."""
    processed = WORKSPACE / "data" / "research_db" / "market_data" / "processed"
    test_files = [f for f in processed.glob("_test*")]
    for f in test_files: f.unlink()
    assert len([f for f in processed.glob("_test*")]) == 0
