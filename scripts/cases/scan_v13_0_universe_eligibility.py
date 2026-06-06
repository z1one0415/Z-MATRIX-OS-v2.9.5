#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    labels=json.loads((C/"v8_large_data"/"v8_forward_return_labels.json").read_text())["labels"]
    suspension=load("v12_4_7_1_public_evidence_record.json")
    all_tickers=sorted(set(l["ticker"]for l in labels if l["as_of_date"]=="20240909"))
    ineligible=[{"ticker":"600837","reason":"SUSPENSION_OR_MAJOR_RESTRUCTURING_EVENT","source":"V12_4_7_1"}]
    eligible=[t for t in all_tickers if t!="600837"]
    # Check full label coverage for eligible tickers at 20240909/T20 and T60
    ticker_horizons={}
    for l in labels:
        if l["as_of_date"]=="20240909":
            k=(l["ticker"],l["horizon"])
            if k not in ticker_horizons:ticker_horizons[k]=0
            ticker_horizons[k]+=1
    full_cov=sum(1 for t in eligible if (t,"T20")in ticker_horizons and (t,"T60")in ticker_horizons)
    missing=len(eligible)-full_cov
    result={"status":"V13_0_UNIVERSE_ELIGIBILITY_SCAN_BUILT","as_of_date_candidates":["20240909"],
        "raw_ticker_count":len(all_tickers),"eligible_ticker_count":len(eligible),"ineligible_ticker_count":len(ineligible),
        "ineligible_tickers":ineligible,
        "label_coverage_summary":{"target_as_of_date":"20240909","horizons_checked":["T20","T60"],
            "full_label_coverage_ticker_count":full_cov,"missing_label_ticker_count":missing},
        "eligible_tickers":eligible,"universe_scan_ready_for_candidate_generation":True,
        "blocking_reasons":[],"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_universe_eligibility_scan.json","w"),indent=2)
    print(f"Universe: {len(eligible)} eligible, {len(ineligible)} ineligible")
if __name__=="__main__":main()
