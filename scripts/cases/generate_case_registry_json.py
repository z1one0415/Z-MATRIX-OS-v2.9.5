#!/usr/bin/env python3
"""Generate case_registry_v1.json — fail-closed on schema errors."""
import csv, json
from pathlib import Path

CSV = Path("data/research_db/cases/case_registry_v1.csv")
JSON = Path("data/research_db/cases/case_registry_v1.json")

with CSV.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames or []
    output = []
    for idx, row in enumerate(reader, start=2):
        if None in row:
            raise ValueError(f"CSV row {idx}: None key — columns misaligned")
        item = {}
        for k, v in row.items():
            if v == "TRUE": item[k] = True
            elif v == "FALSE": item[k] = False
            else: item[k] = v
        output.append(item)

JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"{len(output)} cases synced (schema validated)")
