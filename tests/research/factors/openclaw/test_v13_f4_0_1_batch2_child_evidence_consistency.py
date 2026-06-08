"""V13.F4.0.1 — Child consistency audit tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
a = json.loads((B2 / "v13_f4_0_1_batch2_child_evidence_consistency_audit.json").read_text())
def test_6_audited(): assert a.get("audited_factor_count") == 6
def test_f02_inconsistent(): p = [p for p in a.get("per_factor",[]) if p["factor_id"]=="F02"]; assert p and p[0]["claim_consistent_with_artifacts"] is False
def test_f05_inconsistent(): p = [p for p in a.get("per_factor",[]) if p["factor_id"]=="F05"]; assert p and p[0]["claim_consistent_with_artifacts"] is False
def test_f09_violation(): p = [p for p in a.get("per_factor",[]) if p["factor_id"]=="F09"]; assert p and p[0]["recomputed_evidence_score"]=="SOURCE_AUDIT_CONTRACT_VIOLATED"
def test_f09_not_ready(): p = [p for p in a.get("per_factor",[]) if p["factor_id"]=="F09"]; assert p and p[0]["ready_for_candidate_review"] is False
def test_no_alpha(): assert a.get("alpha_claim_allowed") is False
