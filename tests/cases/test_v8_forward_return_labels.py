import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v8_forward_return_labels.json").read_text())
    assert d["label_records"]>50000
    assert d["stock_count"]>=60
    for l in d["labels"][:100]:
        assert l["exit_date"]>l["as_of_date"]
        assert l["used_as_factor_input"] is False
