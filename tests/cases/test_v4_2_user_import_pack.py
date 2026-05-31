"""Test V4.2 User Market Data Import Pack."""
import json, subprocess
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_import_pack_doc_exists():
    assert (WORKSPACE / "docs" / "cases" / "CASE_EXPANSION_V4_2_USER_MARKET_DATA_IMPORT_PACK.md").exists()

def test_csv_file_list_exists():
    assert (WORKSPACE / "docs" / "cases" / "CORE_12_REQUIRED_CSV_FILE_LIST.md").exists()

def test_hash_guide_exists():
    assert (WORKSPACE / "docs" / "cases" / "MARKET_DATA_HASH_GUIDE.md").exists()

def test_v5_entry_criteria_exists():
    assert (WORKSPACE / "docs" / "cases" / "V5_ENTRY_CRITERIA.md").exists()

def test_hash_tool_exists():
    assert (WORKSPACE / "scripts" / "cases" / "generate_market_data_source_hash.py").exists()

def test_validator_exists():
    assert (WORKSPACE / "scripts" / "cases" / "validate_user_market_data_import_pack.py").exists()

def test_v5_gate_exists():
    assert (WORKSPACE / "scripts" / "cases" / "check_v5_entry_gate.py").exists()

def test_validator_runs():
    r = subprocess.run(["python3", "scripts/cases/validate_user_market_data_import_pack.py"],
                       capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode == 0

def test_v5_gate_runs():
    r = subprocess.run(["python3", "scripts/cases/check_v5_entry_gate.py"],
                       capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode == 0

def test_import_pack_status():
    s = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v4_2_user_import_pack_status.json").read_text())
    assert s["status"] == "CASE_EXPANSION_V4_2_USER_MARKET_DATA_IMPORT_PACK_READY"
    assert s["user_csv_required"] is True
    assert s["real_data_committed"] is False
    assert s["v5_entry_allowed"] is False
    assert s["production"] == "BLOCKED"

def test_v5_entry_gate_json():
    g = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())
    assert g["v5_entry_allowed"] is False
    assert g["production"] == "BLOCKED"
    assert g["broker_runtime"] == "BLOCKED"
    assert g["real_trade"] == "BLOCKED"

def test_v5_entry_gate_price_zero():
    g = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").read_text())
    assert g["daily_price_real_read_only"] == 0

def test_processed_gitkeep():
    gk = WORKSPACE / "data" / "research_db" / "market_data" / "processed" / ".gitkeep"
    assert gk.exists()

def test_no_real_data_committed():
    """processed/ should only have .gitkeep, no real CSV."""
    processed = WORKSPACE / "data" / "research_db" / "market_data" / "processed"
    csv_files = [f for f in processed.glob("*.csv") if not f.name.startswith("_test")]
    assert len(csv_files) == 0, f"Real CSV found in processed/: {csv_files}"
