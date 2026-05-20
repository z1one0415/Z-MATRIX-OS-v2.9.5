from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


def clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


@dataclass(slots=True)
class BlackHorseGeneResult:
    total_score: float
    float_market_cap_score: float
    overhead_pressure_score: float
    volatility_compression_score: float
    historical_limit_gene_score: float
    platform_distance_score: float
    turnover_memory_score: float
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def score_float_market_cap(float_market_cap_billion: float | None) -> float:
    if float_market_cap_billion is None:
        return 5.0
    if 20 <= float_market_cap_billion <= 80:
        return 9.0
    if 80 < float_market_cap_billion <= 150:
        return 7.0
    if 10 <= float_market_cap_billion < 20:
        return 6.0
    if 150 < float_market_cap_billion <= 300:
        return 4.5
    return 2.5


def score_overhead_pressure(overhead_pressure_pct: float | None) -> float:
    if overhead_pressure_pct is None:
        return 5.0
    if overhead_pressure_pct < 10:
        return 9.0
    if overhead_pressure_pct < 20:
        return 7.5
    if overhead_pressure_pct < 30:
        return 5.5
    return 2.0


def score_volatility_compression(volatility_compression_pct: float | None) -> float:
    """Compression pct means current volatility vs recent baseline. Lower is more compressed."""
    if volatility_compression_pct is None:
        return 5.0
    if volatility_compression_pct <= 35:
        return 9.0
    if volatility_compression_pct <= 55:
        return 7.0
    if volatility_compression_pct <= 80:
        return 5.0
    return 3.0


def score_historical_limit_gene(limit_up_count_120d: int | None) -> float:
    if limit_up_count_120d is None:
        return 5.0
    if limit_up_count_120d >= 6:
        return 9.0
    if limit_up_count_120d >= 3:
        return 7.5
    if limit_up_count_120d >= 1:
        return 6.0
    return 3.5


def score_platform_distance(distance_to_platform_breakout_pct: float | None) -> float:
    """Distance to breakout. Best if near but not already far above platform."""
    if distance_to_platform_breakout_pct is None:
        return 5.0
    d = abs(distance_to_platform_breakout_pct)
    if d <= 3:
        return 9.0
    if d <= 6:
        return 7.0
    if d <= 10:
        return 5.0
    return 3.0


def score_turnover_memory(turnover_memory_score: float | None) -> float:
    if turnover_memory_score is None:
        return 5.0
    return clamp(turnover_memory_score)


def score_blackhorse_gene(payload: dict[str, Any]) -> BlackHorseGeneResult:
    s1 = score_float_market_cap(payload.get("float_market_cap_billion"))
    s2 = score_overhead_pressure(payload.get("overhead_pressure_pct"))
    s3 = score_volatility_compression(payload.get("volatility_compression_pct"))
    s4 = score_historical_limit_gene(payload.get("limit_up_count_120d"))
    s5 = score_platform_distance(payload.get("distance_to_platform_breakout_pct"))
    s6 = score_turnover_memory(payload.get("turnover_memory_score"))
    total = s1 * 0.20 + s2 * 0.20 + s3 * 0.15 + s4 * 0.15 + s5 * 0.15 + s6 * 0.15
    notes: list[str] = []
    if s2 < 4:
        notes.append("上方套牢压力偏大，黑马拉升成本高")
    if s1 < 4:
        notes.append("流通市值不适合短线黑马弹性")
    return BlackHorseGeneResult(round(total, 2), s1, s2, s3, s4, s5, s6, notes)
