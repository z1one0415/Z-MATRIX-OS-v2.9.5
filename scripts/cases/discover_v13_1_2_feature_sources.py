#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
FEATURE_PATHS=["data/research_db/features","data/research_db/features/processed","data/research_db/features/raw","data/research_db/fundamentals","data/research_db/fundamentals/processed","data/research_db/fundamentals/raw","data/research_db/classification","data/research_db/classification/processed","data/research_db/classification/raw","data/research_db/market_data/processed","data/research_db/market_data/raw"]
MANIFEST_PATTERNS=["feature_source_manifest","v13_feature_manifest","mounted_feature_data_provenance"]
IGNORE_PATTERNS=["audit","closeout","contract","schema","validation","full_chain","requirement","report","scorecard","registry"]
def main():
    root=C.parent.parent;raw_seen=0;accepted=0;ignored=0;sources=[]
    for sp in FEATURE_PATHS:
        dp=root/sp
        if not dp.exists():continue
        for f in dp.rglob("*"):
            if not f.is_file():continue
            raw_seen+=1;fn=f.name.lower()
            is_manifest=any(m in fn for m in MANIFEST_PATTERNS)
            is_ignored=any(i in fn for i in IGNORE_PATTERNS)
            if is_ignored and not is_manifest:ignored+=1;continue
            accepted+=1
            cat="unknown"
            if"sector"in fn or"industry"in fn:cat="sector_or_industry"
            elif"fundamental"in fn or"quality"in fn:cat="fundamental_proxy_field"
            elif"price"in fn or"daily"in fn or"bar"in fn:cat="price_bar_input"
            elif"turnover"in fn:cat="turnover"
            elif"volume"in fn:cat="turnover"
            sources.append({"source_path":str(f.relative_to(root)),"source_kind":"FEATURE_MANIFEST"if is_manifest else"DATA_FILE","source_category_guess":cat,"accepted_as_feature_source":True,"file_type":"csv"if f.suffix==".csv"else"json"if f.suffix==".json"else"unknown","size_bytes":f.stat().st_size,"readable":True})
    found_sector=any("sector"in s["source_path"].lower()or"industry"in s["source_path"].lower()for s in sources)
    found_fund=any("fundamental"in s["source_path"].lower()or"quality"in s["source_path"].lower()for s in sources)
    found_price=any("price"in s["source_path"].lower()or"daily"in s["source_path"].lower()or"bar"in s["source_path"].lower()for s in sources)
    found_turn=any("turnover"in s["source_path"].lower()or"volume"in s["source_path"].lower()for s in sources)
    result={"status":"V13_1_2_FEATURE_SOURCE_DISCOVERY_BUILT","candidate_paths_checked_count":len(FEATURE_PATHS),"raw_files_seen_count":raw_seen,"accepted_feature_source_count":accepted,"ignored_runtime_report_count":ignored,"sources_found":accepted,"sector_or_industry_source_found":found_sector,"fundamental_proxy_source_found":found_fund,"price_bar_source_found":found_price,"turnover_source_found":found_turn,"sources":sources,"ready_for_feature_schema_validation":accepted>0,"blocking_reasons":[]if accepted>0 else["FEATURE_SOURCES_NOT_MOUNTED"],"ready_for_v13_2_bucket_construction_next_stage":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_2_feature_source_discovery.json","w"),indent=2)
    print(f"Discovery: {accepted} accepted, {raw_seen} seen, {ignored} ignored")
if __name__=="__main__":main()
