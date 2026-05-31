import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v9_formal_factor_stability.json").read_text())
    assert d["total_metrics"]>=50
    assert d["alpha_validated"] is False
    for m in d["metrics"][:30]:
        if m["sample_sufficient"]:
            assert m["average_cross_section_size"]>=30
