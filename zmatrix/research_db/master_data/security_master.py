from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

from zmatrix.research_db.master_data import Exchange, ListingStatus, SecurityMaster


class SecurityMasterRegistry:
    def __init__(self, csv_path: Optional[str | Path] = None) -> None:
        self._by_ticker: dict[str, SecurityMaster] = {}
        self._by_name: dict[str, list[SecurityMaster]] = {}
        self._by_exchange: dict[str, list[SecurityMaster]] = {}
        self._by_sw_l1: dict[str, list[SecurityMaster]] = {}
        self._all: list[SecurityMaster] = []
        if csv_path is not None:
            self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path) -> None:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sm = SecurityMaster(
                    ticker=row["ticker"].strip(),
                    name=row["name"].strip(),
                    exchange=Exchange(row["exchange"].strip()),
                    listing_date=row.get("listing_date", "").strip() or None,
                    listing_status=ListingStatus(row.get("listing_status", "UNKNOWN").strip()),
                    market_cap_float=float(row["market_cap_float"]) if row.get("market_cap_float", "").strip() else None,
                    market_cap_total=float(row["market_cap_total"]) if row.get("market_cap_total", "").strip() else None,
                    sw_l1=row.get("sw_l1", "").strip() or None,
                    sw_l2=row.get("sw_l2", "").strip() or None,
                    sw_l3=row.get("sw_l3", "").strip() or None,
                )
                self._by_ticker[sm.ticker] = sm
                self._by_name.setdefault(sm.name, []).append(sm)
                self._by_exchange.setdefault(sm.exchange.value, []).append(sm)
                if sm.sw_l1 is not None:
                    self._by_sw_l1.setdefault(sm.sw_l1, []).append(sm)
                self._all.append(sm)

    def get_by_ticker(self, ticker: str) -> SecurityMaster:
        return self._by_ticker[ticker]

    def get_by_name(self, name: str) -> list[SecurityMaster]:
        return self._by_name.get(name, [])

    def get_by_exchange(self, exchange: str) -> list[SecurityMaster]:
        return self._by_exchange.get(exchange, [])

    def get_by_industry(self, sw_l1: str) -> list[SecurityMaster]:
        return self._by_sw_l1.get(sw_l1, [])

    def list_all(self) -> list[SecurityMaster]:
        return list(self._all)

    def count(self) -> int:
        return len(self._all)

    def has_ticker(self, ticker: str) -> bool:
        return ticker in self._by_ticker
