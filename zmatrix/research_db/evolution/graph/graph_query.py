"""EV1: Graph Query — path finding and impact analysis."""
from .knowledge_graph import KnowledgeGraph
class GraphQuery:
    def __init__(self, kg: KnowledgeGraph): self.kg = kg
    def find_paths(self, source: str, target: str, max_depth: int = 5) -> list[list[str]]:
        paths = []
        def dfs(current, target, visited, path, depth):
            if depth > max_depth: return
            if current == target: paths.append(path + [current]); return
            for r in self.kg.get_outgoing(current):
                if r.target_id not in visited:
                    visited.add(r.target_id); dfs(r.target_id, target, visited, path + [current], depth + 1); visited.discard(r.target_id)
        dfs(source, target, {source}, [], 0)
        return paths[:20]
    def impact_analysis(self, entity_id: str, max_depth: int = 3) -> dict:
        outgoing = self.kg.get_outgoing(entity_id); incoming = self.kg.get_incoming(entity_id)
        return {"entity": entity_id, "outgoing_count": len(outgoing), "incoming_count": len(incoming), "directly_impacts": list(set(r.target_id for r in outgoing))}
