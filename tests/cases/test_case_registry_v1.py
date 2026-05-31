#!/usr/bin/env python3
"""Case Expansion — Registry Tests V1.4.1 (hardened)"""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

CSV_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv"
JSON_PATH = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json"

def _csv(): return list(csv.DictReader(open(CSV_PATH)))
def _json(): return json.loads(open(JSON_PATH).read_text())

def test_csv_row_width(): 
    for i,l in enumerate(open(CSV_PATH).readlines()): assert len(l.strip().split(","))==14
def test_case_layer_valid():
    for c in _csv(): assert c["case_layer"] in ("CORE","EXPANSION","FAILURE")
def test_core_fields_non_empty():
    for c in _csv():
        if c["case_id"].startswith("CORE"):
            for f in ["category","industry","sector","chain","style","risk"]: assert c.get(f)
def test_all_real_trade_false():
    for c in _csv(): assert c["allowed_in_real_trade"]=="FALSE"
def test_total_ge_112(): assert len(_csv())>=112

def test_json_fields_complete():
    c=_json()[0]
    for f in ["category","industry","sector","chain","style","risk","allowed_in_research","allowed_in_paper","allowed_in_real_trade"]:
        assert f in c, f"missing {f}"
def test_json_category(): assert _json()[0]["category"]=="白马蓝筹"
def test_json_industry(): assert _json()[0]["industry"]=="食品饮料"
def test_json_style(): assert _json()[0]["style"]=="quality"
def test_json_allowed_flags():
    assert _json()[0]["allowed_in_research"] is True
    assert _json()[0]["allowed_in_paper"] is False
    assert _json()[0]["allowed_in_real_trade"] is False
def test_csv_json_count(): assert len(_csv())==len(_json())
def test_generator_exists(): assert (WORKSPACE/"scripts"/"cases"/"generate_case_registry_json.py").exists()
def test_generator_runs():
    import subprocess
    r=subprocess.run(["python3","scripts/cases/generate_case_registry_json.py"],capture_output=True,text=True,cwd=str(WORKSPACE))
    assert r.returncode==0,f"generator failed: {r.stderr}"
def test_runner_nominal(): 
    text=(WORKSPACE/"scripts"/"cases"/"run_core_12_cases.sh").read_text()
    assert "CORE_12_NOMINAL_ONLY" in text
    assert "/dev/null" not in text

if __name__=="__main__":
    import pytest; pytest.main([__file__,"-v"])
