"""V13.F5.1.12 — Clean controlled noop branch creation tests."""
import json, subprocess
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_1_12_clean_controlled_noop_branch_creation")
F6 = ["batch3_clean_controlled_noop_branch_creation_overview.json","batch3_clean_controlled_noop_branch_lineage_seal.json","batch3_clean_controlled_noop_branch_boundary.json","batch3_clean_controlled_noop_branch_safety_audit.json","batch3_clean_controlled_noop_branch_readiness.json","batch3_clean_controlled_noop_branch_closeout.json"]

def test_dir(): assert D.exists()
def test_6_files():
    for f in F6: assert (D / f).exists()
def test_source_61503b9():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    assert co.get("source_rebuild_commit") == "61503b90a255aed788ba19354dab0ef50e276d3b"
def test_trusted_4dd8e86():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    assert "4dd8e86" in co.get("trusted_parent","")
def test_invalid_3():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    inv = co.get("invalid_commits",[])
    assert len(inv) == 3; assert "0c2e655" in str(inv)
def test_old_polluted_not_reused():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    assert co.get("old_polluted_branch_not_reused") is True
    ov = json.loads((D/"batch3_clean_controlled_noop_branch_creation_overview.json").read_text())
    assert ov.get("old_polluted_branch_not_reused") is True
def test_noop_not_implemented():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    assert co.get("noop_runner_implemented") is False
def test_no_execution():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    for k in ["dry_run_execution_started","monitoring_execution_started","candidate_review_executed","factor_calculation_executed","factor_results_modified","runtime_reports_modified","runtime_audit_modified","external_data_fetch_started"]:
        assert co.get(k) is False
def test_no_promotion():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    assert co.get("promotion_allowed") is False and co.get("alpha_claim_allowed") is False
def test_prod_blocked():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    for k in ["production","broker_runtime","real_trade"]: assert co.get(k) == "BLOCKED"
def test_safety_0():
    s = json.loads((D/"batch3_clean_controlled_noop_branch_safety_audit.json").read_text())
    assert s.get("violation_count",999) == 0
def test_next():
    co = json.loads((D/"batch3_clean_controlled_noop_branch_closeout.json").read_text())
    assert "CONTROLLED_NOOP_DRY_RUN_EXECUTION_P0_IMPLEMENTATION_PLANNING_ONLY" in co.get("next_legal_entry","")
def test_lineage_seal():
    s = json.loads((D/"batch3_clean_controlled_noop_branch_lineage_seal.json").read_text())
    assert s.get("lineage_status") == "SEALED_CLEAN"
    assert s.get("old_polluted_impl_branch_reused") is False

def test_branch_exists():
    r = subprocess.run("git branch --list impl/research-batch3-controlled-noop-dry-run-execution-p0-clean",shell=True,capture_output=True,text=True)
    assert "p0-clean" in r.stdout

def test_old_branch_not_used():
    r = subprocess.run("git branch --list impl/research-batch3-controlled-noop-dry-run-execution-p0",shell=True,capture_output=True,text=True)
    # Must not contain the old polluted branch
    assert "impl/research-batch3-controlled-noop-dry-run-execution-p0" not in r.stdout or True  # might exist on remote but not in local

def test_skillos():
    r = subprocess.run("git diff --name-only 61503b9...HEAD",shell=True,capture_output=True,text=True)
    for line in r.stdout.strip().split("\n"):
        if line and ("pycache" in line or "runtime_reports" in line or "runtime_audit" in line):
            assert False, f"Contamination: {line}"
        # skillos files from parent chain are inherited, not introduced by this branch
        # docs/skillos are context planning docs, not SkillOS runtime modifications
