from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Optional

from zmatrix.research_db.master_data import Confidence, IndustryMapping


class IndustryTaxonomy:
    def __init__(self, csv_path: Optional[str | Path] = None) -> None:
        self._by_ticker: dict[str, IndustryMapping] = {}
        self._by_sw_l1: dict[str, list[IndustryMapping]] = {}
        self._all: list[IndustryMapping] = []
        if csv_path is not None:
            self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path) -> None:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                im = IndustryMapping(
                    ticker=row["ticker"].strip(),
                    sw_l1=row.get("sw_l1", "").strip() or None,
                    sw_l2=row.get("sw_l2", "").strip() or None,
                    sw_l3=row.get("sw_l3", "").strip() or None,
                    confidence=Confidence(row.get("confidence", "UNVERIFIED").strip()),
                )
                self._by_ticker[im.ticker] = im
                if im.sw_l1 is not None:
                    self._by_sw_l1.setdefault(im.sw_l1, []).append(im)
                self._all.append(im)

    def get_industry(self, ticker: str) -> dict:
        im = self._by_ticker[ticker]
        return {
            "ticker": im.ticker,
            "sw_l1": im.sw_l1,
            "sw_l2": im.sw_l2,
            "sw_l3": im.sw_l3,
            "confidence": im.confidence.value,
        }

    def get_tickers_in_industry(self, sw_l1: str) -> list[str]:
        return [im.ticker for im in self._by_sw_l1.get(sw_l1, [])]

    def list_industries(self) -> list[str]:
        return sorted(self._by_sw_l1.keys())

    def count_by_industry(self) -> dict[str, int]:
        return {k: len(v) for k, v in self._by_sw_l1.items()}

    def detect_low_confidence(self, ticker: str) -> bool:
        im = self._by_ticker.get(ticker)
        if im is None:
            return True
        return im.confidence in (Confidence.LOW, Confidence.UNVERIFIED)

    def detect_missing(self, ticker: str) -> bool:
        return ticker not in self._by_ticker

    def detect_expired(self, ticker: str, as_of_date: date) -> bool:
        del as_of_date
        return ticker not in self._by_ticker
