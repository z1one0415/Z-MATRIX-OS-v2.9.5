#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.regime_conditioned_replay.regime_feature_loader import load_regime_features
from zmatrix.regime_conditioned_replay.regime_policy_library import apply_regime_policy
from zmatrix.regime_conditioned_replay.dataset_loader import load_replay_dataset
from zmatrix.regime_conditioned_replay.anti_overfit_report_builder import build_anti_overfit_report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-report", default="runtime_reports/v357_regime_conditioned_replay_report.json")
    ap.add_argument("--output", default="runtime_reports/v357_anti_overfit_validation_report.json")
    args = ap.parse_args()

    d = load_replay_dataset()
    if d.get("dataset_status") != "READY": print(json.dumps(d,ensure_ascii=False,indent=2)); raise SystemExit(2)

    features = load_regime_features(joined=d["joined"], data_root=".")
    rows = features["rows"]

    # Apply bull_only and range_obs policies
    for pn in ["allow_b_rotation_in_bull_trend_only","range_bound_observation_only"]:
        applied = apply_regime_policy(rows=rows, policy_name=pn)
        for i, r in enumerate(applied["kept"]):
            rows[rows.index(r) if r in rows else 0] = r  # will use join below
    # Actually let's just apply policies to all rows and tag them
    tagged_rows = []
    for r in rows:
        r2 = dict(r)
        r2["regime_policy_action"] = "KEEP"
        regime = r.get("market_regime","")
        liquidity = r.get("liquidity_regime","")
        # bull_only
        if regime != "BULL_TREND": r2["bull_only_action"] = "BLOCK"
        else: r2["bull_only_action"] = "KEEP"
        # range_obs
        if regime == "BEAR_TREND": r2["range_obs_action"] = "BLOCK"
        elif regime == "RANGE_BOUND": r2["range_obs_action"] = "OBSERVE_ONLY"
        else: r2["range_obs_action"] = "KEEP"
        tagged_rows.append(r2)

    # For validation, we need rows tagged per-policy. Let's do bull_only first
    r_bull = []
    for r in tagged_rows:
        r2 = dict(r)
        r2["regime_policy_action"] = r["bull_only_action"]
        r_bull.append(r2)

    r_range = []
    for r in tagged_rows:
        r2 = dict(r)
        r2["regime_policy_action"] = r["range_obs_action"]
        r_range.append(r2)

    report = build_anti_overfit_report(rows=tagged_rows, full_sample_policies=[])

    # Build per-policy validation
    report_bull = build_anti_overfit_report(rows=r_bull, full_sample_policies=["allow_b_rotation_in_bull_trend_only"])
    report_range = build_anti_overfit_report(rows=r_range, full_sample_policies=["range_bound_observation_only"])

    merged = {
        **report,
        "per_policy_validation": {
            "allow_b_rotation_in_bull_trend_only": {
                "temporal": report_bull["temporal_validation"].get("policy_results",{}).get("allow_b_rotation_in_bull_trend_only"),
                "sector": report_bull["sector_validation"].get("policy_results",{}).get("allow_b_rotation_in_bull_trend_only"),
                "stress": report_bull["stress_validation"].get("policy_results",{}).get("allow_b_rotation_in_bull_trend_only"),
                "opportunity": report_bull["opportunity_loss_validation"].get("policy_results",{}).get("allow_b_rotation_in_bull_trend_only"),
                "verdict": report_bull["stability_verdict"].get("verdicts",{}).get("allow_b_rotation_in_bull_trend_only"),
            },
            "range_bound_observation_only": {
                "temporal": report_range["temporal_validation"].get("policy_results",{}).get("range_bound_observation_only"),
                "sector": report_range["sector_validation"].get("policy_results",{}).get("range_bound_observation_only"),
                "stress": report_range["stress_validation"].get("policy_results",{}).get("range_bound_observation_only"),
                "opportunity": report_range["opportunity_loss_validation"].get("policy_results",{}).get("range_bound_observation_only"),
                "verdict": report_range["stability_verdict"].get("verdicts",{}).get("range_bound_observation_only"),
            },
        },
        "full_sample_pass_policies": ["allow_b_rotation_in_bull_trend_only","range_bound_observation_only"],
        "final_promoted_policies": [],
        "recommended_next_step": "v3.5.8 Regime Observation + Sector Data Enrichment",
    }

    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    for pn in ["allow_b_rotation_in_bull_trend_only","range_bound_observation_only"]:
        v = merged["per_policy_validation"][pn]["verdict"] or {}
        o = merged["per_policy_validation"][pn]["opportunity"] or {}
        t = merged["per_policy_validation"][pn]["temporal"] or {}
        print(f"\n=== {pn} ===")
        print(f"  anti_overfit_status: {v.get('anti_overfit_status')}")
        print(f"  reasons: {v.get('reasons')}")
        print(f"  kept_rate: {o.get('kept_rate')}")
        print(f"  temporal_status: {t.get('temporal_status')}")
        print(f"  opportunity_status: {o.get('opportunity_loss_status')}")

    print(f"\nfinal_promoted_policies: {merged['final_promoted_policies']}")
    print(f"recommended_next_step: {merged['recommended_next_step']}")
    print("v3.5.7 anti-overfit validation report generated")

if __name__ == "__main__": main()
