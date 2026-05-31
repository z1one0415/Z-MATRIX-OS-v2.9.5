#!/usr/bin/env python3
"""V7-E: V8 entry gate."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
d=json.loads((W/"runtime_reports/cases/v8_expanded_sample_entry_gate.json").read_text())
print(f"V8: {d["status"]} | ready={d["ready_for_v8_expanded_sample"]}")
