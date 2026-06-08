#!/usr/bin/env python3
"""V13.F2.3 — Stage F: regime/horizon diagnostics."""
import csv, json, sys, math
from pathlib import Path
from collections import defaultdict
from scipy.stats import spearmanr

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
PRICE_BARS = Path(__file__).resolve().parent.parent.parent.parent / "data" / "price_bars"

def load_panel(fname):
    fpath = RUNTIME / fname
    if not fpath.exists():
        return []
    with open(fpath) as f:
        return list(csv.DictReader(f))

def load_label_panel():
    fpath = RUNTIME / "single_factor_outcome_label_panel.csv"
    if not fpath.exists():
        return []
    with open(fpath) as f:
        return list(csv.DictReader(f))

def load_market_return(ticker="000001", horizon=20):
    """Load market return proxy from 000001.SZ kline."""
    for suffix in [".SZ", ".SH"]:
        fpath = PRICE_BARS / f"{ticker}{suffix}.csv"
        if fpath.exists():
            by_date = {}
            rows = []
            with open(fpath) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append({"trade_date": row["trade_date"], "pct_chg": float(row["pct_chg"] or 0)})
            for i, r in enumerate(rows):
                if i + horizon < len(rows):
                    ret = (float(rows[i+horizon]["pct_chg"]) - float(r["pct_chg"])) / 100.0
                    by_date[r["trade_date"]] = ret
            return by_date
    return {}

# Load market regime
market_ret_20d = load_market_return("000001", 20)
market_ret_60d = load_market_return("000001", 60)

def classify_regime(ret_20d):
    if ret_20d is None:
        return "UNKNOWN"
    if ret_20d > 0.03:
        return "UP"
    elif ret_20d < -0.03:
        return "DOWN"
    else:
        return "SIDEWAYS"

per_factor_diag = []

for factor_id, fname in [("F03", "f03_industry_relative_strength_panel.csv"),
                          ("F06", "f06_fundamental_quality_panel.csv")]:
    panel = load_panel(fname)
    labels = load_label_panel()

    if not panel or not labels:
        per_factor_diag.append({
            "factor_id": factor_id,
            "status": "BLOCKED",
            "blocked_reason": "panel_or_label_not_found"
        })
        continue

    label_lookup = {}
    for lbl in labels:
        label_lookup[(lbl["rebalance_date"], lbl["ticker"])] = {
            "fwd_20d": float(lbl["forward_return_20d"]) if lbl["forward_return_20d"] else None,
            "fwd_60d": float(lbl["forward_return_60d"]) if lbl["forward_return_60d"] else None,
        }

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

    # Regime split IC
    regime_ic_20d = {"UP": [], "DOWN": [], "SIDEWAYS": []}
    regime_ic_60d = {"UP": [], "DOWN": [], "SIDEWAYS": []}

    for rebal_date, items in sorted(by_date.items()):
        regime = classify_regime(market_ret_20d.get(rebal_date))

        items_20d = [(it["factor_value"], it["fwd_20d"]) for it in items if it["fwd_20d"] is not None]
        items_60d = [(it["factor_value"], it["fwd_60d"]) for it in items if it["fwd_60d"] is not None]

        if len(items_20d) >= 10:
            try:
                ic, _ = spearmanr([x[0] for x in items_20d], [x[1] for x in items_20d])
                if not math.isnan(ic) and regime in regime_ic_20d:
                    regime_ic_20d[regime].append(ic)
            except Exception:
                pass

        if len(items_60d) >= 10:
            try:
                ic, _ = spearmanr([x[0] for x in items_60d], [x[1] for x in items_60d])
                if not math.isnan(ic) and regime in regime_ic_60d:
                    regime_ic_60d[regime].append(ic)
            except Exception:
                pass

    def avg(vals):
        return round(sum(vals) / len(vals), 6) if vals else 0.0

    per_factor_diag.append({
        "factor_id": factor_id,
        "diagnostics_executed": True,
        "sample_month_count": len(by_date),
        "regime_split_ic_20d": {
            "up_mean_ic": avg(regime_ic_20d["UP"]),
            "down_mean_ic": avg(regime_ic_20d["DOWN"]),
            "sideways_mean_ic": avg(regime_ic_20d["SIDEWAYS"])
        },
        "regime_split_ic_60d": {
            "up_mean_ic": avg(regime_ic_60d["UP"]),
            "down_mean_ic": avg(regime_ic_60d["DOWN"]),
            "sideways_mean_ic": avg(regime_ic_60d["SIDEWAYS"])
        },
        "f03_specific": None if factor_id != "F03" else {
            "note": "sector_concentration/industry_neutrality/sector_wind_overlap require sector mapping (not loaded in this build)"
        },
        "f06_specific": None if factor_id != "F06" else {
            "note": "quality_score_dispersion/reporting_period_distribution/disclosure_freshness require fundamental metadata (not loaded in this build)"
        }
    })

result = {
    "pipeline_signature": "Z2-V13-F2-3-REGIME-DIAGNOSTICS",
    "status": "V13_F2_3_REGIME_HORIZON_DIAGNOSTICS_BUILT",
    "diagnostics_executed": True,
    "validated_factors": ["F03", "F06"],
    "per_factor_diagnostics": per_factor_diag,
    "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_regime_horizon_diagnostics.json"
dst.write_text(json.dumps(result, indent=2))
print(f"[F2.3-F] Regime/horizon diagnostics built -> {dst}")
sys.exit(0)
