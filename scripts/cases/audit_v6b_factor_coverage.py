#!/usr/bin/env python3
"""V6-C: Coverage audit — count valid factor values vs expected."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
data=json.loads((C/"v6b_price_only_factor_values.json").read_text())
FIDS=list(data["records"][0]["factor_values"].keys()) if data["records"] else []
exp=data["as_of_date_count"]*data["core_12_cases"]*len(FIDS)
valid=sum(len(r["factor_values"]) for r in data["records"])
cov_by_f={fid:round(sum(1 for r in data["records"] if fid in r["factor_values"])/(len(data["records"])or 1),4) for fid in FIDS}
tickers=list(set(r["ticker"] for r in data["records"]))
cov_by_t={tk:round(sum(1 for r in data["records"] if r["ticker"]==tk)/(data["as_of_date_count"]or 1),4) for tk in tickers}
audit={"status":"V6B_FACTOR_COVERAGE_AUDIT_PASS" if valid/exp>=0.95 else "BELOW_THRESHOLD",
       "expected_records":exp,"valid_records":valid,
       "coverage":round(valid/exp,4) if exp else 0,
       "coverage_by_factor":cov_by_f,"coverage_by_ticker":cov_by_t,
       "missing_policy":"MISSING_NOT_ZERO_FILLED"}
(C/"v6b_factor_coverage_audit.json").write_text(json.dumps(audit,indent=2,ensure_ascii=False))
print(f"Coverage: {valid}/{exp}={audit['coverage']}")
