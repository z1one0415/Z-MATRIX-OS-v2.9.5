"""V13.5.3 Monthly Bucket Assignments — targeted tests."""
import json,csv;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
m=L("v13_5_3_monthly_bucket_assignments_manifest.json")
csv_f=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"/"v13_5_3_monthly_bucket_assignments.csv"
rows=list(csv.DictReader(open(csv_f)))if csv_f.exists()else[]
def test_exists():assert m
def test_csv_exists():
    if"BUILT"in m.get("status",""):assert csv_f.exists()
def test_bucket_values():
    if rows:
        bkts=set(r["mechanics_bucket"] for r in rows)
        for b in bkts:assert b in("LOW","MID","HIGH","UNASSIGNED"),f"bad:{b}"
def test_source_mode():
    if rows:assert all(r["source_mode"]=="REAL_HISTORICAL_FEATURES_ONLY"for r in rows)
def test_gen_method():
    if rows:assert all(r["generation_method"]=="V13_5_3_MONTHLY_REBALANCE_MECHANICS_BUCKET"for r in rows)
def test_no_outcome_cols():
    if rows:
        cols=set(rows[0].keys())
        forbidden=["forward_return","future_label","t20_return","t60_return","bucket_return","bucket_spread","hit_count","miss_count","alpha_label","trade_signal"]
        for fb in forbidden:assert not any(fb in c.lower()for c in cols),f"forbidden:{fb}"
def test_not_single_date():assert len(set(r["rebalance_date"]for r in rows))>1
def test_balance():
    if"BUILT"in m.get("status",""):assert m.get("monthly_bucket_balance_pass")is True
def test_alpha_false():assert m.get("alpha_claim_allowed")is False
def test_prod_blocked():
    for k in["production","broker_runtime","real_trade"]:assert m.get(k)=="BLOCKED"
