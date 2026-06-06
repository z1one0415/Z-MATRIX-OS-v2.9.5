#!/usr/bin/env python3
import json,csv,io
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    sv=load("v12_4_7_price_data_schema_validation.json");ct=load("v12_4_7_price_data_mount_contract.json")
    base_dir=C.parent.parent/"data"/"research_db"/"market_data"/"processed"
    items=[];passed=0;blocked=0
    for v in sv.get("validations",[]):
        fp=base_dir/Path(v["candidate_file"]).name
        c={"candidate_file":v["candidate_file"],"coverage_validation_status":"COVERAGE_BLOCKED",
           "target_ticker":"600837","target_as_of_date":"20240909",
           "ticker_rows":0,"has_target_as_of_date":False,
           "target_window_start":"20240909","target_window_end_min":"20241201",
           "target_window_end_max":"20241231","has_exit_window_data":False,
           "available_trade_date_count_after_as_of":0,"earliest_available_date":"","latest_available_date":"",
           "blocking_reasons":[]}
        if v["schema_validation_status"]!="SCHEMA_PASS":c["blocking_reasons"].append("SCHEMA_NOT_PASS");items.append(c);blocked+=1;continue
        if not fp.exists():c["blocking_reasons"].append("FILE_NOT_FOUND");items.append(c);blocked+=1;continue
        rows=list(csv.DictReader(io.StringIO(fp.read_text())))
        tr=[r for r in rows if r.get("ticker","")=="600837"]
        c["ticker_rows"]=len(tr)
        if not tr:c["blocking_reasons"].append("TICKER_600837_NOT_IN_FILE");items.append(c);blocked+=1;continue
        dates=sorted(set(r.get("trade_date","")for r in tr))
        if len(dates)>0:c["earliest_available_date"]=dates[0];c["latest_available_date"]=dates[-1]
        if "20240909"in dates:c["has_target_as_of_date"]=True
        else:c["blocking_reasons"].append("TARGET_DATE_20240909_MISSING")
        after=[d for d in dates if d>"20240909"]
        c["available_trade_date_count_after_as_of"]=len(after)
        if after and after[-1]>="20241201":c["has_exit_window_data"]=True
        else:c["blocking_reasons"].append("EXIT_WINDOW_NOT_COVERED")
        if not c["blocking_reasons"]:c["coverage_validation_status"]="COVERAGE_PASS";passed+=1
        else:blocked+=1
        items.append(c)
    ok=passed>0 and blocked==0
    selected=items[0]["candidate_file"]if ok else None
    result={"status":"V12_4_7_PRICE_DATA_TARGET_COVERAGE_BUILT",
        "coverage_pass_file_count":passed,"coverage_blocked_file_count":blocked,
        "target_coverage_ok":ok,"selected_price_file":selected,
        "ready_for_label_regeneration":ok,"ready_for_cycle2_recalculation":False,
        "ready_for_v12_5_feedback":False,"validations":items,
        "blocking_reasons":[]if ok else["TARGET_COVERAGE_NOT_MET"],
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v12_4_7_price_data_target_coverage.json","w"),indent=2)
    print(f"Coverage: {passed}p/{blocked}b")
if __name__=="__main__":main()
