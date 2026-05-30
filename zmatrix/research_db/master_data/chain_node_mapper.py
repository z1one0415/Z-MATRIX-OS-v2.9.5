from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

from zmatrix.research_db.master_data import ChainNodeMapping


_GRADE_ORDER = {"A": 4, "B": 3, "C": 2, "D": 1, "": 0}


def _node_score(node: ChainNodeMapping) -> int:
    vc = _GRADE_ORDER.get(node.value_capture_grade, 0)
    ev = _GRADE_ORDER.get(node.evidence_grade, 0)
    return vc + ev


class ChainNodeMapper:
    def __init__(self, csv_path: Optional[str | Path] = None) -> None:
        self._by_ticker: dict[str, list[ChainNodeMapping]] = {}
        self._by_chain_id: dict[str, list[ChainNodeMapping]] = {}
        self._all: list[ChainNodeMapping] = []
        if csv_path is not None:
            self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path) -> None:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cnm = ChainNodeMapping(
                    ticker=row["ticker"].strip(),
                    chain_id=row["chain_id"].strip() or "",
                    chain_layer=row["chain_layer"].strip(),
                    chain_position=row["chain_position"].strip(),
                    value_capture_grade=row["value_capture_grade"].strip(),
                    evidence_grade=row["evidence_grade"].strip(),
                )
                self._by_ticker.setdefault(cnm.ticker, []).append(cnm)
                if cnm.chain_id:
                    self._by_chain_id.setdefault(cnm.chain_id, []).append(cnm)
                self._all.append(cnm)

    def get_chain_exposure(self, ticker: str) -> list[dict]:
        nodes = self._by_ticker.get(ticker, [])
        return [
            {
                "ticker": node.ticker,
                "chain_id": node.chain_id,
                "chain_layer": node.chain_layer,
                "chain_position": node.chain_position,
                "value_capture_grade": node.value_capture_grade,
                "evidence_grade": node.evidence_grade,
            }
            for node in nodes
        ]

    def get_primary_chain(self, ticker: str) -> dict | None:
        nodes = self._by_ticker.get(ticker, [])
        if not nodes:
            return None
        best = max(nodes, key=_node_score)
        return {
            "ticker": best.ticker,
            "chain_id": best.chain_id,
            "chain_layer": best.chain_layer,
            "chain_position": best.chain_position,
            "value_capture_grade": best.value_capture_grade,
            "evidence_grade": best.evidence_grade,
        }

    def get_secondary_chains(self, ticker: str) -> list[dict]:
        nodes = self._by_ticker.get(ticker, [])
        if len(nodes) <= 1:
            return []
        sc = sorted(nodes, key=_node_score, reverse=True)
        return [
            {
                "ticker": node.ticker,
                "chain_id": node.chain_id,
                "chain_layer": node.chain_layer,
                "chain_position": node.chain_position,
                "value_capture_grade": node.value_capture_grade,
                "evidence_grade": node.evidence_grade,
            }
            for node in sc[1:]
        ]

    def get_tickers_in_chain(self, chain_id: str) -> list[str]:
        return [node.ticker for node in self._by_chain_id.get(chain_id, [])]

    def detect_speculative_theme(self, ticker: str) -> bool:
        SPECULATIVE_LAYERS = ("CONCEPT_PLAY", "MEME_DRIVEN", "HYPE_CASCADE")
        nodes = self._by_ticker.get(ticker, [])
        for node in nodes:
            if node.chain_layer in SPECULATIVE_LAYERS:
                return True
            if node.value_capture_grade in ("D", "") or node.evidence_grade in ("D", ""):
                return True
        return False

    def detect_missing_evidence(self, ticker: str) -> bool:
        nodes = self._by_ticker.get(ticker)
        if nodes is None or len(nodes) == 0:
            return True
        for node in nodes:
            if not node.evidence_grade or node.evidence_grade in ("D", ""):
                return True
        return False
