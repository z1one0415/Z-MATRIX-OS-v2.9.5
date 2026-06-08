#!/usr/bin/env python3
"""V13.F2.3 — Stage E: bucket spread validation."""
import csv, json, sys
from pathlib import Path
from collections import defaultdict
import math

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

def load_panel(fname: str) -> list[dict]:
    fpath = RUNTIME / fname
    if not fpath.exists():
        return []
    with open(fpath) as f:
        return list(csv.DictReader(f))

def load_label_panel() -> list[dict]:
    fpath = RUNTIME / "single_factor_outcome_label_panel.csv"
    if not fpath.exists():
        return []
    with open(fpath) as f:
        return list(csv.DictReader(f))

labels = load_label_panel()
if not labels:
    result = {
        "pipeline_signature": "Z2-V13-F2-3-BUCKET",
        "status": "V13_F2_3_SINGLE_FACTOR_BUCKET_VALIDATION_BLOCKED",
        "bucket_validation_executed": False,
        "blocked_reason": "label_panel_not_found",
        "alpha_claim_allowed": False,
        "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
    }
    (RUNTIME / "v13_f2_3_single_factor_bucket_validation.json").write_text(json.dumps(result, indent=2))
    sys.exit(0)

label_lookup = {}
for lbl in labels:
    key = (lbl["rebalance_date"], lbl["ticker"])
    label_lookup[key] = {
        "fwd_20d": float(lbl["forward_return_20d"]) if lbl["forward_return_20d"] else None,
        "fwd_60d": float(lbl["forward_return_60d"]) if lbl["forward_return_60d"] else None,
    }

BUCKET_COST_BPS = 30  # round-trip cost

def compute_buckets(panel, factor_id):
    """Compute 3-bucket spread for a factor."""
    if not panel:
        return None

    # Group by date and attach labels
    by_date = defaultdict(list)
    for row in panel:
        key = (row["rebalance_date"], row["ticker"])
        lbl = label_lookup.get(key)
        if lbl is None:
            continue
        factor_val = float(row.get("factor_value", row.get("relative_strength_score", 0)))
        by_date[row["rebalance_date"]].append({
            "ticker": row["ticker"],
            "factor_value": factor_val,
            "fwd_20d": lbl["fwd_20d"],
            "fwd_60d": lbl["fwd_60d"]
        })

    bucket_assignments = []
    monthly_spreads_20d = []
    monthly_spreads_60d = []
    monotonicity_20d_list = []
    monotonicity_60d_list = []

    for rebal_date, items in sorted(by_date.items()):
        items.sort(key=lambda x: x["factor_value"])
        n = len(items)
        if n < 6:
            continue

        third = max(1, n // 3)

        low = items[:third]
        mid = items[third:2*third]
        high = items[2*third:]

        def avg_fwd(item_list, horizon):
            vals = [it[f"fwd_{horizon}d"] for it in item_list if it[f"fwd_{horizon}d"] is not None]
            return sum(vals) / len(vals) if vals else 0.0

        low_20d = avg_fwd(low, 20)
        mid_20d = avg_fwd(mid, 20)
        high_20d = avg_fwd(high, 20)
        low_60d = avg_fwd(low, 60)
        mid_60d = avg_fwd(mid, 60)
        high_60d = avg_fwd(high, 60)

        spread_20d = high_20d - low_20d
        spread_60d = high_60d - low_60d
        cost_adj_20d = spread_20d - BUCKET_COST_BPS / 10000
        cost_adj_60d = spread_60d - BUCKET_COST_BPS / 10000

        monthly_spreads_20d.append(spread_20d)
        monthly_spreads_60d.append(spread_60d)

        # Monotonicity: LOW < MID < HIGH
        monotonicity_20d_list.append(low_20d < mid_20d < high_20d)
        monotonicity_60d_list.append(low_60d < mid_60d < high_60d)

        for bucket_label, items_in_bucket in [("LOW", low), ("MID", mid), ("HIGH", high)]:
            for it in items_in_bucket:
                bucket_assignments.append({
                    "rebalance_date": rebal_date,
                    "ticker": it["ticker"],
                    "factor_id": factor_id,
                    "bucket": bucket_label,
                    "factor_value": round(it["factor_value"], 4),
                    "bucket_forward_return_20d": round(it["fwd_20d"], 6) if it["fwd_20d"] is not None else "",
                    "bucket_forward_return_60d": round(it["fwd_60d"], 6) if it["fwd_60d"] is not None else ""
                })

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0.0

    return {
        "factor_id": factor_id,
        "sample_month_count": len(monthly_spreads_20d),
        "high_low_spread_20d": round(avg(monthly_spreads_20d), 6),
        "high_low_spread_60d": round(avg(monthly_spreads_60d), 6),
        "cost_adjusted_high_low_spread_20d": round(avg(monthly_spreads_20d) - BUCKET_COST_BPS / 10000, 6),
        "cost_adjusted_high_low_spread_60d": round(avg(monthly_spreads_60d) - BUCKET_COST_BPS / 10000, 6),
        "bucket_monotonicity_20d_rate": round(sum(monotonicity_20d_list) / len(monotonicity_20d_list), 4) if monotonicity_20d_list else 0.0,
        "bucket_monotonicity_60d_rate": round(sum(monotonicity_60d_list) / len(monotonicity_60d_list), 4) if monotonicity_60d_list else 0.0,
        "bucket_validation_executed": True,
        "bucket_evidence_status": "PASS" if len(monthly_spreads_20d) >= 12 else "BLOCKED_BY_INSUFFICIENT_SAMPLE"
    }, bucket_assignments

per_factor_bucket = []
all_assignments = []

for factor_id, fname in [("F03", "f03_industry_relative_strength_panel.csv"),
                          ("F06", "f06_fundamental_quality_panel.csv")]:
    panel = load_panel(fname)
    if not panel:
        per_factor_bucket.append({
            "factor_id": factor_id,
            "bucket_validation_executed": False,
            "blocked_reason": "panel_not_found"
        })
        continue
    result, assigns = compute_buckets(panel, factor_id)
    if result:
        per_factor_bucket.append(result)
        all_assignments.extend(assigns)
    else:
        per_factor_bucket.append({
            "factor_id": factor_id,
            "bucket_validation_executed": False,
            "blocked_reason": "insufficient_data"
        })

# Write bucket assignments
assign_path = RUNTIME / "v13_f2_3_single_factor_bucket_assignments.csv"
if all_assignments:
    fieldnames = ["rebalance_date", "ticker", "factor_id", "bucket", "factor_value",
                  "bucket_forward_return_20d", "bucket_forward_return_60d"]
    with open(assign_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_assignments)

all_executed = all(f.get("bucket_validation_executed", False) for f in per_factor_bucket)

result = {
    "pipeline_signature": "Z2-V13-F2-3-BUCKET",
    "status": "V13_F2_3_SINGLE_FACTOR_BUCKET_VALIDATION_BUILT",
    "bucket_validation_executed": all_executed,
    "validated_factors": ["F03", "F06"],
    "bucket_count": 3,
    "bucket_labels": ["LOW", "MID", "HIGH"],
    "per_factor_bucket_evidence": per_factor_bucket,
    "multi_factor_composite_built": False,
    "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_single_factor_bucket_validation.json"
dst.write_text(json.dumps(result, indent=2))
print(f"[F2.3-E] Bucket validation built -> {dst}")
sys.exit(0)
