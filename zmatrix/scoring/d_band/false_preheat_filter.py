from __future__ import annotations

from .m1_data_contracts import LateDayAnomalyResult, LateDayAnomalyType, M1FeaturePack, M1Usability


def detect_false_preheat(
    stock_features: M1FeaturePack,
    index_features: M1FeaturePack | None = None,
    sector_confirmed: bool = False,
    late_gain_contribution_threshold: float = 0.70,
    high_volume_share_threshold: float = 0.30,
    index_divergence_drop_pct: float = -0.50,
) -> LateDayAnomalyResult:
    """Classify late-day anomaly.

    Late-day lifting is not always fake.  Volume-backed strength against a weak
    index is classified as SMART_MONEY_TAIL_GRAB and still requires next-day
    validation.  Shrinking/unsupported late-day lift is FALSE_PREHEAT.
    """

    metrics = stock_features.to_dict()
    reasons: list[str] = []
    if stock_features.data_quality.usability == M1Usability.UNUSABLE:
        return LateDayAnomalyResult(
            anomaly_type=LateDayAnomalyType.UNCERTAIN_LATE_DAY_ANOMALY,
            false_preheat=False,
            smart_money_tail_grab=False,
            volume_price_preload_penalty=0.0,
            cooldown_days=0,
            requires_next_day_validation=True,
            allowed_action="WATCH",
            reason=["m1_data_unusable"],
            metrics=metrics,
        )
    late_dominates = stock_features.late_day_gain_contribution >= late_gain_contribution_threshold
    if not late_dominates:
        return LateDayAnomalyResult(
            anomaly_type=LateDayAnomalyType.NONE,
            false_preheat=False,
            smart_money_tail_grab=False,
            volume_price_preload_penalty=0.0,
            cooldown_days=0,
            requires_next_day_validation=False,
            allowed_action="UNCHANGED",
            reason=["late_day_not_dominant"],
            metrics=metrics,
        )
    high_volume = stock_features.late_day_turnover_share >= high_volume_share_threshold
    index_weak = bool(index_features and index_features.late_day_gain_pct <= index_divergence_drop_pct)
    if high_volume and index_weak:
        reasons.extend(["late_day_dominant", "high_volume_tail", "index_divergence_weak"])
        return LateDayAnomalyResult(
            anomaly_type=LateDayAnomalyType.SMART_MONEY_TAIL_GRAB,
            false_preheat=False,
            smart_money_tail_grab=True,
            volume_price_preload_penalty=0.0,
            cooldown_days=0,
            requires_next_day_validation=True,
            allowed_action="WATCH_OR_PAPER",
            reason=reasons,
            metrics=metrics,
        )
    # If sector did not confirm and late-day dominates without high-volume divergence, treat as fake.
    if not sector_confirmed or not high_volume:
        reasons.extend(["late_day_dominant", "sector_not_confirmed" if not sector_confirmed else "not_high_volume"])
        return LateDayAnomalyResult(
            anomaly_type=LateDayAnomalyType.FALSE_PREHEAT,
            false_preheat=True,
            smart_money_tail_grab=False,
            volume_price_preload_penalty=1.0,
            cooldown_days=3,
            requires_next_day_validation=False,
            allowed_action="WATCH_ONLY",
            reason=reasons,
            metrics=metrics,
        )
    return LateDayAnomalyResult(
        anomaly_type=LateDayAnomalyType.UNCERTAIN_LATE_DAY_ANOMALY,
        false_preheat=False,
        smart_money_tail_grab=False,
        volume_price_preload_penalty=0.5,
        cooldown_days=1,
        requires_next_day_validation=True,
        allowed_action="WATCH",
        reason=["late_day_dominant_but_ambiguous"],
        metrics=metrics,
    )
