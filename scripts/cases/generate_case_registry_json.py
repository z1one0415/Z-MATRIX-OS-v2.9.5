#!/usr/bin/env python3
"""Generate case_registry_v1.json from case_registry_v1.csv (CSV is source of truth)."""
import csv, json
from pathlib import Path

CSV = Path("data/research_db/cases/case_registry_v1.csv")
JSON = Path("data/research_db/cases/case_registry_v1.json")

cases = list(csv.DictReader(open(CSV)))
output = []
for c in cases:
    item = {}
    for k, v in c.items():
        if k is None: continue
        if v == "TRUE": item[k] = True
        elif v == "FALSE": item[k] = False
        else: item[k] = v
    output.append(item)

JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False))
print(f"Generated {len(output)} cases from CSV → {JSON}")
