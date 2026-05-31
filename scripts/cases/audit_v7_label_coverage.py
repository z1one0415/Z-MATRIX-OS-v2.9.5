#!/usr/bin/env python3
"""V7-C: Audit label coverage."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
d=json.loads((C/"v7_forward_return_labels.json").read_text())
for h in d["horizons"]:
    cnt=sum(1 for l in d["labels"] if l["horizon"]==h)
    print(f"{h}: {cnt} labels")
