from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

from zmatrix.research_db.master_data import SectorMapping


class SectorMapper:
    def __init__(self, csv_path: Optional[str | Path] = None) -> None:
        self._by_ticker: dict[str, list[SectorMapping]] = {}
        self._by_sector_id: dict[str, list[SectorMapping]] = {}
        self._by_sector_name: dict[str, list[SectorMapping]] = {}
        self._all: list[SectorMapping] = []
        if csv_path is not None:
            self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path) -> None:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sm = SectorMapping(
                    ticker=row["ticker"].strip(),
                    sector_id=row["sector_id"].strip(),
                    sector_name=row["sector_name"].strip(),
                    weight=float(row["weight"]),
                )
                self._by_ticker.setdefault(sm.ticker, []).append(sm)
                self._by_sector_id.setdefault(sm.sector_id, []).append(sm)
                self._by_sector_name.setdefault(sm.sector_name, []).append(sm)
                self._all.append(sm)

    def get_sectors(self, ticker: str) -> list[dict]:
        mappings = self._by_ticker.get(ticker, [])
        return [
            {
                "ticker": sm.ticker,
                "sector_id": sm.sector_id,
                "sector_name": sm.sector_name,
                "weight": sm.weight,
            }
            for sm in mappings
        ]

    def get_tickers_in_sector(self, sector_id: str) -> list[str]:
        mappings = self._by_sector_id.get(sector_id, [])
        return [sm.ticker for sm in mappings]

    def list_sectors(self) -> list[str]:
        return sorted(self._by_sector_id.keys())

    def detect_speculative_theme(self, ticker: str) -> bool:
        SPECULATIVE_KEYWORDS = ("概念", "题材", "ST", "壳", "妖", "科创板")
        mappings = self._by_ticker.get(ticker, [])
        for sm in mappings:
            if any(kw in sm.sector_name for kw in SPECULATIVE_KEYWORDS):
                return True
            if sm.sector_id.startswith("SW80") and sm.weight < 0.3:
                return True
        return False

    def detect_missing_sector(self, ticker: str) -> bool:
        return ticker not in self._by_ticker or len(self._by_ticker[ticker]) == 0
