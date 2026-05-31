#!/usr/bin/env python3
"""V6-C Coverage audit: count valid factor values vs expected."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
data=json.loads((W/"runtime_reports/cases/v6b_price_only_factor_values.json").read_text())
fids=[k for r in data["records"] for k in r["factor_values"]]
print(f"Coverage: {len(fids)} factor values across {len(data['records'])} records")
