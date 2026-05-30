"""R4: Lesson Extractor — automated success/failure reason extraction."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Lesson:
    lesson_id: str; entry_id: str; category: str = "GENERAL"; summary: str = ""; cause: str = ""
    source_evidence: list = field(default_factory=list); production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class LessonExtractor:
    @staticmethod
    def extract(entry_id: str, result: str, metrics: dict) -> Lesson:
        lesson_id = f"L-{entry_id}"
        if result == "WINNER":
            if metrics.get("ic",0) > 0.05: return Lesson(lesson_id=lesson_id, entry_id=entry_id, category="FACTOR_EDGE", summary=f"Strong IC={metrics['ic']:.3f} drove success", cause=f"IC={metrics['ic']:.3f}", source_evidence=[metrics])
            return Lesson(lesson_id=lesson_id, entry_id=entry_id, category="UNCLEAR_EDGE", summary="Winner but unclear driver", cause="UNKNOWN")
        elif result == "LOSER":
            if abs(metrics.get("ic",0)) < 0.01: return Lesson(lesson_id=lesson_id, entry_id=entry_id, category="NO_ALPHA", summary="Near-zero IC", cause=f"IC={metrics.get('ic',0):.3f}", source_evidence=[metrics])
            return Lesson(lesson_id=lesson_id, entry_id=entry_id, category="ALPHA_DECAY", summary="Previously valid factor decayed", cause="DECAY")
        return Lesson(lesson_id=lesson_id, entry_id=entry_id)
