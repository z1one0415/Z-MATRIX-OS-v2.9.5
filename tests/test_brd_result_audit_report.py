import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_result_audit.audit_report_builder import build_brd_result_audit_report

def test_report():
    daily={"paper_actions":[{"paper_id":"p1","ticker":"000001","role":"B_MID_ROTATION","paper_action":"PAPER_WATCH_ROTATION","source_brd_result":{"reason_codes":["B_MATRIX_BASE_ELIGIBLE"],"source_raw":{"b_matrix":{"reason_codes":["B_MATRIX_BASE_ELIGIBLE"],"role_cap":"B_MID_ROTATION"}}}}]*1000,"outcomes":[{"paper_id":"p1","outcome_status":"READY","actual_return_t20":0.1}]*1000}
    r=build_brd_result_audit_report(replay_result={"daily_results":[daily]})
    assert r["audit_status"]=="PASS"; assert r["real_trade_allowed"] is False; assert r["policy_violations"]==[]
    print(f"✅ audit: status={r['audit_status']}")

if __name__=="__main__": test_report(); print("\n🏁 Audit Report PASS")
