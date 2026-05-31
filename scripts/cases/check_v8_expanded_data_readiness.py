#!/usr/bin/env python3
"""V8-C: Check expanded data readiness."""
import json, csv, io
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
REG=json.loads((W/"data/research_db/cases/case_registry_v1.json").read_text())
EXP=[c for c in REG if c["case_layer"] in ("CORE","EXPANSION")]
tks_found=set()
for r in csv.DictReader(io.StringIO((W/"data/research_db/market_data/processed/v8_expanded_daily_price_bar.csv").read_text())): tks_found.add(r["ticker"])
td=sorted(set(r["trade_date"] for r in csv.DictReader(io.StringIO((W/"data/research_db/market_data/processed/v8_expanded_daily_price_bar.csv").read_text()))))
miss=[c["ticker"] for c in EXP if c["ticker"] not in tks_found]
rd={"status":"V8_EXPANDED_DATA_READY","universe_target_count":len(EXP),"data_ready_count":len(tks_found),"missing_tickers":miss,"missing_ticker_count":len(miss),"history_start":td[0] if td else None,"history_end":td[-1] if td else None,"trading_days":len(td),"price_coverage":round(len(tks_found)/len(EXP),4),"ready_for_factor_rebuild":len(tks_found)>=60,"ready_for_alpha_claim":False}
json.dump(rd,open(W/"runtime_reports/cases/v8_expanded_data_readiness.json","w"),indent=2)
print(f"Readiness: {len(tks_found)}/{len(EXP)} tickers, {len(td)} days")
