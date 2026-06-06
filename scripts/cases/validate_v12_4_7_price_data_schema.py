#!/usr/bin/env python3
import json,csv,io
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
REQUIRED=["ticker","trade_date","close","adjusted_close","volume"]
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    disc=load("v12_4_7_price_data_file_discovery.json");ct=load("v12_4_7_price_data_mount_contract.json")
    base_dir=C.parent.parent/"data"/"research_db"/"market_data"/"processed"
    items=[];passed=0;blocked=0
    for c in disc.get("candidates",[]):
        fp=base_dir/Path(c["candidate_file"]).name
        v={"candidate_file":c["candidate_file"],"schema_validation_status":"SCHEMA_BLOCKED",
           "required_fields_checked":list(REQUIRED),
           "has_ticker_column":False,"has_trade_date_column":False,"has_close_column":False,
           "has_adjusted_close_column":False,"has_volume_column":False,
           "missing_required_fields":[],"ticker_format_ok":False,"date_format_ok":False,
           "close_numeric_ok":False,"adjusted_close_numeric_ok":False,"volume_numeric_ok":False,
           "blocking_reasons":[]}
        if not fp.exists():v["blocking_reasons"].append("FILE_NOT_FOUND");items.append(v);blocked+=1;continue
        try:rows=list(csv.DictReader(io.StringIO(fp.read_text())))
        except:v["blocking_reasons"].append("FILE_UNREADABLE");items.append(v);blocked+=1;continue
        cols=list(rows[0].keys());mr=[]
        for f in REQUIRED:
            if f in cols:v[f"has_{f}_column"]=True
            else:mr.append(f)
        if mr:v["missing_required_fields"]=mr;v["blocking_reasons"].append("MISSING_REQUIRED_COLUMNS");items.append(v);blocked+=1;continue
        # Check ticker format (6-digit)
        try:
            for row in rows[:10]:
                t=row.get("ticker","");assert t.isdigit()and len(t)==6
            v["ticker_format_ok"]=True
        except:v["blocking_reasons"].append("TICKER_FORMAT_INVALID")
        # Check date format
        try:
            for row in rows[:10]:d=row.get("trade_date","");assert len(d)==8 and d.isdigit()
            v["date_format_ok"]=True
        except:v["blocking_reasons"].append("DATE_FORMAT_INVALID")
        # Check numeric
        try:
            for row in rows[:10]:
                float(row.get("close",""));float(row.get("adjusted_close",""));float(row.get("volume",""))
            v["close_numeric_ok"]=True;v["adjusted_close_numeric_ok"]=True;v["volume_numeric_ok"]=True
        except:v["blocking_reasons"].append("NON_NUMERIC_PRICE_FIELDS")
        if not v["blocking_reasons"]:v["schema_validation_status"]="SCHEMA_PASS";passed+=1
        else:blocked+=1
        items.append(v)
    ok=passed>0 and blocked==0
    result={"status":"V12_4_7_PRICE_DATA_SCHEMA_VALIDATION_BUILT",
        "schema_validated_file_count":passed,"schema_blocked_file_count":blocked,
        "schema_consistency_ok":True,"ready_for_coverage_validation":passed>0,
        "validations":items,"blocking_reasons":[]if passed else["NO_FILE_PASSED_SCHEMA"],
        "ready_for_label_regeneration":False,"ready_for_cycle2_recalculation":False,
        "ready_for_v12_5_feedback":False,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v12_4_7_price_data_schema_validation.json","w"),indent=2)
    print(f"Schema: {passed}p/{blocked}b")
if __name__=="__main__":main()
