# ZC Numbering Map v1.1 — Post-RC1

## Governance Principle

ZC编号是Z-MATRIX-OS系统能力的**唯一主键**。每个ZC编号对应一个独立系统能力模块。禁止编号复用。

## ZC Numbering Main Chain

| 编号 | 标准名称 | 功能定位 | 当前状态 | 对应IRF |
|:--:|------|------|------|:--:|
| ZC00 | Parser-Scorer Split | LLM事实解析 + Python确定性评分 | ACTIVE_PROTOCOL | ALL |
| ZC10 | Research Council | 12专家研究院，多角色审查去幻觉 | INTEGRATION_DONE | IRF-01 |
| ZC20 | DataForge | 数据证据熔炉，PIT，EvidenceCard，跨源校验 | DEPTH_PARTIAL | IRF-01/02/08 |
| ZC30 | FactorFactory | IC/RankIC/Decile/T20/T60/PromotionGate | DEPTH_PARTIAL | IRF-03/07/08 |
| ZC31 | MultiStrategy Sleeve | 多策略套桶，权重生命周期，策略组合治理 | SMOKE_DONE | IRF-07 |
| ZC32 | Portfolio Optimizer | 组合优化，协方差，风险平价 | RESERVED | — |
| ZC35 | Catalyst Lifecycle | 催化生命周期，半衰期，利好出尽，催化真空 | SMOKE_DONE | IRF-01 |
| ZC40 | ExecutionQuality | 涨跌停，停牌，滑点，可成交性 | DEPTH_PARTIAL | IRF-04 |
| ZC45 | Proxy Hedge | 代理防御，Beta预算，避险配置预览 | SMOKE_DONE | IRF-05/06 |
| ZC50 | AccountGovernance | 资金曲线，持仓Alpha，风险预算，动作权限 | DEPTH_PARTIAL | IRF-05/06 |
| ZSC | Audit Export | 审计包，OutputEnvelope，Traceability | INTEGRATION_DONE | ALL |

## ZC30 Numbering Correction

**历史错误**: `ZC30` 曾被同时用于 FactorFactory 和 MultiStrategy Sleeve。

**修正**:
- `ZC30` = **FactorFactory** (唯一)
- `ZC31` = **MultiStrategy Sleeve** (新分配)
- `ZC32` = **Portfolio Optimizer** (预留)
- `ZC30_MULTI_STRATEGY_SLEEVE_WEIGHT_LIFECYCLE_V10` = **DEPRECATED_ALIAS_OF_ZC31**

## Status Definitions

| Status | Meaning |
|--------|---------|
| ACTIVE_PROTOCOL | 系统运行协议，非可选 |
| INTEGRATION_DONE | 功能完整集成，通过测试 |
| DEPTH_PARTIAL | 核心功能可用，深层细化待完成 |
| SMOKE_DONE | 基础链路通过，完整验证待完成 |
| RESERVED | 编号预留，未实现 |
| PLANNED_NOT_IMPLEMENTED | 计划中，未落地 |
| RESEARCH_PROTOTYPE_EXCLUDED_FROM_RC1 | 研究原型，不在RC1范围内 |

## ZC to IRF Mapping

| ZC | IRF Chain | User Scenario |
|----|-----------|---------------|
| ZC00 | ALL | 所有操作基础协议 |
| ZC10 | IRF-01 | 个股深度研究 → 12专家审查 |
| ZC20 | IRF-01/02/08 | 数据校验 → 月度全市场扫描 |
| ZC30 | IRF-03/07/08 | 因子验证 → 多策略组合 |
| ZC31 | IRF-07 | 策略组合 → 权重管理 |
| ZC35 | IRF-01 | 催化事件 → 买卖时机辅助 |
| ZC40 | IRF-04 | 订单执行 → 可成交性检查 |
| ZC45 | IRF-05/06 | 风险对冲 → 账户审查 |
| ZC50 | IRF-05/06 | 资金管理 → 组合Alpha审查 |
| ZSC | ALL | 审计追溯 → 全链路 |

## Prohibition

禁止未来复用已占用的ZC编号。新增能力必须分配新编号。
