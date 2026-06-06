#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    co=load("v13_1_3_1_source_mount_closeout.json")
    ready=co.get("ready_for_v13_1_4_feature_materialization_next_stage",False) and "READY"in co.get("status","")
    ct={"status":"V13_1_4_FEATURE_MATERIALIZATION_CONTRACT_BUILT"if ready else"V13_1_4_FEATURE_MATERIALIZATION_CONTRACT_BLOCKED",
        "materialization_mode":"AS_OF_SAFE_FEATURE_STORE_BUILD","target_as_of_date":"20240909",
        "eligible_universe_ticker_count":70,"excluded_tickers":["600837"],
        "feature_materialization_allowed":ready,"v13_1_field_gate_rerun_allowed_next_stage":ready,
        "v13_2_bucket_construction_allowed":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(ct,open(C/"v13_1_4_feature_materialization_contract.json","w"),indent=2)
    print(f"MatContract: {'BLOCKED' if not ready else 'BUILT'} source_ready={ready}")
if __name__=="__main__":main()
