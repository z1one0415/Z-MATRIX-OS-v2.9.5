#!/usr/bin/env python3
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    co=load("v12_4_6_price_data_restore_closeout.json")
    ok="CONFIRMED"in co.get("status","")
    ct={"status":"V12_4_7_PRICE_DATA_MOUNT_CONTRACT_BUILT"if ok else"V12_4_7_PRICE_DATA_MOUNT_CONTRACT_BLOCKED",
        "mount_mode":"SCHEMA_GATED_PRICE_DATA_MOUNT","target_ticker":"600837",
        "target_as_of_date":"20240909","target_horizon":"T60",
        "required_fields":["ticker","trade_date","close","adjusted_close","volume"],
        "candidate_files":["data/research_db/market_data/processed/v8_expanded_daily_price_bar.csv","data/research_db/market_data/processed/core12_daily_price_bar.csv"],
        "coverage_policy":"TICKER_DATE_TO_T60_EXIT_WINDOW_REQUIRED",
        "expected_exit_date_min":"20241201","expected_exit_date_max":"20241231",
        "fail_closed":True,"ready_for_label_regeneration":False,
        "ready_for_cycle2_recalculation":False,"ready_for_v12_5_feedback":False,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(ct,open(C/"v12_4_7_price_data_mount_contract.json","w"),indent=2)
    print(f"Contract: {ct['status']}")
if __name__=="__main__":main()
