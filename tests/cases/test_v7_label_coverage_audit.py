import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_coverage():
    d=json.loads((W/"runtime_reports/cases/v7_forward_return_labels.json").read_text())
    for h in ["T1","T5","T10"]:
        cnt=sum(1 for l in d["labels"] if l["horizon"]==h)
        assert cnt>500,f"{h}: only {cnt} labels"
