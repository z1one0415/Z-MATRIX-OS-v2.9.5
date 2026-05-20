from __future__ import annotations

from collections import defaultdict
from typing import Iterable, List

from .contracts import HumanPatternFeature, SettlementReport, Confidence


class HumanPatternAnalyzer:
    """Deterministic sample-based human pattern extraction.

    This intentionally avoids psychological labels. It only emits evidence-bound
    trading behavior features with sample_count and validation ids.
    """

    def analyze_settlements(self, settlements: Iterable[SettlementReport], profile_id: str, window: str) -> List[HumanPatternFeature]:
        rows = list(settlements)
        features: List[HumanPatternFeature] = []
        if not rows:
            return features
        positive = [r for r in rows if r.active_return > 0]
        negative = [r for r in rows if r.active_return <= 0]
        avg_active = sum(r.active_return for r in rows) / len(rows)
        conf = Confidence.LOW.value if len(rows) < 8 else Confidence.MEDIUM.value if len(rows) < 30 else Confidence.HIGH.value
        if avg_active > 0:
            features.append(HumanPatternFeature(
                profile_id=profile_id,
                window=window,
                pattern_type="strength",
                label="验证仓主动收益为正",
                description=f"该窗口内 Alpha 平行验证样本平均主动收益为 {avg_active:.2%}，需继续分角色验证。",
                sample_count=len(rows),
                confidence=conf,
                supporting_validation_ids=[r.validation_id for r in positive],
                counter_examples=[r.validation_id for r in negative[:5]],
            ))
        else:
            features.append(HumanPatternFeature(
                profile_id=profile_id,
                window=window,
                pattern_type="weakness",
                label="验证仓主动收益未显著为正",
                description=f"该窗口内 Alpha 平行验证样本平均主动收益为 {avg_active:.2%}，应优先检查基准选择、买点和过度交易。",
                sample_count=len(rows),
                confidence=conf,
                supporting_validation_ids=[r.validation_id for r in negative],
                counter_examples=[r.validation_id for r in positive[:5]],
            ))
        return features
