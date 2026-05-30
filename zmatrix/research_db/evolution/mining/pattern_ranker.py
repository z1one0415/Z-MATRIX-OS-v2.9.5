"""EV3: Pattern Ranker — rank patterns by support * confidence."""
from __future__ import annotations

class PatternRanker:
    @staticmethod
    def rank(patterns: list) -> list:
        return sorted(patterns, key=lambda p: p.support * p.confidence, reverse=True)

    @staticmethod
    def top_patterns(patterns: list, n: int = 5) -> list:
        return PatternRanker.rank(patterns)[:n]
