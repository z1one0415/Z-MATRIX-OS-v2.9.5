import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_labels():
    d=json.loads((W/"runtime_reports/cases/v7_forward_return_labels.json").read_text())
    assert d["label_records"]>2000
    for l in d["labels"]:
        assert l["used_as_factor_input"] is False
        assert l["exit_date"]>l["as_of_date"]
        assert l["ready_for_alpha_claim"] is False
