#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    co=load("v13_1_3_feature_mount_closeout.json")
    ok="CONFIRMED_BLOCKED"in co.get("status","")
    ct={"status":"V13_1_3_1_SOURCE_MOUNT_PROVENANCE_CONTRACT_BUILT"if ok else"V13_1_3_1_SOURCE_MOUNT_PROVENANCE_CONTRACT_BLOCKED","mount_stage":"REAL_FEATURE_SOURCE_FILE_MOUNT","target_as_of_date":"20240909","eligible_universe_ticker_count":70,"excluded_tickers":["600837"],"required_feature_groups":["sector_or_industry","fundamental_proxy_field","price_bar_input","turnover","rank_short_medium"],"source_mount_allowed":True,"feature_materialization_allowed":False,"v13_2_bucket_construction_allowed":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(ct,open(C/"v13_1_3_1_source_mount_provenance_contract.json","w"),indent=2)
    print(f"Contract: {ct['status']}")
if __name__=="__main__":main()
