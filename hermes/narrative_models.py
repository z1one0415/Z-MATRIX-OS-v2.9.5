"""
Z2天师 Hermes — 情绪与叙事雷达
v1.0: 爬虫采集 → Z2天师自提取 → NarrativeMetrics → L1.6 → EventStore
成本: ~$0.012/次, ~$1/月
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import hashlib


@dataclass
class NarrativeSource:
    channel: str       # cls | xueqiu | taoguba | xuangubao
    url: str
    title: str = ""
    body: str = ""
    timestamp: str = ""
    heat: int = 0


@dataclass
class NarrativeEntropyEvent:
    """L1.6 叙事熵事件 — 写入 EventStore"""
    event_type: str = "NarrativeEntropyEvent"
    source: str = "Z2_Hermes_NarrativeRadar"
    scan_time: str = ""
    sources_scanned: int = 0
    slogan_repetition_ratio: float = 0.0
    marginal_buyer_exhaustion: float = 0.0
    narrative_diversity: float = 0.0
    narrative_acceleration: float = 0.0
    dominant_emotion: str = "neutral"
    top_narratives: list[str] = field(default_factory=list)
    l16_signal: str = ""       # MANIA_WARNING | CAPITULATION | NEUTRAL
    l16_action: str = ""       # RESTRICT_NEW | MARK_OPPORTUNITY | NO_ACTION
    evidence_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "source": self.source,
            "scan_time": self.scan_time,
            "sources_scanned": self.sources_scanned,
            "slogan_repetition_ratio": self.slogan_repetition_ratio,
            "marginal_buyer_exhaustion": self.marginal_buyer_exhaustion,
            "narrative_diversity": self.narrative_diversity,
            "narrative_acceleration": self.narrative_acceleration,
            "dominant_emotion": self.dominant_emotion,
            "top_narratives": self.top_narratives,
            "l16_signal": self.l16_signal,
            "l16_action": self.l16_action,
            "evidence_hash": self.evidence_hash,
        }
