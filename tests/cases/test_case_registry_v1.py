#!/usr/bin/env python3
"""Case Expansion — Hardened Test Gate V1.4.2"""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

CSV_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv"
JSON_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json"

def _rows(): return open(CSV_PATH).readlines()
def _csv(): return list(csv.DictReader(open(CSV_PATH)))
def _json(): return json.loads(JSON_PATH.read_text())

def test_csv_row_width():
    h = len(_rows()[0].strip().split(","))
    for i, l in enumerate(_rows()): assert len(l.strip().split(",")) == h, f"Row{i} width"
def test_csv_no_none_key():
    for i, r in enumerate(_csv()): assert None not in r, f"Row{i} None key"
def test_case_layer_valid():
    for c in _csv(): assert c["case_layer"] in ("CORE","EXPANSION","FAILURE")
def test_core_fields():
    for c in _csv():
        if c["case_id"].startswith("CORE"):
            for f in ["category","industry","sector","chain","style","risk"]: assert c.get(f)
def test_rt_false(): 
    for c in _csv(): assert c["allowed_in_real_trade"] == "FALSE"
def test_total(): assert len(_csv()) == 112
def test_json_field_set():
    for f in ["category","industry","sector","chain","style","risk","allowed_in_research","allowed_in_paper","allowed_in_real_trade"]:
        assert f in _json()[0]
def test_json_category(): assert _json()[0]["category"] == "白马蓝筹"
def test_json_industry(): assert _json()[0]["industry"] == "食品饮料"
def test_json_style(): assert _json()[0]["style"] == "quality"
def test_json_flags():
    c = _json()[0]
    assert c["allowed_in_research"] is True
    assert c["allowed_in_paper"] is False
    assert c["allowed_in_real_trade"] is False
def test_csv_json_fields_match():
    csv_c = {c["case_id"]: c for c in _csv() if c["case_id"].startswith("CORE")}
    json_c = {j["case_id"]: j for j in _json() if j["case_id"].startswith("CORE")}
    for cid in csv_c:
        for f in ["category","industry","sector","chain","style","risk"]:
            assert csv_c[cid][f] == json_c[cid][f]
def test_csv_json_count(): assert len(_csv()) == len(_json())
def test_gen_fail_closed():
    import subprocess
    bad = WORKSPACE / "data" / "research_db" / "cases" / "_bad.csv"
    bad.write_text("a,b,c\n1,2\n")
    r = subprocess.run(["python3","-c","import csv; r=list(csv.DictReader(open('data/research_db/cases/_bad.csv'))); assert None not in r[0].values()"], capture_output=True, text=True, cwd=str(WORKSPACE))
    assert r.returncode != 0, "should fail on width mismatch"
    bad.unlink(missing_ok=True)
def test_runner_nominal():
    t = (WORKSPACE / "scripts" / "cases" / "run_core_12_cases.sh").read_text()
    assert "CORE_12_NOMINAL_ONLY" in t and "/dev/null" not in t

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
