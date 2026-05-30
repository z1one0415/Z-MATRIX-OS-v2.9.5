"""EV4: Research Efficiency — measure research throughput and quality."""
from __future__ import annotations

class ResearchEfficiency:
    @staticmethod
    def compute_efficiency(research_logs: list[dict]) -> dict:
        if not research_logs: return {"total_research": 0, "success_rate": 0, "avg_duration_ms": 0, "efficiency_score": 0}
        total = len(research_logs)
        successes = sum(1 for r in research_logs if r.get("result") == "PASS")
        durations = [r.get("duration_ms", 0) for r in research_logs]
        avg_duration = sum(durations) / total if durations else 0
        efficiency = (successes / total) / max(avg_duration / 1000, 1) if total > 0 else 0
        return {"total_research": total, "success_rate": successes / total, "avg_duration_ms": avg_duration, "efficiency_score": efficiency, "production_allowed": False}
