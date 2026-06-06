#!/usr/bin/env python3
import json,hashlib;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    inv=load("v13_1_3_1_mounted_file_inventory.json");pkg=load("v13_1_3_mount_requirement_package.json")
    gm={'sector': 'sector_or_industry', 'industry': 'sector_or_industry', 'classification': 'sector_or_industry', 'fundamental': 'fundamental_proxy_field', 'quality': 'fundamental_proxy_field', 'price': 'price_bar_input', 'daily': 'price_bar_input', 'bar': 'price_bar_input', 'turnover': 'turnover', 'volume': 'turnover', 'float': 'turnover', 'rank': 'rank_short_medium'};items={g:[] for g in set(gm.values())}
    for f in inv.get("files",[]):
        if not f.get("accepted_for_validation"):continue
        fn=f["file_name"].lower();fg="unknown"
        for k in gm:
            if k in fn:fg=gm[k];break
        if fg!="unknown":items[fg].append({"path":f["path"],"sha256":f.get("sha256",""),"mapping_confidence":"HIGH","mapping_reason":"filename"})
    mapped=sum(1 for g,ss in items.items() if ss);nosrc=sum(1 for g,ss in items.items() if not ss)
    result={"status":"V13_1_3_1_FEATURE_SOURCE_MAPPING_BUILT","feature_group_count":5,"mapped_group_count":mapped,"no_source_group_count":nosrc,"ambiguous_group_count":0,"mappings":{k:v for k,v in items.items()},"ready_for_strict_schema_validation":mapped>0,"feature_materialization_allowed":False,"v13_2_bucket_construction_allowed":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_1_feature_source_mapping.json","w"),indent=2)
    print(f"Mapper: {mapped} mapped, {nosrc} nosource")
if __name__=="__main__":main()
