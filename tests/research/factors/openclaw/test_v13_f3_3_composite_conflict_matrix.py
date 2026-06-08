"""V13.F3.3 — Conflict matrix tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
m = json.loads((B / "v13_f3_3_composite_conflict_matrix.json").read_text())
def test_3_pairs(): assert len(m.get("pairwise_conflicts", [])) == 3
def test_f04f10(): p = [p for p in m["pairwise_conflicts"] if "F04" in p["pair"] and "F10" in p["pair"]]; assert p
def test_f04f11(): p = [p for p in m["pairwise_conflicts"] if "F04" in p["pair"] and "F11" in p["pair"]]; assert p
def test_f10f11(): p = [p for p in m["pairwise_conflicts"] if "F10" in p["pair"] and "F11" in p["pair"]]; assert p
def test_no_exec(): assert m.get("composite_execution_allowed") is False
def test_no_weight(): assert m.get("weight_optimization_allowed") is False
def test_no_alpha(): assert m.get("alpha_claim_allowed") is False
