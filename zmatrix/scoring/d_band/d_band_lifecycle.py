from __future__ import annotations

from dataclasses import dataclass

from .d_band_contracts import DBandStage, AllowedAction, ExecutionMode, DataCompleteness
from .d_band_config import DBandConfig


@dataclass(slots=True)
class LifecycleDecision:
    stage: DBandStage
    stage_variant: str
    allowed_action: AllowedAction
    execution_mode: ExecutionMode
    next_triggers: list[str]
    caps_applied: list[str]
    warnings: list[str]


def apply_phase1_lifecycle(
    *,
    d_early_score: float,
    blackhorse_gene_score: float | None,
    sector_ignition_score: float | None,
    vol_price_preload_score: float | None,
    completeness: DataCompleteness,
    config: DBandConfig,
) -> LifecycleDecision:
    caps: list[str] = []
    warnings: list[str] = []
    independent = completeness.independent_signal_count()
    sector_ok = sector_ignition_score is not None and sector_ignition_score >= config.thresholds["sector_ignition"]
    gene_preheat_ok = blackhorse_gene_score is not None and blackhorse_gene_score >= config.thresholds["blackhorse_gene_preheat"]
    gene_d3_ok = blackhorse_gene_score is not None and blackhorse_gene_score >= config.thresholds["blackhorse_gene_d3"]
    vol_d3_ok = vol_price_preload_score is not None and vol_price_preload_score >= config.thresholds["vol_price_preload_d3"]

    if not completeness.blackhorse_gene:
        return LifecycleDecision(
            DBandStage.COLD_IDLE, "D0", AllowedAction.NONE, ExecutionMode.NONE,
            [], ["missing_blackhorse_gene_cap"], ["缺少黑马基因数据，无法进入预热池"]
        )

    if not completeness.sector_ignition:
        return LifecycleDecision(
            DBandStage.THEME_SEED, "D1", AllowedAction.NONE, ExecutionMode.NONE,
            [], ["missing_sector_ignition_cap"], ["缺少板块点火数据，禁止推动升档"]
        )

    if sector_ok and gene_preheat_ok:
        stage = DBandStage.PREHEAT
        action = AllowedAction.WATCH
        mode = ExecutionMode.PAPER
        variant = "D2"
    elif sector_ok:
        stage = DBandStage.THEME_SEED
        action = AllowedAction.WATCH if independent >= 2 and d_early_score >= config.thresholds["watch_score"] else AllowedAction.NONE
        mode = ExecutionMode.PAPER if action != AllowedAction.NONE else ExecutionMode.NONE
        variant = "D1"
    else:
        stage = DBandStage.COLD_IDLE
        action = AllowedAction.NONE
        mode = ExecutionMode.NONE
        variant = "D0"

    if (
        d_early_score >= config.thresholds["d3_candidate_score"]
        and sector_ok
        and gene_d3_ok
        and vol_d3_ok
        and independent >= 2
    ):
        stage = DBandStage.D3_CANDIDATE
        variant = "D3_CANDIDATE"
        action = AllowedAction.PAPER_PROBE_PLAN
        mode = ExecutionMode.PAPER

    if not completeness.theme_seed:
        caps.append("missing_theme_seed_score_ceiling")
        warnings.append("Phase1 使用板块点火替代主题种子，theme_unverified=true")
    if not completeness.smart_money:
        caps.append("missing_smart_money_lifecycle_max_D3_CANDIDATE")
    if not completeness.micro_absorption:
        caps.append("missing_micro_absorption_execution_max_paper")

    next_triggers = [
        "次日不低开杀",
        "放量突破平台",
        "板块继续IGNITION/CONFIRMATION",
        "分时回落承接有效",
        "出现明确主题催化",
    ]
    return LifecycleDecision(stage, variant, action, mode, next_triggers, caps, warnings)
