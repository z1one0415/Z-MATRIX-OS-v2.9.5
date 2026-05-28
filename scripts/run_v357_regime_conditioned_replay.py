#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.regime_conditioned_replay.dataset_loader import load_replay_dataset
from zmatrix.regime_conditioned_replay.replay_report_builder import build_replay_report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-items", type=int, default=None)
    ap.add_argument("--output", default="runtime_reports/v357_regime_conditioned_replay_report.json")
    args = ap.parse_args()
    d = load_replay_dataset()
    if d.get("dataset_status") != "READY": print(json.dumps(d, ensure_ascii=False, indent=2)); raise SystemExit(2)
    r = build_replay_report(joined=d["joined"], data_root=".", max_items=args.max_items)
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    s = {"report_version":r.get("report_version"),"input_count":r.get("input_count"),"feature_ready_rate":r.get("feature_ready_rate"),"baseline_raw":{"win_rate":r["baseline_raw"]["win_rate"],"median":r["baseline_raw"]["median"],"mean":r["baseline_raw"]["mean"],"trimmed_mean":r["baseline_raw"]["trimmed_mean_5pct"],"invalidation_rate":r["baseline_raw"]["invalidation_rate"],"top1pct":r["baseline_raw"]["top_1pct_contribution"]},"ready_policies":r.get("ready_policies"),"recommended_next_step":r.get("recommended_next_step"),"policy_violations":r.get("policy_violations"),"real_trade_allowed":r.get("real_trade_allowed")}
    for n, p in r.get("policy_results",{}).items():
        m=p["metrics"]; d=p.get("delta_vs_raw",{})
        s.setdefault("policies",{})[n]={"kept":p["kept_count"],"kept_rate":p["kept_rate"],"downgraded":p["downgraded_count"],"win_rate":m["win_rate"],"median":m["median"],"mean":m["mean"],"invalidation_rate":m["invalidation_rate"],"top1pct":m["top_1pct_contribution"],"opportunity_loss":p["opportunity_loss_rate"],"win_delta":d.get("win_rate_delta"),"median_delta":d.get("median_delta")}
    print(json.dumps(s, ensure_ascii=False, indent=2))
    if r.get("policy_violations"): raise SystemExit(3)
    print("v3.5.7 regime-conditioned paper replay report generated")

if __name__ == "__main__": main()
