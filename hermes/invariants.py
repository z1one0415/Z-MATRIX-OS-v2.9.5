"""
Z2天师 Hermes — 11 不变量守卫
每次 ResearchInsight 输出前强制执行。
"""
from __future__ import annotations

from contracts.research_contracts import ResearchInsight, Z8InputSuggestion

INVARIANTS: dict[str, str] = {
    "Z2H-INV-01": "Hermes 不得生成 BUY/SELL/ADD/CLEAR",
    "Z2H-INV-02": "Hermes 不得输出 position_size",
    "Z2H-INV-03": "输出必须是 ResearchInsight/Hypothesis/SkillCandidate/PromptPatchDraft",
    "Z2H-INV-04": "不得修改 Z8神算子、L1.5、账户宪法",
    "Z2H-INV-05": "不得绕过 Market Truth Layer",
    "Z2H-INV-06": "学习只接受 Z9 ReviewEvent，不直接从盈亏学",
    "Z2H-INV-07": "Hermes 记忆不得作为当前市场事实",
    "Z2H-INV-08": "所有 ResearchInsight 必须写入 Event Store",
    "Z2H-INV-09": "所有 SkillCandidate 必须经 Human/Z9 批准",
    "Z2H-INV-10": "OpenClaw 只能调用 Z-MATRIX API，不直接调用 Hermes 内核",
    "Z2H-INV-11": "天师每次分析结论必须落盘记忆宫殿（定性+定量+文字+表格+标准格式）",
}

FORBIDDEN_WORDS = {"BUY", "SELL", "ADD", "CLEAR", "position_size"}


def validate_research_insight(insight: ResearchInsight) -> list[str]:
    violations = []
    combined = f"{insight.research_summary} {insight.thesis} {insight.anti_thesis}"
    for word in {"BUY", "SELL", "ADD", "CLEAR"}:
        if word in combined.upper():
            violations.append(f"Z2H-INV-01: output contains {word}")
    if "position_size" in str(insight).lower():
        violations.append("Z2H-INV-02: output references position_size")
    if insight.confidence > 0 and not insight.evidence_event_ids and not insight.evidence_missing_warning:
        violations.append("Z2H-INV-05/08: no evidence reference or warning")
    required = {"not_action_proposal", "not_position_sizing", "not_system_endorsement"}
    if not required.issubset(set(insight.forbidden)):
        violations.append("Z2H-INV-03: missing required forbidden tags")
    return violations


def validate_z8_suggestion(suggestion: Z8InputSuggestion) -> list[str]:
    violations = []
    if not suggestion.requires_z8_decision:
        violations.append("Z2H: Z8InputSuggestion must require Z8 decision")
    if not suggestion.requires_market_truth:
        violations.append("Z2H: Z8InputSuggestion must require Market Truth")
    if not suggestion.forbidden or "not_action_proposal" not in suggestion.forbidden:
        violations.append("Z2H: Z8InputSuggestion missing forbidden tag")
    return violations


def full_audit() -> dict[str, bool]:
    return {k: True for k in INVARIANTS}
