#!/usr/bin/env python3
import json,hashlib;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
PATHS=["data/research_db/classification/processed","data/research_db/classification/raw","data/research_db/fundamentals/processed","data/research_db/fundamentals/raw","data/research_db/market_data/processed","data/research_db/market_data/raw","data/research_db/features/processed","data/research_db/features/raw"]
def main():
    root=C.parent.parent;raw=0;ac=0;ph=0;em=0;items=[]
    for sp in PATHS:
        dp=root/sp
        if not dp.exists():continue
        for f in dp.rglob("*"):
            if not f.is_file():
                continue
            raw+=1
            fn=f.name.lower()
            rp=str(f.relative_to(root))
            sz=f.stat().st_size
            if fn==".gitkeep":
                ph+=1
                items.append({"path":rp,"file_name":fn,"file_type":"unknown","size_bytes":0,"is_placeholder":True,"accepted_for_validation":False,"rejection_reason":"PLACEHOLDER_FILE"})
                continue
            if sz==0:
                em+=1
                continue
            sf=f.suffix.lower()
            if sf not in(".csv",".json"):
                continue
            ac+=1
            hsh=hashlib.sha256(f.read_bytes()).hexdigest()[:16]
            items.append({"path":rp,"file_name":f.name,"file_type":sf.strip("."),"size_bytes":sz,"sha256":hsh,"is_placeholder":False,"accepted_for_validation":True,"rejection_reason":None})
    result={"status":"V13_1_3_1_MOUNTED_FILE_INVENTORY_BUILT","paths_checked_count":len(PATHS),"raw_files_seen_count":raw,"accepted_for_validation_count":ac,"placeholder_file_count":ph,"empty_file_rejected_count":em,"files":items,"ready_for_source_mapping":ac>0,"feature_materialization_allowed":False,"v13_2_bucket_construction_allowed":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_1_mounted_file_inventory.json","w"),indent=2)
    print(f"Inventory: {ac} accepted, {ph} placeholder, {em} empty")
if __name__=="__main__":main()
