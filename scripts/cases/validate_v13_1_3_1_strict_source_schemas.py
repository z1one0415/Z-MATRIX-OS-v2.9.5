#!/usr/bin/env python3
import json,hashlib;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
import csv,io
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
RQ={"sector_or_industry":["ticker","as_of_date","sector","industry"],"fundamental_proxy_field":["ticker","as_of_date","fundamental_proxy_score"],"price_bar_input":["ticker","trade_date","close","adjusted_close","volume"],"turnover":[["ticker","trade_date","turnover"],["ticker","trade_date","volume","float_shares"]],"rank_short_medium":[["ticker","as_of_date","short_rank_input","medium_rank_input"],["ticker","as_of_date","short_rank","medium_rank","rank_acceleration"]]}
def main():
    mp=load("v13_1_3_1_feature_source_mapping.json");pkg=load("v13_1_3_mount_requirement_package.json");root=C.parent.parent;items=[];pc=0;bc=0;ns=0
    for g in ["sector_or_industry","fundamental_proxy_field","price_bar_input","turnover","rank_short_medium"]:
        ss=mp.get("mappings",{}).get(g,[]);rq=RQ[g]
        if not ss:ns+=1;items.append({"feature_group":g,"schema_status":"NO_SOURCE","missing_columns":rq if isinstance(rq,list)else rq[0]});continue
        fp=root/ss[0]["path"]
        try:
            rd=list(csv.DictReader(io.StringIO(fp.read_text())));cols=list(rd[0].keys())if rd else[];n=len(rd)
            if isinstance(rq[0],list):ok=any(all(c in cols for c in req)for req in rq)
            else:ok=all(c in cols for c in rq)
            miss=[c for c in(rq[0]if isinstance(rq[0],list)else rq)if c not in cols]
        except:ok=False;cols=[];n=0;miss=rq if isinstance(rq,list)else rq[0]
        if ok:pc+=1;st="SCHEMA_PASS"
        else:bc+=1;st="SCHEMA_BLOCKED"
        items.append({"feature_group":g,"selected_source_path":str(ss[0]["path"]),"source_found":True,"schema_status":st,"required_columns":rq,"present_columns":cols,"missing_columns":miss,"row_count":n,"blocking_reasons":[]if ok else["MISSING_COLUMNS"]})
    result={"status":"V13_1_3_1_STRICT_SOURCE_SCHEMA_VALIDATION_BUILT","feature_group_count":5,"schema_pass_group_count":pc,"schema_blocked_group_count":bc,"no_source_group_count":ns,"validations":items,"ready_for_coverage_validation":pc>0,"feature_materialization_allowed":False,"v13_2_bucket_construction_allowed":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_1_strict_source_schema_validation.json","w"),indent=2)
    print(f"Schema: {pc}p/{bc}b/{ns}ns")
if __name__=="__main__":main()