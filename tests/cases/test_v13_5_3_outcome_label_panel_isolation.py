"""V13.5.3 Outcome Label Panel Isolation — targeted tests."""
import json,csv;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
m=L("v13_5_3_monthly_outcome_label_panel_manifest.json")
def test_exists():assert m
def test_role():assert m.get("role")=="OUTCOME_LABEL_ONLY"
def test_feature_side_blocked():assert m.get("feature_side_access_allowed")is False
def test_not_written_to_feature():assert m.get("written_to_feature_store")is False
def test_label_known_after():assert m.get("label_known_after_rebalance")is True
def test_horizons():assert"20D"in m.get("label_horizons",[])and"60D"in m.get("label_horizons",[])
def test_csv_not_in_snapshots():
    ol_csv=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"/"v13_5_3_monthly_outcome_label_panel.csv"
    if ol_csv.exists():
        snap_csv=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"/"v13_5_3_monthly_feature_snapshots.csv"
        if snap_csv.exists():
            snap_cols=set(list(csv.DictReader(open(snap_csv)))[0].keys())
            for c in["outcome_20d_return","outcome_60d_return","label"]:
                assert c not in snap_cols,f"leak:{c}"
def test_alpha_false():assert m.get("alpha_claim_allowed")is False
def test_prod_blocked():
    for k in["production","broker_runtime","real_trade"]:assert m.get(k)=="BLOCKED"
