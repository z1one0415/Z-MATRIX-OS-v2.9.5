"""V13.F2.3 — Stage C: label isolation validation tests."""
import csv, json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

iso = L("v13_f2_3_outcome_label_isolation_validation.json")

def test_isolation_validation_executed():
    assert "isolation" in iso.get("status", "").lower()

def test_label_isolation_passed():
    # This will pass if the label panel is properly isolated from factor panels
    assert iso.get("label_isolation_passed") is True

def test_no_feature_panel_write():
    assert iso.get("feature_panel_write_detected") is False

def test_no_outcome_labels_in_factor_panels():
    assert iso.get("factor_panels_contain_outcome_labels") is False

def test_label_role_valid():
    assert iso.get("label_role_valid") is True

def test_label_known_after_rebalance():
    assert iso.get("label_known_after_rebalance") is True

def test_no_blocked_reasons():
    assert len(iso.get("blocked_reasons", [])) == 0

def test_alpha_false():
    assert iso.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert iso.get("production") == "BLOCKED"

def test_factor_panels_clean():
    """Verify F03/F06 panels don't contain forward_return columns."""
    forbidden = ["forward_return_20d", "forward_return_60d", "future_return", "target_return"]
    for fname in ["f03_industry_relative_strength_panel.csv", "f06_fundamental_quality_panel.csv"]:
        fpath = RUNTIME_FACTORS / fname
        assert fpath.exists()
        with open(fpath) as f:
            reader = csv.DictReader(f)
            for h in (reader.fieldnames or []):
                assert h not in forbidden, f"{fname} contains forbidden column: {h}"
