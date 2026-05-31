#!/usr/bin/env python3
<<<<<<< HEAD
"""Generate case_registry_v1.json from case_registry_v1.csv — fail-closed on schema errors."""
import csv
import json
from pathlib import Path

CSV_PATH = Path("data/research_db/cases/case_registry_v1.csv")
JSON_PATH = Path("data/research_db/cases/case_registry_v1.json")

with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames or []
    output = []

    for idx, row in enumerate(reader, start=2):
        if None in row:
            raise ValueError(f"CSV row width mismatch at line {idx}: None key detected (columns misaligned)")
        if set(row.keys()) != set(header):
            raise ValueError(f"CSV header mismatch at line {idx}: got {sorted(row.keys())}, expected {sorted(header)}")

=======
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
        if None in row.values():
            raise ValueError(f"CSV row {idx}: None key — columns misaligned")
>>>>>>> v4.0-batch-0-final-hardgates-scope-lock
        item = {}
        for k, v in row.items():
            if v == "TRUE": item[k] = True
            elif v == "FALSE": item[k] = False
            else: item[k] = v
        output.append(item)

<<<<<<< HEAD
JSON_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"{len(output)} cases synced with schema validation")
=======
JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"{len(output)} cases synced (schema validated)")
>>>>>>> v4.0-batch-0-final-hardgates-scope-lock
