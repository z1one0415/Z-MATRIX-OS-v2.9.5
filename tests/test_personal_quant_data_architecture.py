"""Personal Quant Data Architecture Integration tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
from zmatrix.architecture.gate_registry import GATE_REGISTRY
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
from pathlib import Path
from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY

REQUIRED_SKILLS = ["data_facts.load_price_bars","paper_trade.ledger.build","paper_trade.outcome_backfill.calculate","portfolio.exposure.calculate_from_history","backtest.lightweight_role.run","monthly_review.build"]
REQUIRED_GATES = ["data_facts.valid","paper_ledger.valid","outcome_backfill.valid","backtest.report.valid"]

def test_paper_data_skills_registered():
    missing=[s for s in REQUIRED_SKILLS if s not in SHARED_SKILL_REGISTRY]
    assert not missing, f"missing: {missing}"
    print(f"✅ {len(REQUIRED_SKILLS)} data skills registered")

def test_paper_data_gates_registered():
    missing=[g for g in REQUIRED_GATES if g not in GATE_REGISTRY]
    assert not missing, f"missing: {missing}"
    print(f"✅ {len(REQUIRED_GATES)} data gates registered")

def test_paper_data_pipeline_registered():
    p=PIPELINE_REGISTRY.get("Z-PaperDataLoop")
    assert p is not None
    assert "data_facts.load_price_bars" in p.get("allowed_skills",[])
    assert "external_api_default_on" in p.get("forbidden_capabilities",[])
    print("✅ Z-PaperDataLoop pipeline registered (external_api forbidden)")

def test_paper_data_workflow_registered():
    w=WORKFLOW_DAG_REGISTRY.get("Z-PaperData.paper_outcome_loop_workflow")
    assert w is not None, "workflow not registered"
    nodes=w.get("nodes",[])
    assert "data_facts.load_price_bars" in nodes and "monthly_review.build" in nodes
    print(f"✅ Z-PaperData workflow: {len(nodes)} nodes")

def test_external_api_disabled_by_default():
    for sid in REQUIRED_SKILLS:
        sb=SHARED_SKILL_REGISTRY.get(sid,{}).get("safety_boundary","")
        assert "external API" not in sb.lower() or "no external" in sb.lower(), f"{sid}: external API mentioned"
    p=PIPELINE_REGISTRY.get("Z-PaperDataLoop",{})
    fc=p.get("forbidden_capabilities",[])
    assert "external_api_default_on" in fc
    print("✅ external API disabled by default")

def test_no_real_z9_write_declared():
    for sid in ["paper_trade.outcome_backfill.calculate"]:
        sb=SHARED_SKILL_REGISTRY.get(sid,{}).get("safety_boundary","")
        assert "no real z9 write" in sb.lower(), f"{sid}: missing no real Z9 write"
    print("✅ no real Z9 write declared")

def test_personal_quant_docs_exist():
    required=["docs/architecture/PERSONAL_QUANT_DATA_VALIDITY_LAYER_V10.md",
              "docs/contracts/DATA_FACT_LAYER_V10.md",
              "docs/contracts/PAPER_TRADE_LEDGER_V10.md",
              "docs/contracts/OUTCOME_BACKFILL_RUNNER_V10.md",
              "docs/contracts/PORTFOLIO_EXPOSURE_HISTORY_V10.md",
              "docs/contracts/LIGHTWEIGHT_BACKTEST_V10.md",
              "docs/contracts/MONTHLY_REVIEW_V10.md"]
    missing=[p for p in required if not Path(p).exists()]
    assert not missing, f"missing: {missing}"
    print(f"✅ {len(required)} docs/contracts exist")


def test_paper_data_workflow_has_dag_path():
    w=WORKFLOW_DAG_REGISTRY.get("Z-PaperData.paper_outcome_loop_workflow")
    edges=w.get("edges",[])
    g={}; [g.setdefault(a,[]).append(b) for a,b in edges]
    seen=set();s=["data_facts.load_price_bars"]
    while s:
        n=s.pop()
        if n in seen: continue
        seen.add(n)
        s.extend(g.get(n,[]))
    assert "safety.no_real_trade" in seen, "workflow not connected"
    print(f"✅ workflow DAG path connected ({len(seen)} nodes reachable)")

if __name__ == "__main__":
    test_paper_data_skills_registered(); test_paper_data_gates_registered()
    test_paper_data_pipeline_registered(); test_paper_data_workflow_registered()
    test_external_api_disabled_by_default(); test_no_real_z9_write_declared()
    test_paper_data_workflow_has_dag_path()
    test_personal_quant_docs_exist()
    print("\n🏁 Personal Quant Data Architecture — tests PASS")
