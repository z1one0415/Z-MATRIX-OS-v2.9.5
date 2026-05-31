#!/usr/bin/env python3
"""Case Expansion V1.3 — Registry Schema Tests (hardened)"""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

CSV_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv"
JSON_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json"

def _cases(): return list(csv.DictReader(open(CSV_PATH)))

def test_csv_header_count_14():
    header = open(CSV_PATH).readline().strip().split(",")
    assert len(header) == 14, f"Header columns: {len(header)}"

def test_csv_all_rows_14_columns():
    for i, line in enumerate(open(CSV_PATH).readlines()):
        cols = line.strip().split(",")
        assert len(cols) == 14 or (i == 0), f"Row {i}: {len(cols)} cols"

def test_no_none_key_in_dictreader():
    for c in _cases():
        for k in c.keys():
            assert k is not None, f"None key found"

def test_case_layer_valid():
    for c in _cases():
        assert c["case_layer"] in ("CORE", "EXPANSION", "FAILURE"), f"{c['case_id']}: {c['case_layer']}"

def test_core_category_not_equals_core():
    core = [c for c in _cases() if c["case_id"].startswith("CORE")]
    for c in core:
        assert c["category"] != "CORE", f"{c['case_id']}: category={c['category']}"

def test_core_required_fields_non_empty():
    core = [c for c in _cases() if c["case_id"].startswith("CORE")]
    for c in core:
        for f in ["category","industry","sector","chain","style","risk"]:
            assert c.get(f), f"{c['case_id']}: {f} empty"

def test_allowed_in_real_trade_all_false():
    for c in _cases():
        assert c["allowed_in_real_trade"] == "FALSE", f"{c['case_id']}: {c['allowed_in_real_trade']}"

def test_allowed_in_research_valid():
    for c in _cases():
        assert c["allowed_in_research"] in ("TRUE", "FALSE"), f"{c['case_id']}: {c['allowed_in_research']}"

def test_core_risk_valid():
    core = [c for c in _cases() if c["case_id"].startswith("CORE")]
    for c in core:
        assert c["risk"] in ("low", "medium", "high"), f"{c['case_id']}: risk={c['risk']}"

def test_csv_json_consistent():
    csv_ids = {c["case_id"] for c in _cases()}
    json_data = json.loads(open(JSON_PATH).read_text())
    json_ids = {j["case_id"] for j in json_data}
    assert csv_ids == json_ids, f"CSV:{len(csv_ids)} JSON:{len(json_ids)}"

def test_total_ge_112():
    assert len(_cases()) >= 112

def test_runner_nominal_only():
    text = (WORKSPACE / "scripts" / "cases" / "run_core_12_cases.sh").read_text()
    assert "/dev/null" not in text
    assert "|| echo" not in text
    assert "CORE_12_NOMINAL_ONLY" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
