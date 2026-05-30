"""EV3: Pattern Miner — automatic pattern discovery from knowledge graph."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class MinedPattern:
    pattern_id: str; pattern_type: str; entities: list = field(default_factory=list)
    confidence: float = 0.0; support: int = 0; description: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PatternMiner:
    @staticmethod
    def mine_from_graph(kg, min_support: int = 2) -> list[MinedPattern]:
        patterns = []
        for source_id, entity in kg._entities.items():
            outgoing = kg.get_outgoing(source_id)
            if len(outgoing) >= min_support:
                rel_types = [r.rel_type for r in outgoing]
                if len(set(rel_types)) == 1:
                    patterns.append(MinedPattern(pattern_id=f"P-{source_id}", pattern_type=rel_types[0], entities=[r.target_id for r in outgoing], support=len(outgoing), confidence=0.7, description=f"{entity.entity_type} → {rel_types[0]}"))
        return patterns

    @staticmethod
    def mine_co_occurrence(registry, entity_types: list) -> list[MinedPattern]:
        patterns = []
        by_type = {}
        for et in entity_types:
            entities = [e for e in registry._entities.values() if e.entity_type == et]
            by_type[et] = len(entities)
        max_type = max(by_type, key=by_type.get) if by_type else ""
        patterns.append(MinedPattern(pattern_id="CO-OCCUR", pattern_type="FREQUENCY", entities=[max_type], support=by_type.get(max_type,0), confidence=0.5, description="Most frequent entity type"))
        return patterns
