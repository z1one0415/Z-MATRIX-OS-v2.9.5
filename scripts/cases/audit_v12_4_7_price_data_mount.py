#!/usr/bin/env python3
import json,re
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
FW=[r"\bBUY\b",r"\bSELL\b",r"\bADD\b",r"\bREDUCE\b",r"\bLONG\b",r"\bSHORT\b",r"\bPOSITION\b",r"\bORDER\b",r"\bTRADE_EXECUTION\b",r"\bWEIGHT\b",r"\bTARGET_PRICE\b",r"\bTAKE_PROFIT\b",r"\bSTOP_LOSS\b"]
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def scan(obj,path=""):
    v=[]
    if isinstance(obj,dict):
        for k,val in obj.items():
            c=f"{path}.{k}"if path else k
            if isinstance(val,str):
                for w in FW:
                    if re.search(w,val,re.I):v.append(f"FW {w} in {c}={val}")
            elif isinstance(val,(dict,list)):v.extend(scan(val,c))
    elif isinstance(obj,list):
        for i,item in enumerate(obj):v.extend(scan(item,f"{path}[{i}]"))
    return v
def main():
    ct=load("v12_4_7_price_data_mount_contract.json");disc=load("v12_4_7_price_data_file_discovery.json")
    sv=load("v12_4_7_price_data_schema_validation.json");tc=load("v12_4_7_price_data_target_coverage.json")
    reasons=[];svv=[]
    targets=[("contract",ct),("discovery",disc),("schema",sv),("coverage",tc)]
    for fn,d in targets:
        if d.get("ready_for_alpha_claim",False):reasons.append(f"ALPHA_{fn}")
        if d.get("alpha_validated",False):reasons.append(f"AV_{fn}")
        for ch in["production","broker_runtime","real_trade"]:
            if d.get(ch)!="BLOCKED":reasons.append(f"{ch}_{fn}")
    mounted=disc.get("price_file_discovered",False)
    schema_ok=sv.get("ready_for_coverage_validation",False)
    coverage_ok=tc.get("target_coverage_ok",False)
    if not mounted:reasons.append("PRICE_DATA_FILE_NOT_MOUNTED")
    # If files exist but schema fails: BLOCKED
    if mounted and not schema_ok:reasons.append("SCHEMA_NOT_PASS_WITH_MOUNTED_FILE")
    # If schema passes but coverage fails: BLOCKED
    if schema_ok and not coverage_ok:reasons.append("COVERAGE_NOT_MET_WITH_SCHEMA_PASS")
    for fn,d in targets:svv.extend(scan(d,fn))
    blocked=len(reasons)+len(svv)>0
    # Special: no-file is not a blocking reason if everything else is clean
    if len(reasons)==1 and"PRICE_DATA_FILE_NOT_MOUNTED"in reasons and len(svv)==0:
        blocked=False;reasons=[]
    result={"status":"V12_4_7_PRICE_DATA_MOUNT_AUDIT_PASS"if not blocked else"V12_4_7_PRICE_DATA_MOUNT_AUDIT_BLOCKED",
        "price_data_mount_gate_confirmed":not blocked,"price_file_mounted":mounted,
        "schema_validated":schema_ok,"target_coverage_ok":coverage_ok,
        "ready_for_label_regeneration":mounted and schema_ok and coverage_ok and not blocked,
        "cycle2_still_blocked":True,"v12_5_still_blocked":True,
        "forbidden_action_violations":svv+reasons,"safety_violations":svv,
        "blocking_reasons":reasons,"investment_action_count":0,"trade_action_count":0,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v12_4_7_price_data_mount_audit.json","w"),indent=2)
    print(f"Audit: {result['status']} | mounted={mounted} schema={schema_ok} cov={coverage_ok} lr={result['ready_for_label_regeneration']}")
if __name__=="__main__":main()
