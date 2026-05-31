import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_summary():
    d=json.loads((W/"runtime_reports/cases/v8_forward_return_labels_summary.json").read_text())
    assert d["label_records"]>=50000
    assert d["committed_to_git"] is False
