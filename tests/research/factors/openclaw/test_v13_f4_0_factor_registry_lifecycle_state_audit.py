"""V13.F4.0 — Registry audit tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
a = json.loads((B2 / "v13_f4_0_factor_registry_lifecycle_state_audit.json").read_text())
def test_20_registered(): assert a.get("registered_factor_count") == 20
def test_frozen(): assert a.get("frozen_candidates") == ["F04","F10","F11"]
def test_rejected(): assert "F03" in a.get("rejected_factors", [])
def test_batch2_candidates(): assert len(a.get("ready_for_batch2_selection_candidates", [])) > 0
def test_source_audit(): assert a.get("source_audit_only_candidates")  # non-empty
def test_no_alpha(): assert a.get("alpha_claim_allowed") is False
