#!/usr/bin/env python3
# allowlist: forbidden-token-definition
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.governance_closeout.governance_report_builder import build_governance_closeout_report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-report", default="runtime_reports/v357_regime_conditioned_replay_report.json")
    ap.add_argument("--base-ref", default="6d5f624")
    ap.add_argument("--head-ref", default="HEAD")
    ap.add_argument("--output", default="runtime_reports/v357_governance_pool_resilience_report.json")
    args = ap.parse_args()
    path = Path(args.input_report)
    if not path.exists():
        print(json.dumps({"status":"BLOCKED_INPUT_REPORT_MISSING","real_trade_allowed":False,"broker_order_allowed":False},ensure_ascii=False,indent=2)); raise SystemExit(2)
    replay = json.loads(path.read_text(encoding="utf-8"))
    report = build_governance_closeout_report(regime_replay_report=replay, base_ref=args.base_ref, head_ref=args.head_ref)
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    s = {"report_version":report["report_version"],"governance_status":report["governance_status"],"yaml_mutation_detected":report["no_yaml_mutation_audit"]["yaml_mutation_detected"],"pool_statuses":{k:v.get("pool_resilience_status") for k,v in report["candidate_pool_resilience"]["policy_pool_results"].items()},"clock_alignment_status":report["matrix_clock_alignment_precheck"]["clock_alignment_status"],"conflict_precheck_status":report["zg18_conflict_precheck"]["conflict_precheck_status"],"fallback_plan_status":report["o3_conditional_fallback_plan"]["fallback_plan_status"],"policy_violations":report["policy_violations"],"recommended_next_step":report["recommended_next_step"],"real_trade_allowed":report["real_trade_allowed"]}
    print(json.dumps(s, ensure_ascii=False, indent=2))
    if report["policy_violations"]: raise SystemExit(3)
    print("v3.5.7 governance + pool resilience patch report generated")

if __name__ == "__main__": main()
