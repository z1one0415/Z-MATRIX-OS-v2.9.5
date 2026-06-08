#!/usr/bin/env python3
"""V13.F4.0.1 — Stage E: recompute child closeouts after coverage repair."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
FACTORS = {"F02":"MATERIALIZATION","F05":"MATERIALIZATION","F14":"MATERIALIZATION","F15":"MATERIALIZATION","F16":"MATERIALIZATION","F09":"SOURCE_AUDIT_VIOLATED"}

def load(fid, name):
    p = B2 / fid / name
    return json.loads(p.read_text()) if p.exists() else {}

def wj(fid, data):
    (B2 / fid / f"{fid.lower()}_closeout_recomputed.json").write_text(json.dumps(data, indent=2))

cov_repair = load("", "v13_f4_0_1_batch2_coverage_expansion_repair.json")
cov_map = {c["factor_id"]: c for c in cov_repair.get("per_factor_coverage_repair", [])}

for fid, ftype in FACTORS.items():
    if ftype == "SOURCE_AUDIT_VIOLATED":
        rc = {"factor_id": fid, "evidence_score": "SOURCE_AUDIT_CONTRACT_VIOLATED",
              "subsession_status": "BLOCKED", "ready_for_candidate_review": False,
              "alpha_claim_allowed": False, "production": "BLOCKED",
              "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"}
        wj(fid, rc)
        print(f"  [{fid}] → SOURCE_AUDIT_CONTRACT_VIOLATED")
        continue

    cr = cov_map.get(fid, {})
    cov_pass = cr.get("coverage_passed", False)
    tier = cr.get("coverage_tier", "N/A")
    cov_count = cr.get("expanded_covered_ticker_count", 0)

    if cov_pass:
        ev = "PASS_RESEARCH_EVIDENCE"
        status = "PASS"
        ready = True
    else:
        ev = "MATERIALIZED_BUT_COVERAGE_BLOCKED"
        status = "BLOCKED"
        ready = False

    rc = {"factor_id": fid, "evidence_score": ev,
          "subsession_status": status, "coverage_passed": cov_pass,
          "coverage_tier": tier, "expanded_covered_ticker_count": cov_count,
          "ready_for_candidate_review": ready,
          "ready_for_promotion_review": False,
          "recomputed_from_artifacts": True,
          "multi_factor_composite_built": False, "v13_6_allowed": False,
          "alpha_claim_allowed": False, "production": "BLOCKED",
          "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"}
    wj(fid, rc)
    print(f"  [{fid}] → {ev} (cov={cov_pass}, tier={tier})")

sys.exit(0)
