"""ZC35 — 催化生命周期域 (v2.1 Enhanced)

v2.1 新增 (基于Top 50大数据实证):
- classify_true_signal() — 真信号三要素判定
- classify_false_signal() — 假信号四型态分类
- compute_signal_strength() — 综合信号强度计算
- get_sector_profile() — 行业催化规律档案
- methodology.py — 完整方法论文档

SEAT_04_CATALYST_TRACKER + SEAT_06_EVENT_SPECIALIST
"""
from zmatrix.zc35.catalyst_lifecycle import (
    CatalystLifecycleEngine,
    CATALYST_TAXONOMY,
    SENTIMENT_PHASES,
    LIFECYCLE,
)
__all__ = ["CatalystLifecycleEngine", "CATALYST_TAXONOMY", "SENTIMENT_PHASES", "LIFECYCLE"]
