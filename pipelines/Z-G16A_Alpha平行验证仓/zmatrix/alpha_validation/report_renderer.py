from __future__ import annotations

from .contracts import SettlementReport, ValidationPlan, AlphaValidationPosition, MarkToMarketSnapshot, LLMCoachReport


class AlphaValidationReportRenderer:
    def render_plan(self, plan: ValidationPlan) -> str:
        return f"""# Alpha 平行验证计划

- 验证ID：{plan.validation_id}
- 标的：{plan.symbol} {plan.name}
- 角色：{plan.primary_role}
- 验证假设：{plan.human_hypothesis}
- 幽灵基准：{plan.ghost_benchmark.symbol} {plan.ghost_benchmark.name}
- 观察周期：{plan.planned_horizon_days} 日
- 最大可接受回撤：{plan.max_acceptable_drawdown:.2%}
- 失效条件：{'; '.join(plan.invalidation_conditions)}
- 世界：{plan.world}

> 本计划不生成真实订单，不写入真实账户。"""

    def render_mark(self, mark: MarkToMarketSnapshot) -> str:
        return f"""# Alpha 盯市快照

- 验证ID：{mark.validation_id}
- 日期：{mark.mark_date}
- 个股收益：{mark.stock_return:.2%}
- 基准收益：{mark.benchmark_return:.2%}
- 主动收益：{mark.active_return:.2%}
- 最大不利：{mark.max_adverse_return:.2%}
- 最大有利：{mark.max_favorable_return:.2%}
- 触发条件：{', '.join(mark.triggered_conditions) if mark.triggered_conditions else '无'}
"""

    def render_settlement(self, report: SettlementReport) -> str:
        return f"""# Alpha 平行验证结算

- 验证ID：{report.validation_id}
- 平仓原因：{report.close_reason}
- 个股收益：{report.stock_return:.2%}
- 基准收益：{report.benchmark_return:.2%}
- 主动收益：{report.active_return:.2%}
- 风险调整主动收益：{report.risk_adjusted_active_return:.2f}
- 成本拖累：{report.cost_drag:.2%}
- 持有天数：{report.holding_days}
- 假设遵守：{report.hypothesis_adherence}
- 中途改规则：{report.rule_changed_midway}
- 结论：{report.verdict}

> 该结果属于 PAPER_WORLD，不得展示为真实账户收益。"""

    def render_coach(self, report: LLMCoachReport) -> str:
        return f"""# AI 复盘教练报告草案

- 报告ID：{report.report_id}
- 期间：{report.period}
- 置信度：{report.confidence}

## 摘要
{report.summary}

## 优势
{chr(10).join('- '+x for x in report.strengths) if report.strengths else '- 样本不足，暂不判定'}

## 盲区
{chr(10).join('- '+x for x in report.blind_spots) if report.blind_spots else '- 暂无明确盲区结论'}

## 训练建议
{chr(10).join('- '+x for x in report.training_suggestions)}

证据验证ID：{', '.join(report.source_validation_ids)}
"""
