"""V13.F4.0 — Subsession contracts tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
s = json.loads((B2 / "v13_f4_0_batch2_subsession_contracts.json").read_text())
def test_7_subsessions(): assert len(s.get("subsession_contracts", [])) == 7
def test_lane_a_f05(): c = [c for c in s["subsession_contracts"] if c["lane_id"]=="A"]; assert c and c[0]["factor_id"]=="F05"
def test_lane_c_audit(): c = [c for c in s["subsession_contracts"] if c["lane_id"]=="C"]; assert c and c[0]["lane_type"]=="SOURCE_AUDIT_ONLY"
def test_lane_g_audit(): c = [c for c in s["subsession_contracts"] if c["lane_id"]=="G"]; assert c and c[0]["lane_type"]=="SOURCE_AUDIT_ONLY"
def test_no_forbidden_in_allowed(): 
    for c in s["subsession_contracts"]:
        if c["lane_type"] == "SOURCE_AUDIT_ONLY":
            assert "materialization" not in c.get("allowed_actions", [])
def test_no_alpha(): assert s.get("alpha_claim_allowed") is False
