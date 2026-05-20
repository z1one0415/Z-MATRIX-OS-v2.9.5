# Z-G16A：Alpha 平行验证仓完整设计蓝图与管线说明书 v1.0

> 版本：Z-G16A-AlphaValidation-v1.0  
> 所属系统：Z-MATRIX-OS v2.9.5  
> 产品名：Alpha 平行验证仓  
> 工程世界：PAPER_WORLD  
> 关键边界：不写真实账本、不生成真实订单、不修改 B/R/D 原始分、不把验证收益伪装成真实收益

---

## 0. 定位纠偏

Z-G16 与 Z-G16A 必须拆开：

| 编号 | 名称 | 职责 |
|---|---|---|
| Z-G16 | V4 纸面执行教练 | 针对单个选定标的生成执行路线、价格区间、信号、仓位节奏、买卖计划、失败回撤 |
| Z-G16A | Alpha 平行验证仓 | 承接纸面执行计划或人工/系统分歧，在真实行情与真实交易约束下做前向验证和操盘画像沉淀 |

Z-G16 负责“计划怎么走”；Z-G16A 负责“这套计划长期是否有 Alpha”。

---

## 1. 产品定义

Alpha 平行验证仓不是普通模拟仓，也不是游戏训练账户。它是在真实资金账户之外运行的隔离验证世界，用来承接：

- 系统认为还不能进入真实仓的候选动作；
- 人类有直觉但证据不足的观察票；
- Human 与 System 发生分歧的判断；
- 负 Alpha、样本不足、基准争议下需要继续前向观察的策略。

一句话定义：

```text
用真实行情和真实交易约束，验证一笔投资判断能否产生 Alpha，并长期提炼人类操盘者的判断画像。
```

它验证三件事：

| 层级 | 验证对象 | 核心问题 |
|---|---|---|
| 标的验证 | 股票 / ETF / 板块 / 策略假设 | 如果进入真实仓，会不会跑赢幽灵基准 |
| 判断验证 | Human 与 System 的分歧 | 人类直觉在哪些场景有效，哪些场景容易错 |
| 画像训练 | 人类操盘行为 | 用户优势、盲区、纪律问题和 Alpha 来源是什么 |

---

## 2. 三世界隔离

| 世界 | 用途 | 是否影响真实账户 |
|---|---|---|
| TRAINING_WORLD | 历史行情训练和游戏化学习 | 否 |
| PAPER_WORLD | Alpha 平行验证仓，真实行情下的前向验证 | 否 |
| REAL_WORLD | 真实资金账户和真实交易审计 | 是 |

Z-G16A 只属于 `PAPER_WORLD`。

硬规则：

```text
不写入 Real ledger。
不修改真实账户真值。
不修改 policy。
不修改 B/R/D 原始分。
不生成真实订单。
不把验证仓收益展示为真实收益。
不把 Training 的游戏成绩替代 Alpha 平行验证仓数据。
不把 Alpha 平行验证仓结果伪装成 Real Alpha。
```

---

## 3. 进入条件

入口不应是孤立页面，而应嵌入日常动作流：

| 来源 | 触发 |
|---|---|
| Calm Cockpit 首页 | 持仓或候选动作显示“加入 Alpha 平行验证仓” |
| 专业版驾驶舱 | Gate 阻断、负 Alpha、样本不足、基准争议 |
| Alpha 宇宙试炼 | 历史训练结束后，进入真实行情前向验证 |
| LLM 工作室蓝军 | 蓝军指出风险，需要进入验证仓观察 |
| Human 手动创建 | 用户有直觉票，需要隔离验证 |
| System 自动降级 | ENTER / HUMAN_CONFIRM 被降级为 PAPER_PROBE / WATCH |
| Z-G16 纸面执行教练 | 用户选择将某条纸面路线送入前向验证 |

进入前必须生成验证计划：

```text
验证对象
primary_role
验证假设
幽灵基准
计划观察周期
失效条件
最大可接受回撤
是否与系统意见分歧
人类理由
系统判决摘要
```

没有验证假设、没有幽灵基准、没有失效条件的动作不得进入验证仓。

---

## 4. 生命周期

```text
Create Candidate
→ Build Validation Plan
→ Open Alpha Parallel Position
→ Mark to Market
→ Human/System Interventions
→ Close or Expire
→ Alpha Settlement
→ LLM Reflection
→ Human Pattern Update
→ Promote / Continue / Retire / ETF Substitute Review
```

### 4.1 创建验证计划

验证计划必须回答：

```text
我为什么要观察它？
我认为市场会验证什么？
什么结果说明我错了？
它应该跑赢哪个基准？
如果它跑赢了，是选股能力，还是板块 Beta？
```

### 4.2 开仓

开仓必须遵守真实交易约束：资金约束、T+1、手数、停牌、涨跌停、手续费、印花税、滑点、冲击成本。系统记录的是“如果用真实规则执行，会发生什么”，不是理想成交。

### 4.3 盯市

每个交易日或关键节点记录：个股收益、幽灵基准收益、主动收益、最大不利收益率、最大有利收益率、是否触发失效条件、是否出现系统新判决、Human 是否覆盖、延迟或改变假设。

### 4.4 平仓或到期

平仓原因必须结构化：

| 原因 | 说明 |
|---|---|
| hypothesis_confirmed | 假设被验证 |
| hypothesis_failed | 假设失败 |
| stop_loss | 跌破验证仓止损 |
| benchmark_underperform | 跑输幽灵基准 |
| system_blocked | 系统阻断继续持有 |
| human_changed_mind | 人类改变判断 |
| expired | 到达计划观察期 |
| data_invalid | 数据质量失效 |

### 4.5 结算

结算区分：价格收益、基准收益、主动收益、风险调整后收益、交易成本、是否遵守原始假设、是否因为中途改规则导致结论失真。

---

## 5. 核心数据模型

### 5.1 ValidationPlan

关键字段：

```text
validation_id
world = PAPER_WORLD
symbol / name
primary_role / role_candidates
human_hypothesis
ghost_benchmark
planned_horizon_days
max_acceptable_drawdown
invalidation_conditions
source / source_proposal_id
system_verdict_at_entry
human_confidence / human_reason
evidence_pack_id
module_versions
```

### 5.2 AlphaValidationPosition

关键字段：

```text
validation_id
paper_trade_id
world = PAPER_WORLD
entry_price
entry_benchmark_price
quantity
fees / slippage / cost
max_adverse_return
max_favorable_return
status
```

### 5.3 HumanValidationDecision

关键字段：

```text
decision_type = OPEN / ADD / REDUCE / HOLD / CLOSE / CHANGE_HYPOTHESIS
system_suggestion
human_decision
reason_code
human_reason
confidence
acknowledged_risks
linked_evidence_ids
```

### 5.4 MarkToMarketSnapshot

关键字段：

```text
stock_return
benchmark_return
active_return
max_adverse_return
max_favorable_return
triggered_conditions
system_verdict
```

### 5.5 SettlementReport

关键字段：

```text
stock_return
benchmark_return
active_return
risk_adjusted_active_return
cost_drag
holding_days
hypothesis_adherence
rule_changed_midway
verdict
```

---

## 6. 管线代码职责

| 文件 | 职责 |
|---|---|
| contracts.py | dataclass / enum / schema 边界 |
| policy.py | 三世界隔离、禁止真实订单、必填验证条件 |
| ghost_benchmark.py | 幽灵基准绑定与收益计算 |
| validation_plan_builder.py | 从 OpenClaw payload 构造验证计划 |
| paper_adapter.py | 简化 PAPER_WORLD fill，不连接券商 |
| ledger.py | append-only JSONL 账本 |
| mark_to_market.py | 盯市、主动收益、触发条件 |
| settlement.py | 结算与晋级/淘汰判定 |
| human_pattern.py | 样本级操盘画像特征 |
| llm_coach.py | LLM 复盘教练草案生成器 |
| report_renderer.py | Markdown 报告输出 |
| pipeline.py | Z-G16A 应用服务 API |
| cli.py | OpenClaw/LangGraph 调用入口 |

---

## 7. OpenClaw / LangGraph 固化接口

OpenClaw 不应直接修改账本，也不应绕过 Z-G16A pipeline。推荐只调用 CLI：

```bash
python -m zmatrix.alpha_validation.cli create_plan --store ./data/alpha_events.jsonl --payload ./payload.json
python -m zmatrix.alpha_validation.cli open        --store ./data/alpha_events.jsonl --payload ./open.json
python -m zmatrix.alpha_validation.cli mark        --store ./data/alpha_events.jsonl --payload ./mark.json
python -m zmatrix.alpha_validation.cli decision    --store ./data/alpha_events.jsonl --payload ./decision.json
python -m zmatrix.alpha_validation.cli settle      --store ./data/alpha_events.jsonl --payload ./settle.json
python -m zmatrix.alpha_validation.cli coach       --store ./data/alpha_events.jsonl --payload ./coach.json
```

---

## 8. 必须禁止

```text
禁止真实订单。
禁止 REAL_WORLD 写账。
禁止删除失败样本。
禁止 LLM 修改 active return。
禁止自动晋级真实仓。
禁止用没有样本证据的语言给用户贴心理标签。
禁止把验证仓收益说成真实收益。
```

---

## 9. 与 Z-G16 的关系

```text
Z-G16 = 纸面执行教练，输出 PaperExecutionCoachPlan。
Z-G16A = Alpha 平行验证仓，接收计划/候选/人工分歧进入 PAPER_WORLD 前向验证。
```

推荐链路：

```text
Z-G16 纸面执行计划
→ 用户选择进入验证仓
→ Z-G16A 创建 ValidationPlan
→ PaperExecutionAdapter 打开 PAPER_WORLD 位置
→ MarkToMarket
→ Settlement
→ HumanPattern
→ LLMCoachReport
```

---

## 10. 验收标准

第一阶段必须满足：

```text
能创建验证计划；
每个计划必须绑定幽灵基准；
能打开 PAPER_WORLD 位置；
能盯市并计算主动收益；
能结构化记录人类决策；
能结算并输出 promote / continue / retire / ETF substitute review；
能生成 LLMCoachReport 草案；
不污染真实账本。
```

第二阶段应补：

```text
真实 PaperExecutionSimulator 接入；
幽灵基准行情自动更新；
专业版 UI；
Human/System 分歧胜率；
按 B/R/D/OKR 角色拆画像；
Z9 统计显著性；
本地隐私与脱敏策略。
```

---

## 11. 最终冻结句

```text
Z-G16A 不是 Z-G16，也不是普通模拟仓。

Z-G16A 是 Alpha 平行验证仓：
它把不能进入真实仓、但值得前向观察的判断，放入 PAPER_WORLD，
用真实行情、真实交易约束和幽灵基准，长期验证是否存在 Alpha，
并沉淀人类操盘画像。
```
