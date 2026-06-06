#!/usr/bin/env python3
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v12_4_7_price_data_mount_contract.json")
    base_dir=C.parent.parent/"data"/"research_db"/"market_data"/"processed"
    candidates=[];found=0;readable=0
    for cf in ct.get("candidate_files",[]):
        fp=base_dir/Path(cf).name
        ex=fp.exists();fnd=0;rd=0;ds="NOT_FOUND";br=["FILE_NOT_FOUND"]
        if ex:
            sz=fp.stat().st_size;fnd=1
            try:
                fp.read_text();rd=1;readable+=1;ds="FOUND";br=[]
            except:ds="UNREADABLE";br=["FILE_UNREADABLE"]
        found+=fnd
        candidates.append({"candidate_file":cf,"exists":ex,"size_bytes":sz if ex else 0,
            "readable":rd>0,"file_type":"csv","discovery_status":ds,"blocking_reasons":br})
    any_found=found>0
    result={"status":"V12_4_7_PRICE_DATA_FILE_DISCOVERY_BUILT",
        "candidates_checked":len(candidates),"candidates_found":found,"candidates_readable":readable,
        "price_file_discovered":readable>0,"ready_for_schema_validation":readable>0,
        "candidates":candidates,"blocking_reasons":[]if readable else["PRICE_DATA_FILE_NOT_MOUNTED"],
        "ready_for_label_regeneration":False,"ready_for_cycle2_recalculation":False,
        "ready_for_v12_5_feedback":False,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v12_4_7_price_data_file_discovery.json","w"),indent=2)
    print(f"Discovery: {len(candidates)} chk | found={found} readable={readable}")
if __name__=="__main__":main()
