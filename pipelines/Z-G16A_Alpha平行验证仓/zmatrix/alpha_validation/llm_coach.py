from __future__ import annotations

from typing import Iterable, List

from .contracts import HumanPatternFeature, LLMCoachReport, SettlementReport, Confidence


class LLMCoachDraftBuilder:
    """Evidence-bound coach report draft builder.

    No external LLM call is made here. This module prepares a safe deterministic
    draft that a future LLM may rewrite, while preserving sample_count and source ids.
    """

    def build(self, profile_id: str, period: str, settlements: Iterable[SettlementReport],
              features: Iterable[HumanPatternFeature]) -> LLMCoachReport:
        rows = list(settlements)
        feats = list(features)
        source_ids = [r.validation_id for r in rows]
        n = len(rows)
        avg_active = sum(r.active_return for r in rows) / n if n else 0.0
        confidence = Confidence.LOW.value if n < 8 else Confidence.MEDIUM.value if n < 30 else Confidence.HIGH.value
        strengths = [f.label for f in feats if f.pattern_type == "strength"]
        blind_spots = [f.label for f in feats if f.pattern_type in {"weakness", "bias", "discipline"}]
        suggestions: List[str] = []
        if n < 8:
            suggestions.append("样本不足，暂不做强结论；继续积累同角色验证样本。")
        if avg_active < 0:
            suggestions.append("优先复核幽灵基准选择与入场时点，避免把 Beta 当成 Alpha。")
        else:
            suggestions.append("保留当前有效判断，但继续按 B/R/D/OKR 角色拆分归因。")
        return LLMCoachReport(
            profile_id=profile_id,
            period=period,
            summary=f"本期 Alpha 平行验证样本 {n} 个，平均主动收益 {avg_active:.2%}；置信度 {confidence}。",
            strengths=strengths,
            blind_spots=blind_spots,
            system_disagreements=[],
            training_suggestions=suggestions,
            source_validation_ids=source_ids,
            source_report_ids=[f.feature_id for f in feats],
            confidence=confidence,
        )
