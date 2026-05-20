"""
Z2天师 Hermes — Z9学习适配器
只接收 Z9扫地僧归因后的 ReviewEvent，不直接从盈亏学习。
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from contracts.research_contracts import (
    ResearchSkillCandidate, PromptPatchDraft
)
from hermes.memory_bank import get_memory_bank


@dataclass
class ReviewEvent:
    """Z9 归因后的复盘事件"""
    review_id: str
    trading_day: str
    symbol: str = ""
    pattern: str = ""                  # REJECTION_RATE_HIGH | MISSED_DRIVERS | SLIPPAGE | ...
    deviation_magnitude: float = 0.0   # 偏差幅度
    pattern_frequency: int = 0         # 同类模式出现次数
    missed_drivers: list[str] = field(default_factory=list)
    recommended_action: str = ""       # Z9 的修复建议
    source_events: list[str] = field(default_factory=list)


class Z9LearningAdapter:
    """天师的学习窗口 — 只接收 Z9扫地僧归因后的数据"""

    def __init__(self, review_store: str | None = None):
        if review_store is None:
            review_store = str(Path(__file__).resolve().parent / "learned_reviews.json")
        self.review_path = Path(review_store)
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not self.review_path.exists():
            self.review_path.write_text(json.dumps([], ensure_ascii=False))

    # ═══ 消费 Z9 Review ═══

    def consume_z9_review(self, review: ReviewEvent) -> list[Any]:
        """
        输入: Z9 归因后的 ReviewEvent
        → 决定是否生成 MemoryCandidate / SkillCandidate / PromptPatchDraft
        → 不会自动生效
        """
        candidates = []

        # 记录到本地日志
        self._log_review(review)

        # 规则1: 偏差 > 20% → 生成技能候选
        if review.deviation_magnitude > 0.2:
            skill = ResearchSkillCandidate(
                skill_name=f"review_{review.pattern}_{review.symbol}",
                trigger=f"检测到 {review.pattern} 模式",
                learned_from_events=review.source_events,
                proposed_research_steps=self._derive_steps(review),
                confidence=min(0.9, review.pattern_frequency * 0.15),
            )
            candidates.append(skill)

        # 规则2: 同类模式 ≥ 3次 → 生成记忆候选 + 提示词补丁
        if review.pattern_frequency >= 3:
            memory = self._build_memory_suggestion(review)
            candidates.append(memory)

            if review.pattern in ("REJECTION_RATE_HIGH", "MISSED_DRIVERS"):
                patch = PromptPatchDraft(
                    target_prompt="research_template",
                    proposed_change=f"增加 {review.pattern} 维度的检查步骤",
                    reason=f"Z9发现 {review.pattern} 模式出现 {review.pattern_frequency} 次",
                    learned_from=review.source_events,
                )
                candidates.append(patch)

        return candidates

    def _derive_steps(self, review: ReviewEvent) -> list[str]:
        """从 Review 推导研究步骤修正"""
        steps = []
        if review.pattern == "REJECTION_RATE_HIGH":
            steps = ["重新评估顺风信号阈值", "检查是否遗漏关键逆风因子", "降低该链的初始置信度"]
        elif review.pattern == "MISSED_DRIVERS":
            steps = [f"在研究模板中加入 {d} 维度" for d in review.missed_drivers]
        elif review.pattern == "SLIPPAGE":
            steps = ["估值范围加宽10%缓冲", "检查成交价与VWAP偏离"]
        return steps

    def _build_memory_suggestion(self, review: ReviewEvent) -> dict:
        return {
            "type": "MemoryCandidate",
            "fingerprint": f"z9_learned:{review.pattern}:{review.symbol}",
            "pattern": review.pattern,
            "frequency": review.pattern_frequency,
            "approval_required": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    # ═══ 查询 ═══

    def get_pending_candidates(self) -> list[dict]:
        """获取所有待审批的候选"""
        reviews = json.loads(self.review_path.read_text())
        return [r for r in reviews if r.get("approval_status") == "pending"]

    def mark_approved(self, candidate_id: str, approved_by: str = "Z9") -> bool:
        """标记候选为已审批"""
        reviews = json.loads(self.review_path.read_text())
        for r in reviews:
            if r.get("id") == candidate_id:
                r["approval_status"] = "approved"
                r["approved_by"] = approved_by
                r["approved_at"] = datetime.now(timezone.utc).isoformat()
                self.review_path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2))
                return True
        return False

    # ═══ 内部 ═══

    def _log_review(self, review: ReviewEvent) -> None:
        reviews = json.loads(self.review_path.read_text())
        reviews.append({
            "id": review.review_id,
            "trading_day": review.trading_day,
            "symbol": review.symbol,
            "pattern": review.pattern,
            "frequency": review.pattern_frequency,
            "approval_status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        self.review_path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2))
