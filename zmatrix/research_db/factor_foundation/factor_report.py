"""Batch-B: Factor Report — Top/Weak/Stability/Decay."""
from __future__ import annotations
import statistics

class FactorReport:
    @staticmethod
    def generate_top_factors(snapshots: list, n: int = 10, metric: str = "ic") -> list:
        key = lambda s: abs(getattr(s, metric, 0))
        sorted_snaps = sorted(snapshots, key=key, reverse=True)
        return [{"factor_id": s.factor_id, "factor_name": s.factor_name, metric: getattr(s, metric, 0)}
                for s in sorted_snaps[:n]]

    @staticmethod
    def generate_weak_factors(snapshots: list, n: int = 10, metric: str = "ic") -> list:
        key = lambda s: abs(getattr(s, metric, 0))
        sorted_snaps = sorted(snapshots, key=key)
        return [{"factor_id": s.factor_id, "factor_name": s.factor_name, metric: getattr(s, metric, 0)}
                for s in sorted_snaps[:n]]

    @staticmethod
    def compute_stability(historical_snapshots: list, factor_id: str) -> float:
        ic_values = [s.ic for s in historical_snapshots if s.factor_id == factor_id]
        if len(ic_values) < 2: return 0.0
        mean_ic = statistics.mean(ic_values)
        std_ic = statistics.stdev(ic_values) if len(ic_values) > 1 else 0.0
        return abs(std_ic / mean_ic) if mean_ic != 0 else 0.0

    @staticmethod
    def compute_decay(historical_snapshots: list, factor_id: str, window_days: int = 20) -> float:
        ic_values = [s.ic for s in historical_snapshots if s.factor_id == factor_id]
        if len(ic_values) < 2: return 0.0
        return abs(ic_values[-1] - ic_values[0])

    @staticmethod
    def generate_report(snapshots: list) -> str:
        lines = ["# Factor Foundation Report","",f"## Summary",f"- Factors analyzed: {len(snapshots)}"]
        if snapshots:
            top = FactorReport.generate_top_factors(snapshots, 3)
            lines.append("## Top Factors")
            for t in top: lines.append(f"- {t['factor_name']}: IC={t['ic']:.4f}")
            lines.extend(["","## Safety","- Production: BLOCKED","- Broker/runtime: BLOCKED"])
        return "\n".join(lines)
