"""EV1: Entity Registry — typed entity registration."""
from .knowledge_graph import KnowledgeGraph, Entity
class EntityRegistry:
    def __init__(self, kg: KnowledgeGraph): self.kg = kg
    def register(self, entity_id: str, entity_type: str, label: str, props: dict = None) -> Entity:
        return self.kg.add_entity(entity_id, entity_type, label, props)
    def get_by_type(self, entity_type: str) -> list[Entity]:
        return [e for e in self.kg._entities.values() if e.entity_type == entity_type]
    def count_by_type(self) -> dict:
        counts = {}
        for e in self.kg._entities.values(): counts[e.entity_type] = counts.get(e.entity_type, 0) + 1
        return counts
