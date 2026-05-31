"""Test V4 market data contract."""
import json
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_contract_exists():
    assert (WORKSPACE / "runtime_reports" / "cases" / "v4_market_data_contract.json").exists()

def test_contract_enum():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v4_market_data_contract.json").read_text())
    assert "REAL_READ_ONLY" in c["source_status_enum"]
    assert "SYNTHETIC" in c["source_status_enum"]
    assert "MISSING" in c["source_status_enum"]

def test_contract_hard_rules():
    c = json.loads((WORKSPACE / "runtime_reports" / "cases" / "v4_market_data_contract.json").read_text())
    rules = c["hard_rules"]
    assert any("source_hash" in r for r in rules)
    assert any("not be default-filled" in r for r in rules)
    assert any("SYNTHETIC" in r for r in rules)

def test_templates_exist():
    tmpl = WORKSPACE / "data" / "research_db" / "market_data" / "templates"
    assert len(list(tmpl.glob("*.csv"))) == 4

def test_raw_staging_vendor_empty():
    """raw/staging/vendor must not contain real data (only .gitkeep)."""
    for dname in ["raw", "staging", "vendor"]:
        d = WORKSPACE / "data" / "research_db" / "market_data" / dname
        files = [f for f in d.glob("*") if f.name != ".gitkeep"]
        assert len(files) == 0, f"{dname} contains data: {files}"

def test_contract_doc_exists():
    assert (WORKSPACE / "docs" / "cases" / "CASE_EXPANSION_V4_MARKET_DATA_CONTRACT.md").exists()
