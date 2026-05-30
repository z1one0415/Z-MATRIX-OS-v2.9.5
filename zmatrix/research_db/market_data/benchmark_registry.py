"""Phase 3-A: Benchmark Registry."""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Optional

class BenchmarkRegistry:
    def __init__(self, csv_path: Optional[str | Path] = None):
        self._by_id: dict[str, dict] = {}
        self._by_type: dict[str, list[dict]] = {}
        if csv_path: self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rec = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items()}
                self._by_id[rec["benchmark_id"]] = rec
                self._by_type.setdefault(rec.get("benchmark_type",""), []).append(rec)

    def get_benchmark(self, benchmark_id: str) -> dict | None:
        return self._by_id.get(benchmark_id)

    def list_benchmarks(self) -> list[dict]:
        return list(self._by_id.values())

    def get_default_benchmark(self, asset_type: str = "STOCK") -> str:
        defaults = {"STOCK":"CSI300","LARGE_CAP":"CSI300","MID_CAP":"CSI500","SMALL_CAP":"CSI1000","CHINEXT":"CHINEXT","STAR":"STAR50","CASH":"CASH"}
        return defaults.get(asset_type, "CSI300")
