"""V13.F2.3 — Stage E: bucket validation tests."""
import json, csv
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

bucket = L("v13_f2_3_single_factor_bucket_validation.json")

def test_bucket_validated():
    assert bucket.get("bucket_validation_executed") is True

def test_validated_factors():
    assert "F03" in bucket.get("validated_factors", [])
    assert "F06" in bucket.get("validated_factors", [])

def test_bucket_count():
    assert bucket.get("bucket_count") == 3

def test_bucket_labels():
    assert bucket.get("bucket_labels") == ["LOW", "MID", "HIGH"]

def test_per_factor_count():
    assert len(bucket.get("per_factor_bucket_evidence", [])) == 2

def test_f03_bucket():
    f03 = next((f for f in bucket.get("per_factor_bucket_evidence", []) if f["factor_id"] == "F03"), None)
    assert f03 is not None
    assert f03.get("bucket_validation_executed") is True
    assert isinstance(f03.get("high_low_spread_20d"), (int, float))

def test_f06_bucket():
    f06 = next((f for f in bucket.get("per_factor_bucket_evidence", []) if f["factor_id"] == "F06"), None)
    assert f06 is not None
    assert f06.get("bucket_validation_executed") is True

def test_f03_cost_adjusted():
    f03 = next((f for f in bucket.get("per_factor_bucket_evidence", []) if f["factor_id"] == "F03"), None)
    assert isinstance(f03.get("cost_adjusted_high_low_spread_20d"), (int, float))
    assert isinstance(f03.get("cost_adjusted_high_low_spread_60d"), (int, float))

def test_f03_monotonicity():
    f03 = next((f for f in bucket.get("per_factor_bucket_evidence", []) if f["factor_id"] == "F03"), None)
    assert 0 <= f03.get("bucket_monotonicity_20d_rate", -1) <= 1

def test_bucket_assignments_csv():
    p = RUNTIME_FACTORS / "v13_f2_3_single_factor_bucket_assignments.csv"
    assert p.exists()
    with open(p) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) > 0
        assert "bucket" in (reader.fieldnames or [])

def test_no_buy_sell():
    p = RUNTIME_FACTORS / "v13_f2_3_single_factor_bucket_assignments.csv"
    with open(p) as f:
        reader = csv.DictReader(f)
        for h in (reader.fieldnames or []):
            assert h.lower() not in ("buy", "sell", "trade", "position")

def test_multi_composite_false():
    assert bucket.get("multi_factor_composite_built") is False

def test_alpha_false():
    assert bucket.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert bucket.get("production") == "BLOCKED"
