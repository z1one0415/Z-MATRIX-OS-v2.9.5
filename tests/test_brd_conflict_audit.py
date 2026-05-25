"""BRD Conflict Audit tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.stock_role_classifier import classify_stock_role
from zmatrix.investment.d_matrix import evaluate_d_matrix
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY


def test_d_matrix_cannot_convert_to_base():
    r = evaluate_d_matrix("002472")
    assert r.get("cannot_convert_to_base") is True
    print("✅ D-Matrix: cannot_convert_to_base=True")


def test_b_pass_gives_a():
    r = classify_stock_role("002472", {"status":"PASS","base_role_eligible":True}, {"status":"DEGRADED","r_action_cap":"WAIT"}, {"status":"DEGRADED","short_event_eligible":False})
    assert r["role"] == "A_LONG_CORE"
    print("✅ B alone → A_LONG_CORE")


def test_d_alone_gives_c():
    r = classify_stock_role("002472", {"status":"DEGRADED","base_role_eligible":False}, {"status":"DEGRADED","r_action_cap":"WAIT"}, {"status":"PASS","short_event_eligible":True})
    assert r["role"] == "C_SHORT_EVENT"
    print("✅ D alone → C_SHORT_EVENT")


def test_b_plus_d_gives_watch_only():
    r = classify_stock_role("002472", {"status":"PASS","base_role_eligible":True}, {"status":"DEGRADED","r_action_cap":"WAIT"}, {"status":"PASS","short_event_eligible":True})
    assert r["role"] == "WATCH_ONLY", f"expected WATCH_ONLY, got {r['role']}"
    assert "MULTI_MATRIX_CONFLICT" in str(r["downgrade_reasons"])
    print("✅ B+D conflict → WATCH_ONLY")


def test_g18_workflow_has_role_review():
    w = WORKFLOW_DAG_REGISTRY.get("Z-G18.paper_z9_preview_workflow")
    assert w is not None
    nodes = w.get("nodes", [])
    assert "investment.role_review.build" in nodes
    assert "investment.role_review.required" in w.get("required_gates", [])
    print("✅ G18: investment.role_review required in workflow")



def test_g18_role_review_has_path_to_paper_record():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY["Z-G18.paper_z9_preview_workflow"]
    edges = w["edges"]
    def has_path(source, target):
        graph = {}
        for a, b in edges: graph.setdefault(a, []).append(b)
        seen = set(); stack = [source]
        while stack:
            node = stack.pop()
            if node == target: return True
            if node in seen: continue
            seen.add(node); stack.extend(graph.get(node, []))
        return False
    assert has_path("investment.role_review.build", "paper.record")
    print("✅ G18 role review has DAG path to paper.record")

def test_investment_review_pipeline_has_gates():
    p = PIPELINE_REGISTRY.get("Z-InvestmentRoleReview")
    assert p is not None
    gates = p.get("required_gates", [])
    for g in ["account.constitution.valid","z8.position_control.valid","human.final_override.required"]:
        assert g in gates, f"missing {g}"
    print("✅ Z-InvestmentRoleReview: account/z8/g17 gates present")


if __name__ == "__main__":
    test_d_matrix_cannot_convert_to_base()
    test_b_pass_gives_a(); test_d_alone_gives_c(); test_b_plus_d_gives_watch_only()
    test_g18_workflow_has_role_review()
    test_g18_role_review_has_path_to_paper_record()
    test_investment_review_pipeline_has_gates()
    print("\n🏁 BRD Conflict Audit — tests PASS")
