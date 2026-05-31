#!/usr/bin/env python3
"""Case Expansion V1 Tests"""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_registry_csv_exists(): assert (WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv").exists()
def test_registry_json_exists(): assert (WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json").exists()
def test_total_cases_ge_100():
    cases = list(csv.DictReader(open(WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv")))
    assert len(cases) >= 100
def test_core_ge_12():
    cases = list(csv.DictReader(open(WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv")))
    core = [c for c in cases if c["case_layer"] == "CORE"]
    assert len(core) >= 12
def test_expansion_ge_60():
    cases = list(csv.DictReader(open(WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv")))
    exp = [c for c in cases if c["case_layer"] == "EXPANSION"]
    assert len(exp) >= 60
def test_failure_ge_40():
    cases = list(csv.DictReader(open(WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv")))
    fail = [c for c in cases if c["case_layer"] == "FAILURE"]
    assert len(fail) >= 40
def test_all_real_trade_false():
    cases = list(csv.DictReader(open(WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv")))
    for c in cases: assert c["allowed_in_real_trade"] == "FALSE"
def test_taxonomy_exists(): assert (WORKSPACE / "docs" / "cases" / "CASE_TAXONOMY_V1.md").exists()
def test_coverage_audit_exists(): assert (WORKSPACE / "runtime_reports" / "cases" / "case_coverage_audit.json").exists()
def test_closeout_exists(): assert (WORKSPACE / "docs" / "cases" / "CASE_EXPANSION_V1_CLOSEOUT.md").exists()
def test_closeout_verdict(): 
    text = (WORKSPACE / "docs" / "cases" / "CASE_EXPANSION_V1_CLOSEOUT.md").read_text()
    assert "CASE_EXPANSION_V1_PARTIAL" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
