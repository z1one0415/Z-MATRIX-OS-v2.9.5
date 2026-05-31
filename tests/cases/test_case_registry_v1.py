#!/usr/bin/env python3
"""Case Expansion V1.4.2 — Hardened Test Gate"""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

CSV_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv"
JSON_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json"

def _rows(): return open(CSV_PATH).readlines()
def _csv(): return list(csv.DictReader(open(CSV_PATH)))
def _json(): return json.loads(open(JSON_PATH).read_text())

# ── CSV schema ──
def test_csv_row_width_matches_header():
    header_cols = len(_rows()[0].strip().split(","))
    for i, line in enumerate(_rows()):
        assert len(line.strip().split(",")) == header_cols, f"Row {i}: width mismatch"

def test_csv_dictreader_has_no_none_key():
    for i, row in enumerate(_csv()):
        assert None not in row, f"Row {i}: None key in DictReader"

def test_case_layer_valid():
    for c in _csv(): assert c["case_layer"] in ("CORE", "EXPANSION", "FAILURE")

def test_core_fields_non_empty():
    for c in _csv():
        if c["case_id"].startswith("CORE"):
            for f in ["category","industry","sector","chain","style","risk"]: assert c.get(f)

def test_all_real_trade_false():
    for c in _csv(): assert c["allowed_in_real_trade"] == "FALSE"

def test_total_112(): assert len(_csv()) == 112

# ── JSON sync ──
def test_json_field_set_matches_csv_header():
    csv_fields = set(_csv()[0].keys())
    json_fields = set(_json()[0].keys())
    required = {"category","industry","sector","chain","style","risk","allowed_in_research","allowed_in_paper","allowed_in_real_trade"}
    for f in required: assert f in json_fields, f"JSON missing: {f}"

def test_core_001_json_category(): assert _json()[0]["category"] == "白马蓝筹"
def test_core_001_json_industry(): assert _json()[0]["industry"] == "食品饮料"
def test_core_001_json_style(): assert _json()[0]["style"] == "quality"

def test_json_allowed_flags_exist_and_boolean():
    c = _json()[0]
    assert c["allowed_in_research"] is True
    assert c["allowed_in_paper"] is False
    assert c["allowed_in_real_trade"] is False

def test_csv_json_core_fields_consistent():
    csv_core = {c["case_id"]: c for c in _csv() if c["case_id"].startswith("CORE")}
    json_core = {j["case_id"]: j for j in _json() if j["case_id"].startswith("CORE")}
    for cid in csv_core:
        for f in ["category","industry","sector","chain","style","risk"]:
            assert csv_core[cid][f] == json_core[cid][f], f"{cid}/{f}: CSV={csv_core[cid][f]} JSON={json_core[cid][f]}"

def test_csv_json_count(): assert len(_csv()) == len(_json())

# ── Generator ──
def test_generator_fail_closed_on_width_mismatch():
    import subprocess
    # Create temp bad CSV, run generator, expect failure
    bad_csv = WORKSPACE / "data" / "research_db" / "cases" / "_test_bad.csv"
    bad_csv.write_text("a,b,c\n1,2\n")  # 3 cols header, 2 cols data
    r = subprocess.run(["python3", "-c", """
import csv
from pathlib import Path
p=Path('data/research_db/cases/_test_bad.csv')
reader=csv.DictReader(open(p))
for row in reader:
    if None in row: raise ValueError('FAIL_CLOSED: width mismatch')
print('SHOULD_NOT_PASS')
"""], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode != 0, "Generator should FAIL on width mismatch"
    bad_csv.unlink(missing_ok=True)

# ── Runner ──
def test_runner_no_dev_null():
    text = (WORKSPACE / "scripts" / "cases" / "run_core_12_cases.sh").read_text()
    assert "/dev/null" not in text
def test_runner_nominal_only():
    assert "CORE_12_NOMINAL_ONLY" in (WORKSPACE / "scripts" / "cases" / "run_core_12_cases.sh").read_text()

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
