#!/usr/bin/env python3
"""Generate case_registry_v1.json from case_registry_v1.csv (CSV is source of truth).
Fails closed on schema errors — no silent None key swallowing."""
import csv, json, sys
from pathlib import Path

CSV = Path("data/research_db/cases/case_registry_v1.csv")
JSON = Path("data/research_db/cases/case_registry_v1.json")

cases = list(csv.DictReader(open(CSV)))
header = open(CSV).readline().strip().split(",")
row_lines = open(CSV).readlines()

# FAIL_CLOSED checks
for i, line in enumerate(row_lines):
    cols = line.strip().split(",")
    if len(cols) != len(header):
        raise ValueError(f"CSV row {i} width mismatch: {len(cols)} vs header {len(header)}")

for i, c in enumerate(cases):
    if None in c.values():
        raise ValueError(f"CSV row {i} has None value in DictReader: keys may be misaligned")

output = []
for c in cases:
    j = {}
    for k, v in c.items():
        if v == "TRUE": j[k] = True
        elif v == "FALSE": j[k] = False
        else: j[k] = v
    output.append(j)

JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False))
print(f"Generated {len(output)} cases from CSV → {JSON} (schema validated)")
