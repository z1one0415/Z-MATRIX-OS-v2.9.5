#!/usr/bin/env python3
import json,csv,io;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def read_csv_headers(fp):
    try:rows=list(csv.DictReader(io.StringIO(fp.read_text())));return list(rows[0].keys())if rows else[],len(rows)
    except:return[],0
SECTOR_REQ=["ticker","as_of_date","sector","industry"];FUND_REQ=["ticker","as_of_date","fundamental_proxy_score"]
PRICE_REQ=["ticker","trade_date","close","adjusted_close","volume"];TURNOVER_REQ=["ticker","trade_date","turnover"];TURNOVER_ALT=["ticker","trade_date","volume","float_shares"]
def main():
    disc=load("v13_1_2_feature_source_discovery.json");spec=load("v13_1_2_feature_schema_spec.json")
    root=C.parent.parent;items=[];pass_c=0;no_src=0
    for s in spec.get("schemas",[]):
        fg=s["feature_group"]
        matched=[src for src in disc.get("sources",[])if fg.replace("_or_","")in src.get("source_path","").lower()or(fg=="turnover"and("turnover"in src.get("source_path","").lower()or"volume"in src.get("source_path","").lower()))or(fg=="drawdown_or_recovery"and("price"in src.get("source_path","").lower()or"daily"in src.get("source_path","").lower()or"bar"in src.get("source_path","").lower()))]
        if not matched:no_src+=1;items.append({"feature_group":fg,"source_found":False,"schema_validation_status":"NO_SOURCE","blocking_reasons":["NO_ACCEPTED_FEATURE_SOURCE"]});continue
        src=matched[0];fp=root/src["source_path"]
        if fg=="sector_or_industry":cols,n=read_csv_headers(fp);ok=all(f in cols for f in SECTOR_REQ)if cols else False
        elif fg=="fundamental_proxy_field":cols,n=read_csv_headers(fp);ok=all(f in cols for f in FUND_REQ)if cols else False
        elif fg=="drawdown_or_recovery":cols,n=read_csv_headers(fp);ok=all(f in cols for f in PRICE_REQ)if cols else False
        elif fg=="turnover":cols,n=read_csv_headers(fp);ok=(all(f in cols for f in TURNOVER_REQ)or all(f in cols for f in TURNOVER_ALT))if cols else False
        else:ok=False
        status="SCHEMA_PASS"if ok else"SCHEMA_BLOCKED";pass_c+=1 if ok else 0
        items.append({"feature_group":fg,"source_path":src.get("source_path"),"source_found":True,"schema_validation_status":status,"blocking_reasons":[]if ok else["MISSING_REQUIRED_COLUMNS"]})
    result={"status":"V13_1_2_FEATURE_SOURCE_SCHEMA_VALIDATION_BUILT","feature_group_count":len(items),"schema_pass_group_count":pass_c,"schema_blocked_group_count":len(items)-pass_c-no_src,"no_source_group_count":no_src,"validations":items,"ready_for_feature_derivation_plan":True,"ready_for_v13_2_bucket_construction_next_stage":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_2_feature_source_schema_validation.json","w"),indent=2)
    print(f"SchemaVal: {pass_c} pass, {len(items)-pass_c-no_src} blocked, {no_src} nosource")
if __name__=="__main__":main()
