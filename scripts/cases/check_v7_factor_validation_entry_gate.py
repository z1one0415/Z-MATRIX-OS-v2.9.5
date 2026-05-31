#!/usr/bin/env python3
"""V7 entry gate: only open if leakage-safe, coverage OK, enough factor values."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports/cases"
co=json.loads((C/"v6d_price_only_factor_closeout.json").read_text())
ok=co["leakage_audit_pass"] and co["coverage_audit_pass"] and co["factor_records"]>=10000
g={"status":"V7_FACTOR_VALIDATION_ENTRY_ALLOWED" if ok else "V7_ENTRY_BLOCKED",
   "ready_for_v7_factor_validation":ok,"ready_for_alpha_claim":False,
   "blocking_reasons":[],"warning":"V7 validation remains small-sample exploratory",
   "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
(C/"v7_factor_validation_entry_gate.json").write_text(json.dumps(g,indent=2,ensure_ascii=False))
print(f"V7: {'ALLOWED' if ok else 'BLOCKED'}")
