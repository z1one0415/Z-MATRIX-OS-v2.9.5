"""BRD Architecture Integration tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
from zmatrix.architecture.gate_registry import GATE_REGISTRY
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY

def _has_path(edges, source, target):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
    seen = set(); stack = [source]
    while stack:
        node = stack.pop()
        if node == target: return True
        if node in seen: continue
        seen.add(node)
        stack.extend(graph.get(node, []))
    return False


REQUIRED_SKILLS = ["chain_force.evaluate_10x5","sector_stage.detect","financial.health_gate","b_matrix.evaluate_base","r_matrix.evaluate_cycle","d_matrix.evaluate_event","stock_role.classify","account.constitution.check","portfolio.exposure.analyze","z8.position_control","pre_trade.checklist.validate","g17.manual_veto.preview","investment.role_review.build"]

REQUIRED_GATES = ["chain_force.valid","sector_stage.valid","financial.health_valid","b_matrix.base_valid","r_matrix.cycle_valid","d_matrix.event_valid","stock_role.classification_valid","account.constitution.valid","portfolio.exposure.valid","z8.position_control.valid","pre_trade.checklist.complete","human.final_override.required","investment.role_review.required"]


def test_all_7_layer_skills_registered():
    missing = [s for s in REQUIRED_SKILLS if s not in SHARED_SKILL_REGISTRY]
    assert not missing, f"missing skills: {missing}"
    print(f"✅ BRD: {len(REQUIRED_SKILLS)} skills registered")


def test_all_7_layer_gates_registered():
    missing = [g for g in REQUIRED_GATES if g not in GATE_REGISTRY]
    assert not missing, f"missing gates: {missing}"
    print(f"✅ BRD: {len(REQUIRED_GATES)} gates registered")


def test_z_g18_cannot_bypass_investment_role_review():
    p = PIPELINE_REGISTRY.get("Z-G18")
    assert p is not None
    assert "investment.role_review.required" in p.get("required_gates", []), "Z-G18 missing investment.role_review.required gate"
    print("✅ Z-G18: investment.role_review.required gate present")


def test_z_investment_role_review_pipeline_registered():
    p = PIPELINE_REGISTRY.get("Z-InvestmentRoleReview")
    assert p is not None
    for s in REQUIRED_SKILLS:
        assert s in p.get("allowed_skills", []), f"missing skill: {s}"
    print(f"✅ Z-InvestmentRoleReview: pipeline with {len(p['allowed_skills'])} skills")


def test_workflow_contains_role_review_before_paper():
    w = WORKFLOW_DAG_REGISTRY.get("Z-G18.paper_z9_preview_workflow")
    assert w is not None
    nodes = w.get("nodes", []); edges = w.get("edges", [])
    assert "investment.role_review.build" in nodes
    assert "paper.record" in nodes
    assert "r_matrix.evaluate_cycle" in nodes
    assert ["investment.role_review.build", "r_matrix.evaluate_cycle"] in edges, "missing review→r_matrix edge"
    assert _has_path(edges, "investment.role_review.build", "paper.record"), "role_review has no DAG path to paper.record"
    assert "investment.role_review.required" in w.get("required_gates", [])
    print("✅ Z-G18 workflow: role_review → r_matrix edge + DAG path to paper.record")


def test_z_g18_allowed_skills_include_role_review():
    p = PIPELINE_REGISTRY.get("Z-G18")
    assert p is not None
    assert "investment.role_review.build" in p.get("allowed_skills", [])
    assert "investment.role_review.required" in p.get("required_gates", [])
    print("✅ Z-G18: allowed_skills + required_gates include role_review")


def test_rmatrix_workflow_does_not_embed_investment_role_review():
    w = WORKFLOW_DAG_REGISTRY.get("RMatrix.cycle_validation_workflow")
    assert w is not None
    assert "investment.role_review.build" not in w.get("nodes", [])
    print("✅ RMatrix workflow: no investment.role_review.build (single responsibility)")


def test_g17_registered_and_required():
    p = PIPELINE_REGISTRY.get("Z-InvestmentRoleReview")
    assert "g17.manual_veto.preview" in p.get("allowed_skills", [])
    assert "human.final_override.required" in p.get("required_gates", [])
    print("✅ G17: registered + required in Z-InvestmentRoleReview")


if __name__ == "__main__":
    test_all_7_layer_skills_registered(); test_all_7_layer_gates_registered()
    test_z_g18_cannot_bypass_investment_role_review()
    test_z_investment_role_review_pipeline_registered()
    test_workflow_contains_role_review_before_paper()
    test_z_g18_allowed_skills_include_role_review()
    test_rmatrix_workflow_does_not_embed_investment_role_review()
    test_z_g18_allowed_skills_include_role_review()
    test_g17_registered_and_required()
    print("\n🏁 BRD Architecture Integration — tests PASS")
