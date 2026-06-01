import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_stability():
    d=json.loads((W/"runtime_reports/cases/v9_formal_factor_stability.json").read_text())
    assert d["status"]=="V9_FORMAL_FACTOR_STABILITY_BUILT"
    assert d["factor_count"]==16
    assert d["horizon_count"]==5
    assert d["factor_horizon_count"]>=70
    assert d["validation_type"].startswith("FORMAL")
    assert d["min_cross_section_size_required"]==30
    assert d["min_valid_date_count_required"]==250
    assert d["alpha_validated"] is False
    for m in d["metrics"][:40]:
        assert "valid_date_count" in m
        assert "average_cross_section_size" in m
        assert "formal_sample_status" in m
        assert "median_ic" in m
        assert "rankic_ir" in m
        assert m["alpha_validated"] is False
