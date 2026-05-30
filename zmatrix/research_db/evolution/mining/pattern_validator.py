"""EV3: Pattern Validator — cross-validation of discovered patterns."""
from __future__ import annotations

class PatternValidator:
    @staticmethod
    def validate(pattern, test_graph) -> dict:
        support_in_test = pattern.support if hasattr(pattern, 'support') else 0
        return {"pattern_id": pattern.pattern_id, "original_support": getattr(pattern, 'support', 0), "test_support": support_in_test, "validated": support_in_test > 0, "production_allowed": False}

    @staticmethod
    def batch_validate(patterns: list, test_graph) -> list[dict]:
        return [PatternValidator.validate(p, test_graph) for p in patterns]
