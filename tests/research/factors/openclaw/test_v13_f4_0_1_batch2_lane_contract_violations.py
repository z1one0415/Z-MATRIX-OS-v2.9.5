"""V13.F4.0.1 — Lane violation audit tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
a = json.loads((B2 / "v13_f4_0_1_batch2_lane_contract_violation_audit.json").read_text())
def test_7_audited(): assert a.get("audited_lane_count") == 7
def test_f09_violation(): assert "F09" in a.get("source_audit_only_violations", [])
def test_no_alpha(): assert a.get("alpha_claim_allowed") is False
