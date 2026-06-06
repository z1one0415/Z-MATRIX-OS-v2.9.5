#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    reg=load("v13_1_candidate_registry.json");us=load("v13_0_universe_eligibility_scan.json")
    labels=json.loads((C/"v8_large_data"/"v8_forward_return_labels.json").read_text())["labels"]
    eligible=set(us.get("eligible_tickers",[]))
    items=[];fc=0;bl=0
    for r in reg.get("registry_items",[]):
        hz=r["target_horizon"];ad="20240909"
        covered=sum(1 for l in labels if l["as_of_date"]==ad and l["horizon"]==hz and l["ticker"]in eligible)
        ok=covered==len(eligible)
        if ok:fc+=1
        else:bl+=1
        items.append({"v13_1_candidate_run_id":r["v13_1_candidate_run_id"],"factor_name":r["factor_name"],
            "target_horizon":hz,"eligible_ticker_count":len(eligible),"label_covered_ticker_count":covered,
            "missing_label_ticker_count":len(eligible)-covered,"full_label_coverage":ok,
            "label_coverage_status":"FULL_COVERAGE"if ok else"BLOCKED_MISSING_LABELS"})
    result={"status":"V13_1_LABEL_COVERAGE_CHECK_BUILT","candidate_count":len(items),
        "full_coverage_candidate_count":fc,"blocked_label_candidate_count":bl,
        "excluded_tickers":["600837"],"checks":items,"ready_for_bucket_construction_count":fc,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_label_coverage.json","w"),indent=2)
    print(f"Labels: {fc} full, {bl} blocked")
if __name__=="__main__":main()
