from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

from zmatrix.research_db.master_data import ChainTaxonomy as ChainTaxonomyRecord


class ChainTaxonomyRegistry:
    def __init__(self, csv_path: Optional[str | Path] = None) -> None:
        self._by_chain_id: dict[str, ChainTaxonomyRecord] = {}
        self._children: dict[str, list[str]] = {}
        self._all: list[ChainTaxonomyRecord] = []
        if csv_path is not None:
            self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path) -> None:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ct = ChainTaxonomyRecord(
                    chain_id=row["chain_id"].strip(),
                    chain_name=row["chain_name"].strip(),
                    chain_type=row["chain_type"].strip(),
                    parent_chain_id=row.get("parent_chain_id", "").strip() or None,
                )
                self._by_chain_id[ct.chain_id] = ct
                if ct.parent_chain_id is not None:
                    self._children.setdefault(ct.parent_chain_id, []).append(ct.chain_id)
                self._all.append(ct)

    def get_chain(self, chain_id: str) -> dict:
        ct = self._by_chain_id[chain_id]
        return {
            "chain_id": ct.chain_id,
            "chain_name": ct.chain_name,
            "chain_type": ct.chain_type,
            "parent_chain_id": ct.parent_chain_id,
        }

    def get_child_chains(self, chain_id: str) -> list[str]:
        return list(self._children.get(chain_id, []))

    def list_chains(self) -> list[dict]:
        return [
            {
                "chain_id": ct.chain_id,
                "chain_name": ct.chain_name,
                "chain_type": ct.chain_type,
                "parent_chain_id": ct.parent_chain_id,
            }
            for ct in self._all
        ]

    def get_parent(self, chain_id: str) -> str | None:
        ct = self._by_chain_id[chain_id]
        return ct.parent_chain_id
