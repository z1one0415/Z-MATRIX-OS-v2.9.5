"""Test V6-B reproducible calculation from real CSV data."""
import json, csv, io, math
from pathlib import Path
import pytest

W=Path(__file__).resolve().parent.parent.parent
PROC=W/"data/research_db/market_data"/"processed"
CASES=W/"runtime_reports"/"cases"

# Read ground-truth CSV data
@pytest.fixture(scope="module")
def csv_data():
    p={}; v={}; a={}
    for row in csv.DictReader(io.StringIO((PROC/"core12_daily_price_bar.csv").read_text())):
        t,d=row["ticker"],row["trade_date"]
        p.setdefault(t,{})[d]=float(row["close"])
        v.setdefault(t,{})[d]=float(row["volume"])
        a.setdefault(t,{})[d]=float(row["amount"])
    b={}
    for row in csv.DictReader(io.StringIO((PROC/"benchmark_csi300_price.csv").read_text())):
        b[row["trade_date"]]=float(row["close"])
    td=sorted(p.get("600519",{}).keys())
    return p,v,a,b,td

@pytest.fixture(scope="module")
def factor_json():
    d=json.loads((CASES/"v6b_price_only_factor_values.json").read_text())
    return d

@pytest.fixture(scope="module")
def leakage_json():
    return json.loads((CASES/"v6b_factor_leakage_audit.json").read_text())

@pytest.fixture(scope="module")
def closeout_json():
    return json.loads((CASES/"v6d_price_only_factor_closeout.json").read_text())

# ── Reproducible calculation tests ──

def test_script_not_empty():
    text=(W/"scripts/cases/calculate_v6b_price_only_factors.py").read_text()
    assert len(text)>500, "Script is empty or stub"
    assert "core12_daily_price_bar.csv" in text
    assert "benchmark_csi300_price.csv" in text
    assert "json.dumps" in text

def test_factor_count(factor_json):
    assert factor_json["factor_count"]==16
    assert factor_json["core_12_cases"]==12
    assert factor_json["as_of_date_count"]==57

def test_mom20_formula(csv_data, factor_json):
    p,_,_,_,td=csv_data
    records=[r for r in factor_json["records"] if r["ticker"]=="300750"]
    for rec in records:
        ad=rec["as_of_date"]
        if "MOM_20D" in rec["factor_values"]:
            i=td.index(ad)
            f=rec["factor_values"]["MOM_20D"]
            expected=p["300750"][ad]/p["300750"][td[i-20]]-1
            assert abs(f["value"]-expected)<1e-8,f"{ad}: {f['value']} vs {expected}"
            assert f["input_start_date"]==td[i-20],f"MOM_20D input_start={f['input_start_date']} should be {td[i-20]}"

def test_rev5_equals_neg_mom5(csv_data, factor_json):
    records=factor_json["records"]
    for rec in records:
        if "REV_5D" in rec["factor_values"] and "MOM_5D" in rec["factor_values"]:
            r5=rec["factor_values"]["REV_5D"]["value"]
            m5=rec["factor_values"]["MOM_5D"]["value"]
            assert abs(r5+m5)<1e-10

def test_max_drawdown_non_positive(factor_json):
    for r in factor_json["records"]:
        if "MAX_DRAWDOWN_60D" in r["factor_values"]:
            v=r["factor_values"]["MAX_DRAWDOWN_60D"]["value"]
            assert v<=0,f"DD={v} > 0"

def test_volatility_non_negative(factor_json):
    for r in factor_json["records"]:
        for fid in ["VOLATILITY_20D","VOLATILITY_60D"]:
            if fid in r["factor_values"]:
                assert r["factor_values"][fid]["value"]>=0

def test_mom_input_start_date(factor_json, csv_data):
    _p,_,_,_,td=csv_data
    for rec in factor_json["records"]:
        ad=rec["as_of_date"]
        for fid in ["MOM_1D","MOM_5D","MOM_10D","MOM_20D","MOM_60D"]:
            if fid in rec["factor_values"]:
                f=rec["factor_values"][fid]
                i=td.index(ad)
                n=int(fid.split("_")[1].replace("D",""))
                expected=td[i-n]
                assert f["input_start_date"]==expected,f"{fid}@{ad}: start={f['input_start_date']} expected={expected}"

def test_volume_input_start_correct(factor_json):
    for rec in factor_json["records"]:
        for fid in ["VOLUME_20D_AVG","VOLUME_60D_AVG","AMOUNT_20D_AVG","AMOUNT_60D_AVG"]:
            if fid in rec["factor_values"]:
                f=rec["factor_values"][fid]
                assert f["input_start_date"]<=f["input_end_date"]

# ── Leakage province tests ──
def test_leakage_safe(leakage_json):
    assert leakage_json["leakage_safe"] is True

def test_input_start_missing_zero(leakage_json):
    assert leakage_json["input_start_missing_violations"]==0

def test_window_alignment_zero(leakage_json):
    assert leakage_json["input_window_alignment_violations"]==0

# ── V7 gate provenance ──
def test_v7_blocked_if_provenance_fails(closeout_json):
    if closeout_json.get("input_window_alignment_violations",0)>0:
        assert not closeout_json["ready_for_v7_validation_entry"]

def test_closeout_has_provenance_fields(closeout_json):
    assert "input_date_violations" in closeout_json
    assert "snapshot_packet_built" in closeout_json

def test_rel_input_start_correct(factor_json, csv_data):
    p,_,_,b,td=csv_data
    for rec in factor_json["records"]:
        tk=rec["ticker"]; ad=rec["as_of_date"]
        for fid in ["TRAILING_BENCHMARK_RELATIVE_20D","TRAILING_BENCHMARK_RELATIVE_60D"]:
            if fid in rec["factor_values"]:
                f=rec["factor_values"][fid]
                i=td.index(ad)
                n=int(fid.split("_")[-1].replace("D",""))
                expected_start=td[i-n]
                assert f["input_start_date"]==expected_start,f"{fid}@{ad}: {f['input_start_date']} vs {expected_start}"
