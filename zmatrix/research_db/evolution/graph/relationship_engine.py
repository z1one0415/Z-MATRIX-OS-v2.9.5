"""EV1: Relationship Engine — cause-effect chain builder."""
from .knowledge_graph import KnowledgeGraph
class RelationshipEngine:
    def __init__(self, kg: KnowledgeGraph): self.kg = kg
    def link(self, rel_id: str, source: str, target: str, rel_type: str) -> dict:
        r = self.kg.add_relationship(rel_id, source, target, rel_type)
        return {"rel_id": r.rel_id, "source": source, "target": target, "type": rel_type}
    def trace_chain(self, start_entity: str, max_depth: int = 5) -> list[dict]:
        chain = []; visited = set(); queue = [(start_entity, 0)]
        while queue and len(chain) < max_depth * 10:
            current, depth = queue.pop(0)
            if current in visited or depth > max_depth: continue
            visited.add(current)
            for r in self.kg.get_outgoing(current):
                chain.append({"from": r.source_id, "to": r.target_id, "type": r.rel_type, "depth": depth})
                queue.append((r.target_id, depth + 1))
        return chain
