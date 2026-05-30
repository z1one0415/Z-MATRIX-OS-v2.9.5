"""EV4: Research Failure Engine — identify patterns of consistently failing research."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class FailureAnalysis:
    direction: str; total_attempts: int = 0; failures: int = 0
    failure_rate: float = 0.0; common_reason: str = ""; recommendation: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchFailureEngine:
    @staticmethod
    def analyze(failure_logs: list[dict]) -> list[FailureAnalysis]:
        by_direction = {}
        for fl in failure_logs:
            d = fl.get("direction", "UNKNOWN")
            if d not in by_direction: by_direction[d] = {"total": 0, "failures": 0, "reasons": []}
            by_direction[d]["total"] += 1
            if fl.get("result") != "PASS": by_direction[d]["failures"] += 1; by_direction[d]["reasons"].append(fl.get("reason", "UNKNOWN"))
        results = []
        for direction, stats in by_direction.items():
            fr = stats["failures"] / max(stats["total"], 1)
            common = max(set(stats["reasons"]), key=stats["reasons"].count) if stats["reasons"] else "UNKNOWN"
            rec = "RETIRE" if fr > 0.7 else ("REVIEW" if fr > 0.4 else "CONTINUE")
            results.append(FailureAnalysis(direction=direction, total_attempts=stats["total"], failures=stats["failures"], failure_rate=fr, common_reason=common, recommendation=rec))
        return results
