"""V13.F4.0 — Batch 2 contract tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
c = json.loads((B2 / "v13_f4_0_batch2_orchestration_contract.json").read_text())
def test_frozen_preserved(): assert c.get("frozen_candidates_preserved") == ["F04","F10","F11"]
def test_no_frozen_mutation(): assert c.get("frozen_candidate_mutation_allowed") is False
def test_no_f3_5_1(): assert c.get("f3_5_1_monitoring_execution_allowed") is False
def test_no_f3_6(): assert c.get("f3_6_true_oos_validation_allowed") is False
def test_no_composite(): assert c.get("multi_factor_composite_allowed") is False
def test_no_alpha(): assert c.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
