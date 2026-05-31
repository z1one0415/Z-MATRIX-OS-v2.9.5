#!/usr/bin/env python3
"""Generate sha256 hash for a market data CSV file."""
import sys, json, hashlib, csv, io
from pathlib import Path

def compute_source_hash(csv_path, exclude_cols=("source_hash",)):
    content = Path(csv_path).read_text()
    reader = csv.DictReader(io.StringIO(content))
    rows_sorted = []
    for row in reader:
        clean = {k: v for k, v in row.items() if k not in exclude_cols}
        rows_sorted.append(json.dumps(clean, sort_keys=True))
    rows_sorted.sort()
    h = hashlib.sha256("\n".join(rows_sorted).encode()).hexdigest()
    return h, len(rows_sorted)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_market_data_source_hash.py <csv_path>")
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print("File not found:", path)
        sys.exit(1)
    h, rows = compute_source_hash(str(path))
    rel = str(path.resolve().relative_to(Path.cwd())) if path.is_absolute() else str(path)
    print("sha256:", h)
    print("rows:", rows)
    print("file:", rel)
