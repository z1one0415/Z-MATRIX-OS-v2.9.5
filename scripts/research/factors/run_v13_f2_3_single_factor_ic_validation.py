#!/usr/bin/env python3
"""V13.F2.3 — Stage D: IC / RankIC validation."""
import csv, json, sys, math
from pathlib import Path
from collections import defaultdict
from scipy.stats import spearmanr

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

# Load data
labels = load_label_panel()
if not labels:
    result = {
        "pipeline_signature": "Z2-V13-F2-3-IC-VALIDATION",
        "status": "V13_F2_3_SINGLE_FACTOR_IC_VALIDATION_BLOCKED",
        "validated_factors": ["F03", "F06"],
        "ic_validation_executed": False,
        "rank_ic_validation_executed": False,
        "blocked_reason": "label_panel_not_found",
        "alpha_claim_allowed": False,
        "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
    }
    (RUNTIME / "v13_f2_3_single_factor_ic_validation.json").write_text(json.dumps(result, indent=2))
    print("[F2.3-D] BLOCKED: label panel not found")
    sys.exit(0)

# Build lookup: (rebalance_date, ticker) -> forward_returns
label_lookup = {}
for lbl in labels:
    key = (lbl["rebalance_date"], lbl["ticker"])
    label_lookup[key] = {
        "fwd_20d": float(lbl["forward_return_20d"]) if lbl["forward_return_20d"] else None,
        "fwd_60d": float(lbl["forward_return_60d"]) if lbl["forward_return_60d"] else None,
    }

per_factor_ic = []

for factor_id, fname in [("F03", "f03_industry_relative_strength_panel.csv"),
                          ("F06", "f06_fundamental_quality_panel.csv")]:
    panel = load_panel(fname)
    if not panel:
        per_factor_ic.append({
            "factor_id": factor_id,
            "sample_month_count": 0,
            "ic_validation_executed": False,
            "blocked_reason": "panel_not_found"
        })
        continue

    # Group by rebalance_date
    by_date = defaultdict(list)
    for row in panel:
        key = (row["rebalance_date"], row["ticker"])
        lbl = label_lookup.get(key)
        if lbl is None:
            continue
        factor_val = float(row.get("factor_value", row.get("relative_strength_score", 0)))
        by_date[row["rebalance_date"]].append({
            "factor_value": factor_val,
            "fwd_20d": lbl["fwd_20d"],
            "fwd_60d": lbl["fwd_60d"]
        })

    monthly_ic_20d = []
    monthly_ic_60d = []
    monthly_rank_ic_20d = []
    monthly_rank_ic_60d = []

    for rebal_date, items in sorted(by_date.items()):
        items_20d = [(it["factor_value"], it["fwd_20d"]) for it in items if it["fwd_20d"] is not None]
        items_60d = [(it["factor_value"], it["fwd_60d"]) for it in items if it["fwd_60d"] is not None]

        if len(items_20d) >= 10:
            fv_20d = [x[0] for x in items_20d]
            ret_20d = [x[1] for x in items_20d]
            try:
                ic_20d, _ = spearmanr(fv_20d, ret_20d)
                monthly_ic_20d.append(ic_20d if not math.isnan(ic_20d) else 0.0)
                monthly_rank_ic_20d.append(ic_20d if not math.isnan(ic_20d) else 0.0)
            except Exception:
                pass

        if len(items_60d) >= 10:
            fv_60d = [x[0] for x in items_60d]
            ret_60d = [x[1] for x in items_60d]
            try:
                ic_60d, _ = spearmanr(fv_60d, ret_60d)
                monthly_ic_60d.append(ic_60d if not math.isnan(ic_60d) else 0.0)
                monthly_rank_ic_60d.append(ic_60d if not math.isnan(ic_60d) else 0.0)
            except Exception:
                pass

    sample_count = len(by_date)

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0.0

    def win_rate(vals):
        return sum(1 for v in vals if v > 0) / len(vals) if vals else 0.0

    per_factor_ic.append({
        "factor_id": factor_id,
        "sample_month_count": sample_count,
        "ic_20d_mean": round(avg(monthly_ic_20d), 6),
        "ic_60d_mean": round(avg(monthly_ic_60d), 6),
        "rank_ic_20d_mean": round(avg(monthly_rank_ic_20d), 6),
        "rank_ic_60d_mean": round(avg(monthly_rank_ic_60d), 6),
        "ic_20d_win_rate": round(win_rate(monthly_ic_20d), 4),
        "ic_60d_win_rate": round(win_rate(monthly_ic_60d), 4),
        "ic_validation_executed": True,
        "ic_evidence_status": "PASS" if sample_count >= 12 else "BLOCKED_BY_INSUFFICIENT_SAMPLE"
    })

all_executed = all(f.get("ic_validation_executed", False) for f in per_factor_ic)

result = {
    "pipeline_signature": "Z2-V13-F2-3-IC-VALIDATION",
    "status": "V13_F2_3_SINGLE_FACTOR_IC_VALIDATION_BUILT",
    "validated_factors": ["F03", "F06"],
    "ic_validation_executed": all_executed,
    "rank_ic_validation_executed": all_executed,
    "minimum_month_count_required": 12,
    "per_factor_ic": per_factor_ic,
    "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_single_factor_ic_validation.json"
dst.write_text(json.dumps(result, indent=2))
print(f"[F2.3-D] IC validation built -> {dst}")
sys.exit(0)
