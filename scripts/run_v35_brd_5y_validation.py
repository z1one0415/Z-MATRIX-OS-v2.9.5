#!/usr/bin/env python3
"""v3.5 BRD 5Y Strategy Validation — run real historical validation"""
import json,sys
from pathlib import Path
from zmatrix.brd_strategy_validation.date_sampler import sample_replay_dates_from_index
from zmatrix.brd_strategy_validation.validation_runner import run_brd_5y_strategy_validation
from zmatrix.brd_strategy_validation.final_report_builder import build_v35_final_validation_report
from zmatrix.brd_strategy_validation.report_writer import write_validation_report
from zmatrix.brd_strategy_validation.validation_policy import validate_v35_validation_status

def main():
    sampled = sample_replay_dates_from_index(local_data_root=".",index_code="000001",max_dates=60)
    if sampled.get("sample_status")!="READY": print("BLOCKED: dates unavailable"); sys.exit(2)
    dates = sampled["dates"]
    print(f"Replay dates: {len(dates)}")
    validation = run_brd_5y_strategy_validation(replay_dates=dates,local_data_root=".",max_tickers=None,horizon="t20")
    replay_result = validation.get("source_replay_result",{})
    if not replay_result: print("BLOCKED: no replay_result"); sys.exit(3)
    final = build_v35_final_validation_report(validation_result=validation,replay_result=replay_result,horizon="t20")
    se = validate_v35_validation_status(final)
    out = write_validation_report(report=final,output_path="runtime_reports/v35_brd_5y_validation_report.json")
    summary = {"validation_status":final.get("validation_status"),"brd_connected":final.get("brd_connected"),
        "fallback_rate":final.get("fallback_rate"),"valid_outcome_count":final.get("metrics",{}).get("valid_outcome_count"),
        "t20_win_rate":final.get("metrics",{}).get("t20",{}).get("win_rate"),
        "t20_avg_return":final.get("metrics",{}).get("t20",{}).get("average_return"),
        "role_count":final.get("role_breakdown",{}).get("role_count"),"status_errors":se,"output":out}
    print(json.dumps(summary,indent=2,ensure_ascii=False))
    if final.get("validation_status")!="STRATEGY_VALIDATION_REPORT_READY": print("BLOCKED: not ready"); sys.exit(4)
    if se: print("BLOCKED: status errors"); sys.exit(5)
    print("v3.5 BRD 5Y Strategy Validation REPORT READY")

if __name__=="__main__": main()
