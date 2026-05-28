#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.regime_observation.report_loader import load_v357_closeout_reports
from zmatrix.regime_observation.observation_report_builder import build_regime_observation_report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay-report", default="runtime_reports/v357_regime_conditioned_replay_report.json")
    ap.add_argument("--anti-overfit-report", default="runtime_reports/v357_anti_overfit_validation_report.json")
    ap.add_argument("--governance-report", default="runtime_reports/v357_governance_pool_resilience_report.json")
    ap.add_argument("--output", default="runtime_reports/v358_regime_observation_pool_resilience_report.json")
    args = ap.parse_args()
    loaded = load_v357_closeout_reports(replay_path=args.replay_report, anti_overfit_path=args.anti_overfit_report, governance_path=args.governance_report)
    if loaded["load_status"] != "READY": print(json.dumps(loaded,ensure_ascii=False,indent=2)); raise SystemExit(2)
    report = build_regime_observation_report(replay_report=loaded["replay_report"],anti_overfit_report=loaded["anti_overfit_report"],governance_report=loaded["governance_report"])
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    s = {"report_version":report["report_version"],"final_observation_status":report["final_observation_status"],"recommended_next_step":report["recommended_next_step"],"sector_data_status":report["sector_data_audit"]["sector_data_status"],"matrix_clock_status":report["matrix_clock_metadata_audit"]["matrix_clock_status"],"conflict_status":report["zg18_conflict_observation"]["conflict_observation_status"],"fallback_status":report["o3_paper_fallback_study"]["fallback_study_status"],"policy_violations":report["policy_violations"],"real_trade_allowed":report["real_trade_allowed"]}
    print(json.dumps(s,ensure_ascii=False,indent=2))
    if report["policy_violations"]: raise SystemExit(3)
    print("v3.5.8 regime observation + pool resilience report generated")

if __name__ == "__main__": main()
