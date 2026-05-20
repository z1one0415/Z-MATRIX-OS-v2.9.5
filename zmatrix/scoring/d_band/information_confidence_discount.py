from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Mapping


class FieldClass(str, Enum):
    CRITICAL = "critical"
    CORE = "core"
    ENHANCEMENT = "enhancement"


@dataclass(frozen=True, slots=True)
class FieldRule:
    name: str
    field_class: FieldClass


DEFAULT_FIELD_RULES = [
    FieldRule("code", FieldClass.CRITICAL),
    FieldRule("trade_date", FieldClass.CRITICAL),
    FieldRule("close", FieldClass.CRITICAL),
    FieldRule("volume", FieldClass.CRITICAL),
    FieldRule("turnover", FieldClass.CRITICAL),
    FieldRule("sector", FieldClass.CRITICAL),
    FieldRule("float_market_cap_billion", FieldClass.CORE),
    FieldRule("overhead_pressure_pct", FieldClass.CORE),
    FieldRule("volatility_compression_pct", FieldClass.CORE),
    FieldRule("limit_up_count_120d", FieldClass.CORE),
    FieldRule("distance_to_platform_breakout_pct", FieldClass.CORE),
    FieldRule("turnover_memory_score", FieldClass.CORE),
    FieldRule("sector_breadth", FieldClass.CORE),
    FieldRule("leader_strength", FieldClass.CORE),
    FieldRule("theme_seed", FieldClass.ENHANCEMENT),
    FieldRule("smart_money_preload", FieldClass.ENHANCEMENT),
    FieldRule("micro_absorption", FieldClass.ENHANCEMENT),
]


@dataclass(slots=True)
class CoverageAssessment:
    coverage_ratio: float
    critical_missing: bool
    missing_critical: list[str] = field(default_factory=list)
    missing_core: list[str] = field(default_factory=list)
    missing_enhancement: list[str] = field(default_factory=list)
    lifecycle_max: str = "D3_CANDIDATE"
    allowed_action_max: str = "PAPER_PROBE_PLAN"
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _has_value(payload: Mapping[str, Any], key: str) -> bool:
    value = payload.get(key)
    return value is not None and value != ""


def lifecycle_cap_by_coverage(c: float, critical_missing: bool) -> tuple[str, str]:
    if critical_missing:
        return "DATA_INCOMPLETE", "NONE"
    if c < 0.50:
        return "D1_THEME_SEED", "WATCH_ONLY"
    if c < 0.70:
        return "D2_PREHEAT", "WATCH"
    if c < 0.85:
        return "D3_CANDIDATE", "PAPER_PROBE_PLAN"
    return "D3_IGNITION_READY_ELIGIBLE", "PAPER_PROBE_PLAN"


def assess_coverage(
    payload: Mapping[str, Any],
    rules: list[FieldRule] | None = None,
) -> CoverageAssessment:
    rules = rules or DEFAULT_FIELD_RULES
    effective_rules = [r for r in rules if r.field_class != FieldClass.CRITICAL]
    present = sum(1 for r in effective_rules if _has_value(payload, r.name))
    coverage = 1.0 if not effective_rules else present / len(effective_rules)
    missing_critical = [r.name for r in rules if r.field_class == FieldClass.CRITICAL and not _has_value(payload, r.name)]
    missing_core = [r.name for r in rules if r.field_class == FieldClass.CORE and not _has_value(payload, r.name)]
    missing_enh = [r.name for r in rules if r.field_class == FieldClass.ENHANCEMENT and not _has_value(payload, r.name)]
    lifecycle, action = lifecycle_cap_by_coverage(coverage, bool(missing_critical))
    warnings: list[str] = []
    if missing_critical:
        warnings.append("critical_fields_missing")
    if coverage < 0.70:
        warnings.append("coverage_discount_active")
    return CoverageAssessment(
        coverage_ratio=round(coverage, 4),
        critical_missing=bool(missing_critical),
        missing_critical=missing_critical,
        missing_core=missing_core,
        missing_enhancement=missing_enh,
        lifecycle_max=lifecycle,
        allowed_action_max=action,
        warnings=warnings,
    )


def apply_confidence_discount(raw_score: float, coverage_ratio: float, threshold: float = 0.70) -> float:
    """Apply post-hoc confidence discount without double-penalizing missing fields.

    Raw score should be calculated with neutral fills.  Coverage discount is the
    only mathematical penalty for non-critical missing data.
    """

    if coverage_ratio >= threshold:
        return round(raw_score, 4)
    factor = (coverage_ratio / threshold) ** 2 if threshold > 0 else 0.0
    return round(raw_score * factor, 4)


def neutral_fill(value: Any, neutral: float = 5.0) -> float:
    """Return neutral score for non-critical missing scoring fields."""

    if value is None or value == "":
        return neutral
    return float(value)
