#!/usr/bin/env python3
"""Case Expansion — Registry Schema Tests (V1.4 hardened)"""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

CSV_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv"
JSON_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json"

def _cases(): return list(csv.DictReader(open(CSV_PATH)))
def _json(): return json.loads(open(JSON_PATH).read_text())

# ── CSV schema ──
def test_csv_row_column_count():
    for i, line in enumerate(open(CSV_PATH).readlines()):
        assert len(line.strip().split(",")) == 14, f"Row {i} width error"

def test_case_layer_valid():
    for c in _cases(): assert c["case_layer"] in ("CORE","EXPANSION","FAILURE")

def test_core_category_not_core():
    for c in _cases():
        if c["case_id"].startswith("CORE"): assert "CORE" not in c["category"], c["case_id"]

def test_core_fields_non_empty():
    for c in _cases():
        if c["case_id"].startswith("CORE"):
            for f in ["category","industry","sector","chain","style","risk"]: assert c.get(f)

def test_all_real_trade_false():
    for c in _cases(): assert c["allowed_in_real_trade"] == "FALSE"

def test_total_ge_112(): assert len(_cases()) >= 112

# ── JSON sync ──
def test_json_fields_complete():
    c0 = _json()[0]
    for f in ["category","industry","sector","chain","style","risk","allowed_in_research","allowed_in_paper","allowed_in_real_trade"]:
        assert f in c0, f"JSON missing field: {f}"

def test_core_001_json_category():
    c0 = _json()[0]; assert c0["category"] == "白马蓝筹"

def test_core_001_json_industry():
    assert _json()[0]["industry"] == "食品饮料"

def test_core_001_json_style():
    assert _json()[0]["style"] == "quality"

def test_json_allowed_in_research():
    assert _json()[0]["allowed_in_research"] is True

def test_json_allowed_in_real_trade():
    for c in _json(): assert c.get("allowed_in_real_trade", False) is False

def test_csv_json_case_count():
    assert len(_cases()) == len(_json())

# ── Runner ──
def test_runner_no_dev_null():
    text = (WORKSPACE / "scripts" / "cases" / "run_core_12_cases.sh").read_text()
    assert "/dev/null" not in text

def test_runner_nominal_only():
    text = (WORKSPACE / "scripts" / "cases" / "run_core_12_cases.sh").read_text()
    assert "CORE_12_NOMINAL_ONLY" in text

# ── Generator script ──
def test_generator_script_exists():
    assert (WORKSPACE / "scripts" / "cases" / "generate_case_registry_json.py").exists()

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
