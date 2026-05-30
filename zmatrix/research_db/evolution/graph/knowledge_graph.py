"""EV1: Knowledge Graph — Factor→Portfolio→Outcome→Prediction→Council→Lesson."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, json

@dataclass
class Entity:
    entity_id: str; entity_type: str; label: str; properties: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class Relationship:
    rel_id: str; source_id: str; target_id: str; rel_type: str; properties: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class KnowledgeGraph:
    def __init__(self): self._entities: dict[str, Entity] = {}; self._rels: list[Relationship] = []
    def add_entity(self, entity_id: str, entity_type: str, label: str, props: dict = None) -> Entity:
        e = Entity(entity_id=entity_id, entity_type=entity_type, label=label, properties=props or {})
        self._entities[entity_id] = e; return e
    def add_relationship(self, rel_id: str, source: str, target: str, rel_type: str, props: dict = None) -> Relationship:
        r = Relationship(rel_id=rel_id, source_id=source, target_id=target, rel_type=rel_type, properties=props or {})
        self._rels.append(r); return r
    def get_entity(self, entity_id: str) -> Entity | None: return self._entities.get(entity_id)
    def get_outgoing(self, source_id: str) -> list[Relationship]: return [r for r in self._rels if r.source_id==source_id]
    def get_incoming(self, target_id: str) -> list[Relationship]: return [r for r in self._rels if r.target_id==target_id]
    def entity_count(self) -> int: return len(self._entities)
    def rel_count(self) -> int: return len(self._rels)
    def graph_hash(self) -> str:
        h = hashlib.sha256(json.dumps({"entities":len(self._entities),"rels":len(self._rels)},sort_keys=True).encode()); return h.hexdigest()[:16]
