from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from .blackhorse_gene_screener import score_blackhorse_gene
from .sector_ignition_mapper import score_sector_ignition
from .d_early_scorer import score_vol_price_preload
from .information_confidence_discount import assess_coverage, apply_confidence_discount, neutral_fill
from .silent_accumulation_detector import score_silent_accumulation
from .micro_absorption_detector import score_micro_absorption


def _clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


DEFAULT_V22_WEIGHTS = {
    "blackhorse_gene": 0.22,
    "sector_ignition": 0.18,
    "theme_seed": 0.15,
    "silent_accumulation": 0.18,
    "smart_money_preload": 0.10,
    "micro_absorption": 0.10,
    "volume_price_preload": 0.07,
}


@dataclass(slots=True)
class DEarlyV22Result:
    code: str
    name: str
    raw_score: float
    final_score: float
    coverage_ratio: float
    lifecycle_max: str
    allowed_action_max: str
    stage_hint: str
    score_breakdown: dict[str, float]
    false_preheat_penalty: float = 0.0
    warnings: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=lambda: [
        "D-Matrix v2.2 does not emit real trade action",
        "D3_CANDIDATE is not D3_IGNITION_READY",
        "Theme Seed is not executable without M1/L1.5 confirmation",
    ])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _theme_seed_score(theme: dict[str, Any]) -> float:
    if not theme:
        return 5.0
    novelty = float(theme.get("novelty_score", 5.0))
    relevance = float(theme.get("relevance_score", 5.0))
    verified = bool(theme.get("theme_seed_verified", False))
    base = (novelty * 0.55 + relevance * 0.45)
    return _clamp(base + (0.8 if verified else 0.0))


def _smart_money_score(smart_money: dict[str, Any]) -> float:
    if not smart_money:
        return 5.0
    return _clamp(float(smart_money.get("score", 5.0)))


def evaluate_d_early_v22(payload: dict[str, Any], weights: dict[str, float] | None = None) -> DEarlyV22Result:
    """D-Matrix v2.2 source-radar aggregator.

    Uses neutral fill for missing non-critical fields, then applies coverage
    discount and lifecycle caps.  It only outputs WATCH/PAPER-level hints.
    """

    weights = weights or DEFAULT_V22_WEIGHTS
    code = str(payload.get("code", ""))
    name = str(payload.get("name", ""))
    coverage = assess_coverage(payload)
    warnings = list(coverage.warnings)

    if coverage.critical_missing:
        return DEarlyV22Result(
            code=code,
            name=name,
            raw_score=0.0,
            final_score=0.0,
            coverage_ratio=coverage.coverage_ratio,
            lifecycle_max=coverage.lifecycle_max,
            allowed_action_max=coverage.allowed_action_max,
            stage_hint="DATA_INCOMPLETE",
            score_breakdown={},
            warnings=warnings + ["critical_missing_blocked"],
        )

    gene_score = neutral_fill(None)
    if payload.get("gene"):
        gene_score = score_blackhorse_gene(payload.get("gene", {})).total_score
    elif payload.get("blackhorse_gene_score") is not None:
        gene_score = float(payload.get("blackhorse_gene_score"))

    sector_score = neutral_fill(None)
    if payload.get("sector_payload"):
        sector_score = score_sector_ignition(payload.get("sector_payload", {})).total_score_0_10
    elif payload.get("sector_ignition_score") is not None:
        sector_score = float(payload.get("sector_ignition_score"))

    vol_price_score = neutral_fill(None)
    if payload.get("market"):
        vol_price_score = score_vol_price_preload(payload.get("market", {}))
    elif payload.get("volume_price_preload_score") is not None:
        vol_price_score = float(payload.get("volume_price_preload_score"))

    theme_score = _theme_seed_score(payload.get("theme", {}))
    silent_result = score_silent_accumulation(payload.get("silent_accumulation", {}))
    smart_money_score = _smart_money_score(payload.get("smart_money", {}))
    micro_result = score_micro_absorption(payload.get("micro_absorption", {}))
    false_penalty = float(payload.get("false_preheat_penalty", 0.0))

    breakdown = {
        "blackhorse_gene": round(_clamp(gene_score), 2),
        "sector_ignition": round(_clamp(sector_score), 2),
        "theme_seed": round(_clamp(theme_score), 2),
        "silent_accumulation": silent_result.score,
        "smart_money_preload": round(_clamp(smart_money_score), 2),
        "micro_absorption": micro_result.score,
        "volume_price_preload": round(_clamp(vol_price_score), 2),
    }
    raw = sum(breakdown[k] * weights[k] for k in weights)
    raw = _clamp(raw - false_penalty * 2.0)  # penalty input 0-1 -> up to -2 score.
    final = apply_confidence_discount(raw, coverage.coverage_ratio)

    # Stage hint remains conservative.
    if coverage.lifecycle_max == "DATA_INCOMPLETE":
        stage = "DATA_INCOMPLETE"
    elif final >= 7.2 and coverage.coverage_ratio >= 0.70:
        stage = "D3_CANDIDATE"
    elif final >= 6.0:
        stage = "D2_PREHEAT"
    elif theme_score >= 6.0:
        stage = "D1_THEME_SEED"
    else:
        stage = "D0_COLD_IDLE"
    # Apply lifecycle cap textually; callers can map rank if needed.
    if coverage.lifecycle_max in {"D1_THEME_SEED", "D2_PREHEAT"} and stage not in {"D0_COLD_IDLE", coverage.lifecycle_max}:
        stage = coverage.lifecycle_max
        warnings.append("stage_capped_by_coverage")
    return DEarlyV22Result(
        code=code,
        name=name,
        raw_score=round(raw, 2),
        final_score=round(final, 2),
        coverage_ratio=coverage.coverage_ratio,
        lifecycle_max=coverage.lifecycle_max,
        allowed_action_max=coverage.allowed_action_max,
        stage_hint=stage,
        score_breakdown=breakdown,
        false_preheat_penalty=false_penalty,
        warnings=warnings,
    )
