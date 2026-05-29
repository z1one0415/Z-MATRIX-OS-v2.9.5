# Z-MATRIX-OS v4.0｜个人量化投资研究决策使用说明书

> Release: v4.0-rc1 (research-only)
> Tag target: f8796f714740b5e8c76ab53d768888a8de87dfdd

---

## 1. 当前系统定位

Z-MATRIX-OS v4.0-rc1 是一个**个人量化投资研究决策系统**。

- ✅ 投研分析：个股深度研究、行业映射、催化追踪
- ✅ 因子研究：IC/RankIC验证、因子晋级
- ✅ 组合研究：纸面策略验证、风险预算
- ✅ 审计追溯：全链路OutputEnvelope
- ❌ 不做实盘交易
- ❌ 不接券商
- ❌ 不执行自动化买卖

**Production: BLOCKED | Broker/runtime: BLOCKED | Real trade: BLOCKED | Paper-only: TRUE**

---

## 2. ZC 编号主链

| 编号 | 名称 | 状态 | 说明 |
|:--:|------|------|------|
| ZC00 | Parser-Scorer Split | ACTIVE_PROTOCOL | LLM解析 + 确定性评分 |
| ZC10 | Research Council | INTEGRATION_DONE | 12专家研究院 |
| ZC20 | DataForge | DEPTH_PARTIAL | 数据证据熔炉 |
| ZC30 | FactorFactory | DEPTH_PARTIAL | 因子工厂 |
| ZC31 | MultiStrategy Sleeve | SMOKE_DONE | 多策略套桶 |
| ZC32 | Portfolio Optimizer | RESERVED | 组合优化器（预留） |
| ZC35 | Catalyst Lifecycle | SMOKE_DONE | 催化生命周期 |
| ZC40 | ExecutionQuality | DEPTH_PARTIAL | 执行质量 |
| ZC45 | Proxy Hedge | SMOKE_DONE | 代理防御 |
| ZC50 | AccountGovernance | DEPTH_PARTIAL | 账户治理 |
| ZSC | Audit Export | INTEGRATION_DONE | 审计导出 |

---

## 3. ZC00 Parser-Scorer Split

**解决什么问题**: LLM输出不稳定、不可审计。Parser负责提取事实字段，Scorer负责确定性Python评分。

**不解决**: LLM幻觉；主观判断的客观化。

**当前状态**: ACTIVE_PROTOCOL — 所有ZC模块的基础协议。

**典型OpenClaw启动**: `解析XX股票最新财报` → Parser提取事实 → Scorer打分

---

## 4. ZC10 Research Council

**解决什么问题**: 从多专业角度审查研究结论，12位独立审查员（宏观/安全边际/护城河/质量增长/法务审计/反身性/产业链/流动性/因子有效性/过拟合/微观结构/账户生存）。

**不解决**: 直接买卖决策。输出只有：RESEARCH_SUPPORT / RESEARCH_CONFLICT / DATA_INSUFFICIENT / RISK_REVIEW_REQUIRED。

**输入**: 标的代码 + 事实数据
**输出**: ReviewerResult（确定性分数+评分追踪+风险标志）
**禁止项**: BUY/SELL/AUTO_EXECUTE
**对应IRF**: IRF-01

---

## 5. ZC20 DataForge

**解决**: 数据质量校验、PIT时点数据、EvidenceCard、跨源比对。

**当前状态**: DEPTH_PARTIAL — 核心EvidenceCard + FactExtractionStore可用。

**输入**: 标的代码 + 数据源
**输出**: EvidenceCard + DataQualityScore
**对应IRF**: IRF-01 / IRF-02 / IRF-08

---

## 6. ZC30 FactorFactory

**解决**: 因子IC验证、RankIC、Decile分层、T20/T60时序穿透、因子晋级门。

**当前状态**: DEPTH_PARTIAL — OutcomeHorizonIntegrity + FactorPromotionGate可用。

**输入**: 因子定义 + 历史数据
**输出**: FactorPromotionGate结果
**对应IRF**: IRF-03 / IRF-07 / IRF-08

---

## 7. ZC31 MultiStrategy Sleeve

**解决**: 多策略组合管理，策略权重生命周期，策略组合治理。

**不解决**: 组合优化数学（见ZC32）。

**当前状态**: SMOKE_DONE

**对应IRF**: IRF-07

---

## 8. ZC32 Portfolio Optimizer

**状态**: RESERVED — 编号预留，未实现。

**计划能力**: 协方差矩阵、风险平价、有效前沿。当前不可用。

---

## 9. ZC35 Catalyst Lifecycle

**解决**: 催化事件分级、有效期衰减、利好出尽识别、催化真空检测。

**当前状态**: SMOKE_DONE — 基础催化生命周期可用。ZC35-v2.1为Research Prototype，**不在RC1范围内**。

**输入**: 标的代码 + 催化事件
**输出**: CatalystLifecycle评估
**对应IRF**: IRF-01

---

## 10. ZC40 ExecutionQuality

**解决**: 涨跌停板检测、停牌检测、滑点估计、可成交性判断。

**不解决**: 实际订单路由和执行。

**当前状态**: DEPTH_PARTIAL — LimitBoardGate + TransactionCostModel可用。

**对应IRF**: IRF-04

---

## 11. ZC45 Proxy Hedge

**解决**: 代理防御信号、Beta预算、避险配置预览。

**当前状态**: SMOKE_DONE

**对应IRF**: IRF-05 / IRF-06

---

## 12. ZC50 AccountGovernance

**解决**: 资金曲线、持仓Alpha、风险预算上限、动作权限门。

**当前状态**: DEPTH_PARTIAL — CapitalCurve + ActionPermissionGate可用。

**对应IRF**: IRF-05 / IRF-06

---

## 13. ZSC Audit Export

**解决**: 全链路审计追溯，OutputEnvelope + AuditEvent + ZIP导出。

**当前状态**: INTEGRATION_DONE

**对应IRF**: ALL

---

## 14. IRF-01 至 IRF-08 使用场景

| IRF | 名称 | 何时使用 |
|:--:|------|------|
| IRF-01 | 个股机构研究 | 深度分析单只股票 |
| IRF-02 | 月度全市场选股 | 每月全量B-R-D扫描 |
| IRF-03 | 策略验证 | 验证因子/策略有效性 |
| IRF-04 | 纸面执行 | 纸面下单预览 |
| IRF-05 | 账户审查 | 账户风险/收益审查 |
| IRF-06 | 组合Alpha审查 | 组合超额收益分析 |
| IRF-07 | 多策略组合 | 策略组合管理 |
| IRF-08 | 因子数据工厂 | 因子研发+专有数据 |

---

## 15. 个人量化投研日常流程

```
每日盘前 → ZC35催化扫描 → 选股池更新
盘中 → ZC40执行质量监控 → ZC50风险预算
盘后 → ZC10研究审查 → ZC20数据校验 → ZC30因子验证
周末 → ZC31组合再平衡 → IRF-02月度重跑
审计 → ZSC全链路追溯
```

---

## 16. OpenClaw 控制模式

当前通过OpenClaw会话控制Z-MATRIX-OS：

- `超级预测` → 启动预测引擎
- `分析XX股票` → 启动ZC10研究审查
- `验证因子XX` → 启动ZC30因子验证
- `审核XX持仓` → 启动ZC50账户审查

---

## 17. 禁止误用清单

| 误用 | 说明 |
|------|------|
| ~~把Research Council输出当买卖建议~~ | RC只输出研究结论 |
| ~~在D-Matrix未覆盖标的上下单~~ | 需完整数据覆盖 |
| ~~跳过ZC40执行质量检查~~ | 涨跌停/停牌必须检测 |
| ~~在宏观逆风时追高~~ | 遵循MACRO字典信号 |
| ~~AutoCaseForge自动生成测试~~ | **PLANNED_NOT_IMPLEMENTED** |
| ~~使用ZC35-v2.1~~ | Research Prototype, 不在RC1 |
| ~~实盘交易~~ | Production BLOCKED |

---

## 18. 当前能力限制

| 限制 | 说明 |
|------|------|
| AutoCaseForge | PLANNED_NOT_IMPLEMENTED — 不可用 |
| ZC35-v2.1 | Research Prototype — excluded from RC1 |
| ZC32 Portfolio Optimizer | RESERVED — 未实现 |
| DataForge + FactorFactory | DEPTH_PARTIAL — 研究级，非生产级 |
| 实盘交易 | BLOCKED — Paper-only |
| Broker/Runtime | BLOCKED |

---

*V4.0-RC1 research-only. Tag v4.0-rc1 @ f8796f7. Published 2026-05-29.*
