# allowlist: forbidden-token-definition
"""Matrix Precompute Report"""
from __future__ import annotations

def build_matrix_precompute_report(*, bundles):
    total = len(bundles or [])
    ready = [b for b in (bundles or []) if b.get("input_ready")]
    b_p = [b for b in (bundles or []) if b.get("b_matrix",{}).get("status")=="PASS"]
    r_p = [b for b in (bundles or []) if b.get("r_matrix",{}).get("status")=="PASS"]
    return {"report_version":"BRD_MATRIX_PRECOMPUTE_REPORT_V10","mode":"REPORT_ONLY",
            "total":total,"input_ready_count":len(ready),
            "b_matrix_pass_count":len(b_p),"r_matrix_pass_count":len(r_p),
            "real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False}
