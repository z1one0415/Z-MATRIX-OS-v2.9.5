"""Dry-Run Rehearsal tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.dry_run.rehearsal_runner import build_v3_alpha_dry_run_rehearsal

def test_dry_run_builds_all_9_artifacts():
    r = build_v3_alpha_dry_run_rehearsal()
    artifacts = r.get("artifacts", {})
    expected = ["paper_ledger_event","outcome_backfill_event","memory_candidate_preview",
                "approval_request","human_approval_decision","prompt_patch_request",
                "prompt_render_preview","tail_risk_controller_preview","v3_alpha_readiness_report"]
    for key in expected:
        assert key in artifacts and artifacts[key], f"{key} missing"
    print(f"✅ all {len(expected)} artifacts built")

def test_dry_run_lineage_not_empty():
    r = build_v3_alpha_dry_run_rehearsal()
    assert len(r.get("lineage", [])) > 0
    print(f"✅ lineage has {len(r['lineage'])} steps")

def test_dry_run_does_not_append_eventstore():
    r = build_v3_alpha_dry_run_rehearsal()
    assert "stored" not in str(r.get("artifacts", {}))
    print("✅ does not append EventStore")

def test_dry_run_no_real_trade():
    r = build_v3_alpha_dry_run_rehearsal()
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    print("✅ no real trade, no broker")

def test_dry_run_runtime_disabled():
    r = build_v3_alpha_dry_run_rehearsal()
    assert r["runtime_enabled"] is False
    print("✅ runtime disabled")

if __name__ == "__main__":
    test_dry_run_builds_all_9_artifacts()
    test_dry_run_lineage_not_empty()
    test_dry_run_does_not_append_eventstore()
    test_dry_run_no_real_trade()
    test_dry_run_runtime_disabled()
    print("\n🏁 Dry-Run Rehearsal tests PASS")
