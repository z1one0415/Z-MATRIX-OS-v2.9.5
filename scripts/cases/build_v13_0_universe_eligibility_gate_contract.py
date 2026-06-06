#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v13_0_research_restart_contract.json")
    ok=ct.get("v13_candidate_discovery_allowed",False)
    gt={"status":"V13_0_UNIVERSE_ELIGIBILITY_GATE_CONTRACT_BUILT"if ok else"V13_0_UNIVERSE_ELIGIBILITY_GATE_CONTRACT_BLOCKED",
        "gate_mode":"PRE_CANDIDATE_UNIVERSE_AND_LABEL_ELIGIBILITY",
        "required_filters":["TRADING_STATUS_AVAILABLE_OR_FAIL_CLOSED","NOT_SUSPENDED","NOT_MAJOR_RESTRUCTURING_EVENT","NOT_DELISTING_TERMINATION","FULL_FORWARD_LABEL_COVERAGE","MIN_BUCKET_SIZE","MAX_BUCKET_IMBALANCE","NO_PARTIAL_TICKER_AVERAGING"],
        "min_bucket_size":10,"max_bucket_size_imbalance":2,"label_coverage_policy":"FULL_TICKER_COVERAGE_REQUIRED",
        "missing_label_policy":"FAIL_CLOSED_OR_ELIGIBILITY_ADJUDICATION","suspension_policy":"EXCLUDE_BEFORE_BUCKET_CONSTRUCTION",
        "ready_for_universe_scan":True,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(gt,open(C/"v13_0_universe_eligibility_gate_contract.json","w"),indent=2)
    print(f"UniverseGate: {gt['status']}")
if __name__=="__main__":main()
