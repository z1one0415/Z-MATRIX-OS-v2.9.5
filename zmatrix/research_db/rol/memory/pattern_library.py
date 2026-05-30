"""R4: Pattern Library — reusable patterns, rules, and experience."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class Pattern:
    pattern_id: str; name: str; description: str; category: str = "GENERAL"; occurrences: int = 0
    examples: list = field(default_factory=list); last_seen: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PatternLibrary:
    def __init__(self): self._patterns: dict[str, Pattern] = {}
    def register(self, pattern_id: str, name: str, description: str, category: str = "GENERAL") -> Pattern:
        self._patterns[pattern_id] = Pattern(pattern_id=pattern_id, name=name, description=description, category=category); return self._patterns[pattern_id]
    def match(self, lessons: list) -> list[Pattern]:
        matched = []
        for lesson in lessons:
            for pid, pat in self._patterns.items():
                if lesson.category == pat.category: pat.occurrences += 1; pat.examples.append(lesson.lesson_id); matched.append(pat)
        seen=set(); unique=[]
        for p in matched:
            if p.pattern_id not in seen: seen.add(p.pattern_id); unique.append(p)
        return unique
    def list_all(self) -> list[Pattern]: return list(self._patterns.values())
    def by_category(self, category: str) -> list[Pattern]: return [p for p in self._patterns.values() if p.category==category]
