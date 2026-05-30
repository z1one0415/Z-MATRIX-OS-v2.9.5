"""EV4: Research Analyzer — evaluate which research directions are most effective."""
from __future__ import annotations

class ResearchAnalyzer:
    @staticmethod
    def analyze_directions(direction_results: dict) -> dict:
        if not direction_results: return {"most_effective": "NONE", "least_effective": "NONE", "total_analyses": 0}
        name_by_score = sorted(direction_results.items(), key=lambda x: x[1].get("ic", 0), reverse=True)
        return {"most_effective": name_by_score[0][0] if name_by_score else "NONE", "least_effective": name_by_score[-1][0] if name_by_score else "NONE", "total_analyses": len(direction_results), "production_allowed": False}

    @staticmethod
    def compute_roi(directions: dict) -> dict:
        return {k: {"roi": v.get("ic", 0) / max(v.get("time_ms", 1), 1) * 1000000} for k, v in directions.items()}
