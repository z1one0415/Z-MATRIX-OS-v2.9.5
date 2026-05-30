from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

from zmatrix.research_db.master_data import AliasType, TickerAlias


class AliasRegistry:
    def __init__(self, csv_path: Optional[str | Path] = None) -> None:
        self._alias_to_ticker: dict[str, str] = {}
        self._ticker_to_aliases: dict[str, list[TickerAlias]] = {}
        if csv_path is not None:
            self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path) -> None:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ta = TickerAlias(
                    ticker=row["ticker"].strip(),
                    alias=row["alias"].strip(),
                    alias_type=AliasType(row["alias_type"].strip()),
                    effective_date=row.get("effective_date", "").strip() or None,
                    expiry_date=row.get("expiry_date", "").strip() or None,
                )
                self._alias_to_ticker[ta.alias] = ta.ticker
                self._ticker_to_aliases.setdefault(ta.ticker, []).append(ta)

    def resolve_alias(self, alias: str) -> Optional[str]:
        return self._alias_to_ticker.get(alias)

    def get_aliases(self, ticker: str) -> list[TickerAlias]:
        return list(self._ticker_to_aliases.get(ticker, []))

    def add_alias(self, ticker: str, alias: str, alias_type: str) -> None:
        ta = TickerAlias(
            ticker=ticker,
            alias=alias,
            alias_type=AliasType(alias_type),
        )
        self._alias_to_ticker[alias] = ticker
        self._ticker_to_aliases.setdefault(ticker, []).append(ta)
