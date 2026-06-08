"""V13.F4.0.1 — Recomputed closeout tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
for fid in ["F02","F05","F14","F15","F16"]:
    globals()[f"test_{fid.lower()}_exists"] = lambda fid=fid: _test_rc_exists(fid)
for fid in ["F09"]:
    globals()[f"test_{fid.lower()}_exists"] = lambda fid=fid: _test_rc_exists(fid)

def _test_rc_exists(fid):
    p = B2 / fid / f"{fid.lower()}_closeout_recomputed.json"
    assert p.exists(), f"Missing: {p}"

def test_f02_pass():
    co = json.loads((B2 / "F02" / "f02_closeout_recomputed.json").read_text())
    assert co.get("evidence_score") == "PASS_RESEARCH_EVIDENCE"

def test_f05_pass():
    co = json.loads((B2 / "F05" / "f05_closeout_recomputed.json").read_text())
    assert co.get("evidence_score") == "PASS_RESEARCH_EVIDENCE"

def test_f09_violated():
    co = json.loads((B2 / "F09" / "f09_closeout_recomputed.json").read_text())
    assert "CONTRACT_VIOLATED" in co.get("evidence_score", "")

def test_f09_not_ready():
    co = json.loads((B2 / "F09" / "f09_closeout_recomputed.json").read_text())
    assert co.get("ready_for_candidate_review") is False

def test_no_coverage_fail_pass():
    for fid in ["F02","F05","F14","F15","F16"]:
        co = json.loads((B2 / fid / f"{fid.lower()}_closeout_recomputed.json").read_text())
        assert not (co.get("coverage_passed") is False and co.get("evidence_score") == "PASS_RESEARCH_EVIDENCE")

def test_no_alpha():
    for fid in ["F02","F05","F14","F15","F16","F09"]:
        co = json.loads((B2 / fid / f"{fid.lower()}_closeout_recomputed.json").read_text())
        assert co.get("alpha_claim_allowed") is False
