"""
Z2天师 Hermes — 研究主引擎
核心: 从记忆增强到研究产出，全程受不变量约束。

模式:
  - hermes 增强模式: 有记忆时 → 记忆检索 → 增强推理 → ResearchInsight
  - fallback 模式:  记忆库空或出错 → 普通 LLM 推理 → ResearchInsight
"""
from __future__ import annotations

from typing import Any

from contracts.research_contracts import (
    ResearchRequest, ResearchInsight, ResearchHypothesis,
    Z8InputSuggestion, ResearchSkillCandidate
)
from hermes.memory_bank import get_memory_bank, ResearchMemoryBank
from hermes.invariants import validate_research_insight, validate_z8_suggestion


class HermesResearchKernel:
    """Z2天师的研究内核 — 学习型, 带长期记忆"""

    def __init__(self):
        self.memory: ResearchMemoryBank = get_memory_bank()

    # ═══ 主入口 ═══

    def run_research(self, request: ResearchRequest) -> ResearchInsight:
        """
        执行研究任务。
        Hermes 增强模式 or fallback 普通模式。
        """
        try:
            return self._hermes_enhanced_research(request)
        except Exception:
            return self._fallback_research(request)

    # ═══ Hermes 增强模式 ═══

    def _hermes_enhanced_research(self, request: ResearchRequest) -> ResearchInsight:
        fingerprint = self.memory._fingerprint(request.task_type, request.symbol)
        prior = self.memory.retrieve(fingerprint)

        # 从记忆增强推理 (这里是框架, 实际推理由上层 LLM 完成)
        ctx = self._build_context(request, prior)

        # ⚠️ 实际研究推理在上层 (OpenClaw LLM) 执行
        # 这里只负责记忆检索和上下文构建
        insight = ResearchInsight(
            symbol=request.symbol,
            name=request.name,
            research_summary=f"[Hermes增强] {request.task_type} 研究 for {request.symbol}",
            evidence_missing_warning=None if (prior and prior.get("insight", {}).get("evidence")) else (
                "首次研究, 无历史记忆" if not prior else "历史记忆存在但无证据记录"
            ),
            confidence=prior.get("decayed_confidence", 0.5) if prior else 0.3,
        )

        # 强制验证
        violations = validate_research_insight(insight)
        if violations:
            insight = ResearchInsight(
                symbol=request.symbol, name=request.name,
                research_summary=f"研究输出被不变量拦截: {'; '.join(violations)}",
                confidence=0.0,
                evidence_missing_warning="invariant_violation",
            )

        return insight

    def _build_context(self, request: ResearchRequest, prior: dict | None) -> dict[str, Any]:
        """构建增强研究的上下文"""
        ctx = {
            "request": request,
            "has_prior_memory": prior is not None,
        }
        if prior:
            ctx["prior_confidence"] = prior.get("decayed_confidence", 0.5)
            ctx["prior_insight"] = prior.get("insight", {})
            ctx["prior_updated"] = prior.get("updated_at", "")
        return ctx

    # ═══ Fallback 模式 ═══

    def _fallback_research(self, request: ResearchRequest) -> ResearchInsight:
        return ResearchInsight(
            symbol=request.symbol,
            name=request.name,
            research_summary=f"[Fallback] {request.task_type} 研究 for {request.symbol} — Hermes 内核暂不可用",
            confidence=0.3,
            evidence_missing_warning="hermes_fallback_mode",
        )

    # ═══ 辅助 ═══

    def retrieve_research_memory(self, task_type: str, symbol: str) -> dict | None:
        fingerprint = self.memory._fingerprint(task_type, symbol)
        return self.memory.retrieve(fingerprint)

    def build_z8_input_suggestion(self, insight: ResearchInsight, symbol: str) -> Z8InputSuggestion:
        suggestion = Z8InputSuggestion(
            symbol=symbol,
            research_confidence=insight.confidence,
            suggested_role=insight.suggested_role,
            risk_flags=[],
            action_hint=insight.suggested_action_hint,
        )
        violations = validate_z8_suggestion(suggestion)
        if violations:
            suggestion = Z8InputSuggestion(
                symbol=symbol,
                research_confidence=0.0,
                risk_flags=["invariant_violation"],
                action_hint="WATCH",
            )
        return suggestion

    def store_insight(self, request: ResearchRequest, insight: ResearchInsight) -> str:
        """将研究 Insight 写入记忆库"""
        fingerprint = self.memory._fingerprint(request.task_type, request.symbol)
        return self.memory.store(
            fingerprint,
            {
                "symbol": insight.symbol,
                "name": insight.name,
                "thesis": insight.thesis,
                "anti_thesis": insight.anti_thesis,
                "confidence": insight.confidence,
            },
            confidence=insight.confidence,
        )

    # ═══ 统计 ═══

    def memory_stats(self) -> dict[str, Any]:
        return self.memory.stats()


# 全局单例
_kernel: HermesResearchKernel | None = None


def get_hermes_kernel() -> HermesResearchKernel:
    global _kernel
    if _kernel is None:
        _kernel = HermesResearchKernel()
    return _kernel
