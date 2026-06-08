#!/usr/bin/env python3
"""V13.F4.0.1 — Stage B: lane contract violation audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
contracts = json.loads((B2 / "v13_f4_0_batch2_subsession_contracts.json").read_text()).get("subsession_contracts", [])
violations = []
source_audit_violations = []

for c in contracts:
    fid = c["factor_id"]
    lane_type = c["lane_type"]
    
    co = json.loads((B2 / fid / f"{fid.lower()}_closeout.json").read_text()) if (B2 / fid / f"{fid.lower()}_closeout.json").exists() else {}
    mat = co.get("materialization_executed", False)
    val = co.get("single_factor_validation_executed", False)
    ev = co.get("evidence_score", "")

    if lane_type == "SOURCE_AUDIT_ONLY":
        reasons = []
        if mat is True: reasons.append("source_audit_only_lane_materialized")
        if val is True: reasons.append("source_audit_only_lane_validated")
        if ev == "PASS_RESEARCH_EVIDENCE": reasons.append("source_audit_only_lane_claimed_pass_research_evidence")
        if reasons:
            violations.append({"factor_id": fid, "lane_type": lane_type, "violation_reasons": reasons})
            source_audit_violations.append(fid)

(B2 / "v13_f4_0_1_batch2_lane_contract_violation_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-1-BATCH2-LANE-CONTRACT-VIOLATION-AUDIT",
    "status": "V13_F4_0_1_BATCH2_LANE_CONTRACT_VIOLATION_AUDIT_BUILT",
    "audited_lane_count": len(contracts),
    "contract_violation_count": len(violations),
    "contract_violating_factors": [v["factor_id"] for v in violations],
    "source_audit_only_violations": source_audit_violations,
    "violations": violations,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0.1-B] Lane audit: {len(violations)} violations: {source_audit_violations}")
sys.exit(0)
