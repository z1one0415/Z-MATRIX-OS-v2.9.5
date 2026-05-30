"""R1: Research Search — fast retrieval by tags/state/date/type."""
from __future__ import annotations

class ResearchSearch:
    @staticmethod
    def search(registry, state_machine, archive, query: str, object_type: str = None, state: str = None, tags: list = None) -> list[dict]:
        results = []
        for e in registry.list_all():
            if object_type and e.object_type != object_type: continue
            if state and state_machine.get_state(e.entry_id) != state: continue
            if tags and not any(t in e.tags for t in tags): continue
            if query and query.lower() not in (e.name.lower() + e.entry_id.lower() + " ".join(e.tags).lower()): continue
            archived = archive.by_entry(e.entry_id)
            results.append({"entry_id":e.entry_id,"type":e.object_type,"ticker":e.ticker,"state":state_machine.get_state(e.entry_id),"archived":len(archived)})
        return results
