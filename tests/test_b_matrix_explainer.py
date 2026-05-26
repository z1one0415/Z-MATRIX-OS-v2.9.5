import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_result_audit.b_matrix_explainer import explain_b_matrix_result

def test_explainer():
    b={"status":"DEGRADED","quality_score":80,"growth_score":70,"valuation_score":20,"valuation_data_status":"MISSING","valuation_confidence":"NONE","valuation_method":"UNAVAILABLE","role_cap":"B_MID_ROTATION","reason_codes":["VALUATION_DATA_MISSING"],"downgrade":{"downgraded":True,"downgrade_reason":"VALUATION_DATA_MISSING","from_role_cap":"A_LONG_CORE","to_role_cap":"B_MID_ROTATION"}}
    r=explain_b_matrix_result(ticker="000001",b_matrix=b)
    assert r["downgrade"]["downgraded"] is True; assert r["real_trade_allowed"] is False
    print(f"✅ explain: {r['human_readable_explanation'][:3]}")

if __name__=="__main__": test_explainer(); print("\n🏁 Explainer PASS")
