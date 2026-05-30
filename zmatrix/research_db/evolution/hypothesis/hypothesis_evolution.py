"""EV2: Hypothesis Evolution — mutation + selection + inheritance."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class HypothesisGene:
    gene_id: str; parent_id: str; motivation: str; mutations: list = field(default_factory=list)
    fitness: float = 0.0; generation: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class HypothesisEvolution:
    def __init__(self): self._genes: list[HypothesisGene] = []
    def seed(self, gene_id: str, motivation: str) -> HypothesisGene:
        g = HypothesisGene(gene_id=gene_id, parent_id="ORIGIN", motivation=motivation); self._genes.append(g); return g
    def mutate(self, parent_id: str, gene_id: str, mutations: list) -> HypothesisGene | None:
        parent = next((g for g in self._genes if g.gene_id==parent_id), None)
        if not parent: return None
        g = HypothesisGene(gene_id=gene_id, parent_id=parent_id, motivation=parent.motivation, mutations=mutations, generation=parent.generation+1)
        self._genes.append(g); return g
    def select_best(self, fitness_fn) -> HypothesisGene | None:
        for g in self._genes: g.fitness = fitness_fn(g)
        return max(self._genes, key=lambda g: g.fitness) if self._genes else None
    def generation_count(self) -> int: return max((g.generation for g in self._genes), default=0)
