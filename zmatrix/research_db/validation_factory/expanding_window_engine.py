"""F2-C: Expanding Window Engine — growing windows for stability check."""
from __future__ import annotations

class ExpandingWindowEngine:
    @staticmethod
    def generate_windows(data: list[dict], min_size: int = 60, step: int = 20) -> list[dict]:
        windows = []
        for end in range(min_size, len(data) + 1, step):
            windows.append({"start": 0, "end": end, "data": data[:end]})
        return windows

    @staticmethod
    def compute_stability(ic_series: list[float]) -> dict:
        if len(ic_series) < 3: return {"stable": False, "trend": 0, "volatility": 0}
        import statistics
        trend = ic_series[-1] - ic_series[0]
        std = statistics.stdev(ic_series)
        stable = abs(trend) < std * 0.5
        return {"stable": stable, "trend": trend, "volatility": std, "production_allowed": False}
