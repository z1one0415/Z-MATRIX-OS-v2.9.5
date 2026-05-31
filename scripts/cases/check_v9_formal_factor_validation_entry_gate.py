#!/usr/bin/env python3
"""V8-G: V9 entry gate — reads all V8 audits."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
rd=json.loads((C/"v8_expanded_data_readiness.json").read_text())
leak=json.loads((C/"v8_factor_leakage_audit.json").read_text())
cov=json.loads((C/"v8_factor_coverage_audit.json").read_text())
lcov=json.loads((C/"v8_label_coverage_audit.json").read_text())
c60=lcov["coverage_by_horizon"].get("T60",{}).get("valid_dates",0)
all_ok=(rd["ready_for_factor_rebuild"] and leak["leakage_safe"] and cov["coverage"]>=0.95 and c60>=400)
g={"status":"V9_FORMAL_FACTOR_VALIDATION_ENTRY_ALLOWED" if all_ok else "V9_ENTRY_BLOCKED_UNTIL_V8_REPRODUCIBLE","ready_for_v9_formal_validation":all_ok,"ready_for_alpha_claim":False,"reason":"All V8 audits pass" if all_ok else f"T60_dates={c60}, cov={cov['coverage']}, leak_safe={leak['leakage_safe']}","production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
(C/"v9_formal_factor_validation_entry_gate.json").write_text(json.dumps(g,indent=2,ensure_ascii=False))
print(f"V9: {'ALLOWED' if all_ok else 'BLOCKED'}")
