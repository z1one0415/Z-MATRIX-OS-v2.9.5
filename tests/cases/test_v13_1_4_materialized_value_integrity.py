"""V13.1.4 Value Integrity Tests — fixture-driven, production-blocked."""
import json,os,csv,subprocess
from pathlib import Path

W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
FIX=W/"tests/fixtures/v13_1_4_materialization"

def run_materializer(fd):
    env=os.environ.copy();env["V13_FIXTURE_DIR"]=str(fd)
    r=subprocess.run(["python3",str(W/"scripts/cases/materialize_v13_1_4_feature_store.py")],cwd=str(W),capture_output=True,text=True,env=env)
    return r.returncode,r.stdout,r.stderr

def run_validator(fd):
    env=os.environ.copy();env["V13_FIXTURE_DIR"]=str(fd)
    r=subprocess.run(["python3",str(W/"scripts/cases/validate_v13_1_4_materialized_feature_store.py")],cwd=str(W),capture_output=True,text=True,env=env)
    return r.returncode,r.stdout,r.stderr

def run_field_gate(fd):
    env=os.environ.copy();env["V13_FIXTURE_DIR"]=str(fd)
    r=subprocess.run(["python3",str(W/"scripts/cases/rerun_v13_1_4_field_gate_after_materialization.py")],cwd=str(W),capture_output=True,text=True,env=env)
    return r.returncode

def pfx(fd):return Path(fd).name+"_"

# ── 1. Positive fixture ──
def test_positive_fixture_materializes():
    rc,out,err=run_materializer(FIX/"positive")
    assert"MATERIALIZED"in out,f"Not BUILT: {out}"

def test_positive_fixture_per_feature_group_status():
    run_materializer(FIX/"positive")
    m=json.load(open(C/f"fixtures/{pfx(FIX/'positive')}feature_store_manifest.json"))
    assert"per_feature_group_materialization_status"in m

def test_positive_fixture_per_candidate_feature_status():
    run_materializer(FIX/"positive")
    m=json.load(open(C/f"fixtures/{pfx(FIX/'positive')}feature_store_manifest.json"))
    assert"per_candidate_feature_status"in m

def test_positive_fixture_validator_per_candidate():
    run_materializer(FIX/"positive");run_validator(FIX/"positive")
    v=json.load(open(C/f"fixtures/{pfx(FIX/'positive')}feature_store_validation.json"))
    assert"per_candidate_validation_status"in v
    assert v.get("candidate_ready_after_materialization_count",0)>=4

# ── 5-8. Negative fixtures ──
def test_empty_values_fixture_blocked():
    rc,out,err=run_materializer(FIX/"empty_values")
    assert"BLOCKED"in out

def test_non_numeric_fixture_blocked():
    rc,out,err=run_materializer(FIX/"non_numeric")
    assert"BLOCKED"in out

def test_insufficient_coverage_fixture_blocked():
    rc,out,err=run_materializer(FIX/"insufficient_coverage")
    assert"BLOCKED"in out

def test_rank_future_label_fixture_blocked():
    rc,out,err=run_materializer(FIX/"rank_future_label_leakage")
    assert"BLOCKED"in out

# ── 9. Field gate source ──
def test_field_gate_uses_validator_per_candidate():
    run_materializer(FIX/"positive");run_validator(FIX/"positive");run_field_gate(FIX/"positive")
    fg=json.load(open(C/f"fixtures/{pfx(FIX/'positive')}candidate_field_availability_after_materialization.json"))
    assert"per_candidate_validation_status"in (fg.get("field_gate_source","")),"Wrong field_gate_source"

# ── 10. Field gate NOT using manifest.columns ──
def test_field_gate_not_use_feature_columns_built():
    src=(W/"scripts/cases/rerun_v13_1_4_field_gate_after_materialization.py").read_text()
    assert"feature_columns_built"not in src

# ── 11. Production still blocked ──
def test_production_runtime_still_blocked():
    r=subprocess.run(["python3",str(W/"scripts/cases/build_v13_1_4_feature_materialization_contract.py")],cwd=str(W),capture_output=True,text=True)
    assert"BLOCKED"in r.stdout

def test_v13_2_never_executed():
    src=(W/"scripts/cases/build_v13_1_4_feature_materialization_closeout.py").read_text()
    assert"v13_2_executed"not in src

# ── Source sha256 check ──
def test_no_multiple_sha256():
    src=(W/"scripts/cases/materialize_v13_1_4_feature_store.py").read_text()
    for p in['source_sha256 = "MULTIPLE"','source_sha256 = "UNKNOWN"']:assert p not in src
