"""Tail-Risk Event Adapters tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.event_adapters import build_tail_risk_event, build_tail_gate_event, build_risk_isolation_event

def _ctrl():
    return {"controller_id":"c1","final_state":"HIBERNATE","final_decision":"HIBERNATE","action_policy_preview":{"requires_human_review":True}}
def _gate():
    return {"gate_id":"g1","gate_type":"HIBERNATE_MODE","state":"HIBERNATE","decision":"HIBERNATE","action_downgrade":"FREEZE_TO_HIBERNATE"}
def _isol():
    return {"isolation_id":"i1","ticker":"002472","isolation_reason":"crash","requires_human_review":True}

def test_tail_risk_event_adapters_do_not_append():
    e = build_tail_risk_event(_ctrl())
    assert "stored" not in e
    e2 = build_tail_gate_event(_gate())
    assert "stored" not in e2
    e3 = build_risk_isolation_event(_isol())
    assert "stored" not in e3
    print("✅ event adapters do not append")

def test_tail_risk_events_use_risk_event_type():
    e = build_tail_risk_event(_ctrl())
    assert e["event_type"] == "RiskEvent"
    print("✅ tail risk events use RiskEvent type")

if __name__ == "__main__":
    test_tail_risk_event_adapters_do_not_append()
    test_tail_risk_events_use_risk_event_type()
    print("\n🏁 Tail-Risk Event Adapters tests PASS")
