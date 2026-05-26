"""Tail-Risk Architecture tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_tail_risk_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    req = ["tail.market_signals.normalize","tail.limit_down_blackhole.evaluate",
           "tail.domestic_liquidity_crash.evaluate","tail.hibernate_mode.evaluate",
           "tail.wakeup_probation.evaluate","tail.d_matrix_freeze.evaluate",
           "tail.risk_isolation.preview","tail.controller.preview","tail.policy.validate",
           "tail.controller_event.build","tail.gate_event.build","tail.isolation_event.build"]
    for s in req:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print(f"✅ {len(req)} Tail skills registered")

def test_tail_risk_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["tail_risk.signal.valid","tail_risk.preview_only.valid","tail_risk.no_broker_order.valid",
              "tail_risk.no_real_trade.valid","tail_risk.action_degradation.valid","tail_risk.no_auto_sell.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 6 Tail gates registered")

def test_tail_risk_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-TailRiskAutonomicGates" in PIPELINE_REGISTRY
    print("✅ Z-TailRiskAutonomicGates pipeline registered")

def test_tail_risk_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-TailRisk.autonomic_gates_preview_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    assert "required_gates" in WORKFLOW_DAG_REGISTRY[wid]
    print(f"✅ Tail workflow registered")

def test_tail_risk_workflow_required_gates():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY.get("Z-TailRisk.autonomic_gates_preview_workflow", {})
    req = ["tail_risk.signal.valid","tail_risk.preview_only.valid","tail_risk.no_broker_order.valid",
           "tail_risk.no_real_trade.valid","tail_risk.action_degradation.valid","tail_risk.no_auto_sell.valid",
           "safety.no_real_trade"]
    gates = w.get("required_gates", [])
    missing = [g for g in req if g not in gates]
    assert not missing, f"missing: {missing}"
    print(f"✅ workflow has {len(gates)} required gates")

def test_tail_risk_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/TAIL_RISK_GATES_V10.md","docs/contracts/LIMIT_DOWN_BLACKHOLE_V10.md",
        "docs/contracts/DOMESTIC_LIQUIDITY_CRASH_V10.md","docs/contracts/HIBERNATE_MODE_V10.md",
        "docs/contracts/WAKEUP_PROBATION_V10.md","docs/contracts/D_MATRIX_FREEZE_V10.md",
        "docs/contracts/BMO_RISK_ISOLATION_UNIT_V10.md","docs/contracts/TAIL_RISK_CONTROLLER_V10.md",
        "docs/architecture/TAIL_RISK_AUTONOMIC_GATES_PREVIEW_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} Tail risk docs exist")

def test_tail_risk_forbids_real_trade_and_broker_order():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-TailRiskAutonomicGates", {})
    fc = p.get("forbidden_capabilities", [])
    assert "real_trade" in fc
    assert "broker_order" in fc
    assert "auto_sell" in fc
    assert "auto_buy" in fc
    print("✅ pipeline forbids real trade, broker, auto sell/buy")

if __name__ == "__main__":
    test_tail_risk_skills_registered()
    test_tail_risk_gates_registered()
    test_tail_risk_pipeline_registered()
    test_tail_risk_workflow_registered()
    test_tail_risk_workflow_required_gates()
    test_tail_risk_docs_exist()
    test_tail_risk_forbids_real_trade_and_broker_order()
    print("\n🏁 Tail-Risk Architecture tests PASS")
