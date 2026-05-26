"""Risk Isolation Unit tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.risk_isolation_unit import build_risk_isolation_preview

def test_risk_isolation_blocks_average_down_and_revenge_trade():
    r = build_risk_isolation_preview(source_result={"gate_id": "g1", "decision": "ISOLATE"})
    assert r["allow_average_down"] is False
    assert r["allow_revenge_trade"] is False
    assert r["auto_sell_allowed"] is False
    print("✅ risk isolation blocks average down and revenge trade")

if __name__ == "__main__":
    test_risk_isolation_blocks_average_down_and_revenge_trade()
    print("\n🏁 Risk Isolation Unit tests PASS")
