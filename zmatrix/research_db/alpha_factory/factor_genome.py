"""Phase 4-F5: Factor Genome — lineage tracking: parent→child→composite→derivative."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

class GenomeRelation(str):
    PARENT="PARENT"; CHILD="CHILD"; COMPOSITE="COMPOSITE"; DERIVATIVE="DERIVATIVE"

@dataclass
class GenomeRecord:
    factor_id: str; relation: str; related_factor_id: str
    note: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class FactorGenome:
    def __init__(self): self._relations: list[GenomeRecord] = []
    def register(self, factor_id: str, relation: str, related_id: str, note: str = "") -> GenomeRecord:
        r = GenomeRecord(factor_id=factor_id, relation=relation, related_factor_id=related_id, note=note)
        self._relations.append(r); return r

    def get_children(self, factor_id: str) -> list[GenomeRecord]:
        return [r for r in self._relations if r.related_factor_id == factor_id and r.relation == GenomeRelation.CHILD]

    def get_parents(self, factor_id: str) -> list[GenomeRecord]:
        return [r for r in self._relations if r.factor_id == factor_id and r.relation == GenomeRelation.PARENT]

    def get_lineage(self, factor_id: str) -> dict:
        return {"factor_id": factor_id, "parents": self.get_parents(factor_id), "children": self.get_children(factor_id)}

    def list_all(self) -> list[GenomeRecord]: return list(self._relations)
