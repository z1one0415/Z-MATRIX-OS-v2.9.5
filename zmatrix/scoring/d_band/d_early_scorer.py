from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any

from .blackhorse_gene_screener import score_blackhorse_gene
from .sector_ignition_mapper import score_sector_ignition
from .d_band_config import DBandConfig, load_config
from .d_band_contracts import (
    DataCompleteness,
    ScoreBreakdown,
    DBandReport,
    ExecutionMode,
    AllowedAction,
)
from .d_band_lifecycle import apply_phase1_lifecycle


def clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


def score_vol_price_preload(market: dict[str, Any]) -> float:
    """Daily-bar proxy for warm pre-ignition. It is not smart-money confirmation."""
    score = 0.0
    volume_ratio = market.get("volume_ratio")
    change_pct = market.get("price_change_pct")
    close_position_pct = market.get("close_position_pct")
    consecutive_up_days = market.get("consecutive_up_days", 0)
    above_ma5 = bool(market.get("above_ma5", False))
    is_limit_up = bool(market.get("is_limit_up", False))

    if volume_ratio is not None:
        if 1.3 <= volume_ratio <= 5.0:
            score += 2.5
        elif 1.1 <= volume_ratio < 1.3 or 5.0 < volume_ratio <= 7.0:
            score += 1.0
    if change_pct is not None:
        if 2.0 <= change_pct <= 6.0:
            score += 2.0
        elif 0.5 <= change_pct < 2.0 or 6.0 < change_pct <= 8.0:
            score += 1.0
    if close_position_pct is not None:
        if close_position_pct >= 70:
            score += 2.0
        elif close_position_pct >= 55:
            score += 1.0
    if 3 <= consecutive_up_days <= 5:
        score += 1.5
    elif consecutive_up_days >= 6:
        score += 0.5  # too extended
    if above_ma5:
        score += 1.0
    if is_limit_up:
        score -= 2.0  # Phase1 early detector should not treat limit-up as early
    return clamp(score)


def score_theme_mapping(theme: dict[str, Any]) -> tuple[float, str | None, bool]:
    tags = theme.get("theme_tags") or []
    verified = bool(theme.get("theme_seed_verified", False))
    if not tags:
        return 0.0, None, True
    # Phase1 proxy. Verified theme is Phase2; here usually unverified.
    return (7.0 if verified else 5.5), str(tags[0]), not verified


def build_completeness(payload: dict[str, Any]) -> DataCompleteness:
    return DataCompleteness(
        blackhorse_gene=bool(payload.get("gene")),
        sector_ignition=bool(payload.get("sector")),
        vol_price_preload=bool(payload.get("market")),
        theme_seed=bool(payload.get("theme", {}).get("theme_seed_verified", False)),
        smart_money=bool(payload.get("smart_money")),
        micro_absorption=bool(payload.get("micro_absorption")),
    )


def evaluate_d_band(payload: dict[str, Any], config: DBandConfig | None = None) -> DBandReport:
    config = config or load_config()
    code = str(payload.get("code", ""))
    name = str(payload.get("name", ""))
    # default Asia/Shanghai/Tokyo-like +08 for A-share reports; callers may override timestamp.
    timestamp = str(payload.get("timestamp") or datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"))

    completeness = build_completeness(payload)

    gene_result = score_blackhorse_gene(payload.get("gene", {})) if completeness.blackhorse_gene else None
    sector_result = score_sector_ignition(payload.get("sector", {})) if completeness.sector_ignition else None
    vol_score = score_vol_price_preload(payload.get("market", {})) if completeness.vol_price_preload else None
    theme_score, theme_seed, theme_unverified = score_theme_mapping(payload.get("theme", {}))

    gene_score = gene_result.total_score if gene_result else 0.0
    sector_score_0_10 = sector_result.total_score_0_10 if sector_result else 0.0
    raw = (
        gene_score * config.weights["blackhorse_gene"]
        + sector_score_0_10 * config.weights["sector_ignition"]
        + (vol_score or 0.0) * config.weights["vol_price_preload"]
        + theme_score * config.weights["theme_mapping"]
    )
    score_ceiling = 10.0
    caps_applied: list[str] = []
    if not completeness.theme_seed:
        score_ceiling = min(score_ceiling, float(config.caps["missing_theme_seed_score_ceiling"]))
        caps_applied.append("missing_theme_seed_score_ceiling")
    final = min(raw, score_ceiling)

    decision = apply_phase1_lifecycle(
        d_early_score=final,
        blackhorse_gene_score=gene_score if gene_result else None,
        sector_ignition_score=sector_result.normalized_score if sector_result else None,
        vol_price_preload_score=vol_score,
        completeness=completeness,
        config=config,
    )
    caps_applied.extend([c for c in decision.caps_applied if c not in caps_applied])

    # Contract hardening: paper only.
    execution_mode = decision.execution_mode
    allowed_action = decision.allowed_action
    if execution_mode not in {ExecutionMode.NONE, ExecutionMode.PAPER}:
        execution_mode = ExecutionMode.PAPER
        caps_applied.append("phase1_forced_paper")
    if allowed_action in {AllowedAction.HUMAN_CONFIRM_PROBE, AllowedAction.HUMAN_CONFIRM_ENTRY}:
        allowed_action = AllowedAction.PAPER_PROBE_PLAN
        caps_applied.append("phase1_blocked_executable_action")

    forbidden = [
        "实盘追入",
        "重仓",
        "把 WATCH 当 ENTRY",
        "把 D3_CANDIDATE 当 IGNITION_READY",
    ]
    breakdown = ScoreBreakdown(
        blackhorse_gene=gene_score if gene_result else None,
        sector_ignition=sector_score_0_10 if sector_result else None,
        vol_price_preload=vol_score,
        theme_mapping=theme_score,
        raw_score=round(raw, 2),
        final_score=round(final, 2),
    )
    report = DBandReport(
        code=code,
        name=name,
        timestamp=timestamp,
        d_lifecycle_stage=decision.stage,
        d_stage_variant=decision.stage_variant,
        d_early_score=round(final, 2),
        d_early_score_ceiling=score_ceiling,
        d_confirm_score=None,
        execution_mode=execution_mode,
        allowed_action=allowed_action,
        real_trade_allowed=False,
        data_completeness=completeness,
        score_breakdown=breakdown,
        theme_seed=theme_seed,
        theme_unverified=theme_unverified,
        sector_ignition=bool(sector_result.is_ignition) if sector_result else False,
        next_triggers=decision.next_triggers,
        forbidden=forbidden,
        caps_applied=caps_applied,
        warnings=decision.warnings + ((gene_result.notes if gene_result else []) or []),
    )
    report.validate_phase1()
    return report
