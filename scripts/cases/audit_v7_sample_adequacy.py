#!/usr/bin/env python3
"""V7-C: Sample adequacy audit."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
d=json.loads((W/"runtime_reports/cases/v7_sample_adequacy_audit.json").read_text())
for h,s in d["horizon_status"].items(): print(f"{h}: {s}")
