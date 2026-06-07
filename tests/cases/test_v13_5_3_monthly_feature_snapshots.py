"""V13.5.3 Monthly Feature Snapshots — targeted tests."""
import json,csv;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
m=L("v13_5_3_monthly_feature_snapshots_manifest.json")
def test_exists():assert m
def test_csv_exists():
    if"BUILT"in m.get("status",""):
        assert(Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"/"v13_5_3_monthly_feature_snapshots.csv").exists()
def test_feature_real():assert m.get("feature_side_real_only")is True
def test_known_at_pass():assert m.get("known_at_pass")is True
def test_future_leakage():assert m.get("future_leakage_check_pass")is True
def test_no_forbidden_labels():assert m.get("forbidden_label_columns_present")is False
def test_usable_ge_24():
    if"BUILT"in m.get("status",""):assert m.get("usable_rebalance_date_count",0)>=24
def test_alpha_false():assert m.get("alpha_claim_allowed")is False
def test_prod_blocked():
    for k in["production","broker_runtime","real_trade"]:assert m.get(k)=="BLOCKED"
