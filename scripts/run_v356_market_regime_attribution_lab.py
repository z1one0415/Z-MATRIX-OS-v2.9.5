#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.regime_attribution.dataset_loader import load_regime_dataset
from zmatrix.regime_attribution.market_index_loader import load_index_data
from zmatrix.regime_attribution.regime_report_builder import build_regime_attribution_report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-items", type=int, default=None)
    ap.add_argument("--output", default="runtime_reports/v356_market_regime_attribution_report.json")
    args = ap.parse_args()
    dataset = load_regime_dataset(replay_path="runtime_reports/v35_brd_strategy_replay_result.json")
    if dataset.get("dataset_status") != "READY":
        print(json.dumps(dataset, ensure_ascii=False, indent=2)); raise SystemExit(2)
    index_data = load_index_data(data_root=".")
    print(f"Indexes: {index_data.get('available_indexes')} (missing: {index_data.get('missing_indexes')})", flush=True)
    report = build_regime_attribution_report(joined=dataset["joined"], index_data=index_data.get("index_data",{}), max_items=args.max_items)
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    p = report.get("regime_performance_profile",{})
    s = report.get("regime_separability",{})
    c = report.get("regime_candidates",{})
    summary = {"report_version":report.get("report_version"),"input_count":report.get("input_count"),"feature_ready_rate":report.get("feature_ready_rate"),"market_regime_counts":report.get("market_regime_counts"),"best_regime":p.get("best_regime_segment"),"worst_regime":p.get("worst_regime_segment"),"separability_status":s.get("separability_status"),"separability_score":s.get("separability_score"),"candidate_count":c.get("candidate_count"),"candidates":[x.get("candidate_name") for x in c.get("candidates",[])],"recommended_next_step":report.get("recommended_next_step"),"policy_violations":report.get("policy_violations"),"real_trade_allowed":report.get("real_trade_allowed"),"broker_order_allowed":report.get("broker_order_allowed")}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report.get("policy_violations"): raise SystemExit(3)
    print("v3.5.6 market regime attribution report generated")

if __name__ == "__main__": main()
