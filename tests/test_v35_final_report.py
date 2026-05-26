import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_strategy_validation.final_report_builder import build_v35_final_validation_report

def test_report():
    r=build_v35_final_validation_report(validation_result={"validation_status":"STRATEGY_VALIDATION_REPORT_READY","date_count":1,"brd_connected":True,"fallback_rate":0,"metrics":{"valid_outcome_count":1},"failure_analysis":{}},replay_result={"daily_results":[{"paper_actions":[{"paper_id":"p1","role":"B_MID_ROTATION","sector_phase":"主升","paper_action":"PAPER_WATCH_ROTATION"}],"outcomes":[{"paper_id":"p1","outcome_status":"READY","actual_return_t20":0.1}]}]},horizon="t20")
    assert r["real_trade_allowed"] is False; assert r["policy_violations"]==[]
    print("✅ final report builder")

if __name__=="__main__": test_report(); print("\n🏁 Final Report PASS")
