"""V13.F3.0 — Subsession output contract tests."""
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]

def test_each_factor_has_output_dir():
    for fid in FACTOR_IDS:
        d = BATCH / fid
        assert d.exists(), f"Missing directory: {d}"

def test_each_factor_has_8_files():
    required = ["formula_contract", "source_readiness", "materialization",
                "pit_leakage_validation", "coverage_validation",
                "single_factor_validation", "evidence_scorecard", "closeout"]
    for fid in FACTOR_IDS:
        for suffix in required:
            p = BATCH / fid / f"{fid.lower()}_{suffix}.json"
            assert p.exists(), f"Missing: {p}"

def test_no_cross_factor_writes():
    """Verify no factor writes into another factor's directory."""
    for fid in FACTOR_IDS:
        dir_ = BATCH / fid
        for other in FACTOR_IDS:
            if other == fid:
                continue
            # Check that no file in this dir references the other factor's closeout
            for js in dir_.glob("*.json"):
                data = json.loads(js.read_text())
                if isinstance(data, dict) and data.get("factor_id") != fid:
                    assert False, f"{js} has factor_id={data['factor_id']} but is in {fid}/ directory"

def test_no_factor_writes_to_root():
    """Verify no factor writes to openclaw_batch root."""
    root_files = list(BATCH.glob("[Ff]*.json"))
    # Only orchestration/merge/audit/closeout are allowed
    allowed = ["v13_f3_0_parallel_batch_orchestration_contract.json"]
    for f in root_files:
        assert f.name in allowed or "merge" in f.name or "safety" in f.name or "closeout" in f.name, \
            f"Unexpected root file: {f.name}"

def test_f03r_not_materialized():
    p = BATCH / "F03R" / "f03r_closeout.json"
    if p.exists():
        co = json.loads(p.read_text())
        assert co.get("materialized") is False, "F03R must not be materialized"

def test_f03r_not_validated():
    p = BATCH / "F03R" / "f03r_closeout.json"
    if p.exists():
        co = json.loads(p.read_text())
        assert co.get("single_factor_validation_executed") is False, "F03R must not be validated"

def test_all_closeouts_blocked():
    for fid in FACTOR_IDS:
        p = BATCH / fid / f"{fid.lower()}_closeout.json"
        if p.exists():
            co = json.loads(p.read_text())
            assert co.get("alpha_claim_allowed") is False, f"{fid} alpha not blocked"
            assert co.get("v13_6_allowed") is False, f"{fid} v13.6 not blocked"
            assert co.get("production") == "BLOCKED", f"{fid} production not blocked"
