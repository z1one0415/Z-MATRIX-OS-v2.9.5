#!/usr/bin/env python3
"""V13.F3.4.1 — Stage B: resolve last in-sample rebalance dates from artifacts."""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTORS = ["F04","F10","F11"]

def find_last_rebalance_date(fid):
    """Scan multiple artifacts for the latest rebalance date, in priority order."""
    candidates = []

    # 1. Panel CSV (most authoritative)
    for prefix in ["f04_coverage_expanded_panel", f"{fid.lower()}_panel"]:
        p = B / fid / f"{prefix}.csv"
        if p.exists():
            with open(p) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rd = row.get("rebalance_date", "")
                    if rd:
                        candidates.append(rd)
            if candidates:
                break

    # 2. Bucket assignments CSV
    p = B / fid / f"{fid.lower()}_bucket_assignments.csv"
    if p.exists():
        with open(p) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rd = row.get("rebalance_date", "")
                if rd:
                    candidates.append(rd)

    # 3. Outcome label panel
    p = ROOT / "runtime_reports" / "research" / "factors" / "single_factor_outcome_label_panel.csv"
    if p.exists():
        with open(p) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rd = row.get("rebalance_date", "")
                if rd:
                    candidates.append(rd)

    # Parse and find max
    if not candidates:
        return {"factor_id": fid, "resolved": False, "last_in_sample_rebalance_date": "N/A", "source_rebalance_date_count": 0, "blocked_reasons": ["no_rebalance_dates_found_in_any_artifact"]}

    # Extract max date
    max_date = max(candidates)
    return {"factor_id": fid, "resolved": True, "last_in_sample_rebalance_date": max_date, "source_rebalance_date_count": len(set(candidates)), "blocked_reasons": []}

results = [find_last_rebalance_date(fid) for fid in FACTORS]
resolved = sum(1 for r in results if r["resolved"])
blocked = [r for r in results if not r["resolved"]]

result = {
    "pipeline_signature": "Z2-V13-F3-4-1-LAST-IN-SAMPLE-DATE-RESOLUTION",
    "status": "V13_F3_4_1_LAST_IN_SAMPLE_REBALANCE_DATES_RESOLVED" if resolved == len(FACTORS) else "V13_F3_4_1_LAST_IN_SAMPLE_REBALANCE_DATES_BLOCKED",
    "candidate_scope": FACTORS,
    "resolved_factor_count": resolved,
    "blocked_factor_count": len(blocked),
    "unresolved_factors": [b["factor_id"] for b in blocked],
    "per_factor": results,
    "all_last_in_sample_dates_resolved": resolved == len(FACTORS),
    "any_na_last_in_sample_date": len(blocked) > 0,
    "true_oos_validation_executed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(B / "v13_f3_4_1_last_in_sample_rebalance_dates.json").write_text(json.dumps(result, indent=2))
if result["all_last_in_sample_dates_resolved"]:
    for r in results:
        print(f"  {r['factor_id']}: {r['last_in_sample_rebalance_date']} ({r['source_rebalance_date_count']} dates)")
else:
    for b in blocked:
        print(f"  ❌ {b['factor_id']}: BLOCKED - {b['blocked_reasons']}")
sys.exit(0)
