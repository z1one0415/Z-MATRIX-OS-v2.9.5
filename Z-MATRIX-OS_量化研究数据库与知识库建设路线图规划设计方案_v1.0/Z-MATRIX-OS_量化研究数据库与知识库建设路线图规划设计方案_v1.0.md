# Z-MATRIX-OS｜量化研究数据库与知识库建设路线图规划设计方案 v1.0

> **文档定位**：下阶段升级导航与备忘  
> **适用系统**：Z-MATRIX-OS v4.0 FINAL-HARDGATES 之后  
> **核心目标**：把过去 5 年实盘数据、当前研究体系、行业产业链知识、事件催化案例、因子验证结果、账户反馈，沉淀成可长期复用、可审计、可自动更新、可内化为系统记忆的个人量化研究数据库。  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production  
> **第五步状态**：AutoCaseForge v1.0 工程落地执行说明书已完成，纳入本路线图作为“案例记忆与系统内化层”的工程主线。

---

## 0. 总裁决

当前最优路径不是先补 31 个行业板块长篇研究，而是先建立：

```text
5年实盘真相库
→ 行业/产业链映射库
→ Outcome验证库
→ 因子与信号验证库
→ AutoCaseForge案例记忆库
→ 高频赛道深研知识库
→ 31行业骨架库
→ 个人操盘分析建议系统
```

31 个行业板块必须做，但不能作为第一阶段主战场。  
它应该服务于：

```text
1. 个股行业归因
2. 同行业 benchmark 对比
3. 产业链位置判断
4. 板块轮动状态识别
5. 因子横截面验证
6. CaseForge 案例归因
7. 未来候选池生成
```

如果没有账户真相库、信号结果库、Outcome 验证库和 CaseForge 案例库，31 行业研究会变成“知识堆积”，无法判断哪些研究真正提升账户收益。

---

## 1. 当前系统状态与路线前提

### 1.1 系统当前定位

```text
Z-MATRIX-OS v4.0 = 研究平台 / Paper-only / Integration Candidate
```

当前不是：

```text
自动交易系统
生产交易系统
实盘下单系统
全自动操盘机器人
```

所有后续数据库与知识库建设必须继续保持：

```json
{
  "real_trade_allowed": false,
  "broker_order_allowed": false,
  "runtime_enabled": false,
  "auto_buy_allowed": false,
  "auto_sell_allowed": false,
  "production_allowed": false,
  "paper_only": true,
  "human_review_required": true
}
```

### 1.2 当前最关键缺口

目前系统已经有 v4.0 治理、审计、报告、Research Council、ZC35、ZC40、ZC45、ZC50、FactorFactory、DataForge 等骨架，但真正要成长为长期个人研究系统，还缺四类“厚数据”：

```text
1. 过去 5 年实盘交易与账户真相数据
2. 每个信号 / 决策 / 观察对象的后验结果验证
3. 行业、主题、产业链、同类股、基准映射
4. 可自动落盘、可跨案例验证、可内化为记忆的 CaseForge 数据
```

---

## 2. 总体目标架构

最终目标不是做一个“股票资料库”，而是做一个：

```text
Z-MATRIX Proprietary Research Database
= 实盘真相 + 信号验证 + 行业映射 + 财务截面 + 事件催化 + 案例记忆 + 规则候选 + 系统内化
```

它要回答 8 个核心问题：

```text
1. 我过去 5 年到底靠什么赚钱？
2. 我过去 5 年到底因为什么亏钱？
3. 哪些行业、主题、产业链真正贡献了 alpha？
4. 哪些交易只是市场 beta 或板块 beta？
5. 哪些信号有效，哪些信号是假阳性？
6. 哪些机会被我错过，系统为什么没有召回？
7. 哪些规则有跨案例验证，哪些只是单次教训？
8. 我的个人操盘风格、优势、弱点、风险边界是什么？
```

---

## 3. 总路线图

```text
Phase 0：ResearchDB 宪法与目录冻结
Phase 1：5年实盘真相库
Phase 2：标的主数据 + 行业/产业链映射库
Phase 3：行情/基准/Outcome 验证库
Phase 4：FactorFactory 因子与信号验证库
Phase 5：AutoCaseForge 案例记忆与自动内化系统
Phase 6：事件催化与 ZC35 生命周期数据库
Phase 7：财务截面与 B-Matrix 研究数据库
Phase 8：产业链/行业知识库
Phase 9：个人操盘画像与系统建议层
Phase 10：Research Cockpit 与月度内化机制
```

其中：

```text
Phase 5 已完成工程说明书，需要在总路线中作为既定模块接入。
```

---

# Phase 0｜ResearchDB 宪法与目录冻结

## 0.1 阶段目标

先定义数据库的身份、边界、可信度、PIT 规则、生产隔离规则，避免后续数据越积越乱。

## 0.2 必须建立的宪法文件

```text
docs/research_db/
  RESEARCH_DB_CONSTITUTION.md
  DATA_TRUST_LEVEL_POLICY.md
  PIT_SAFETY_POLICY.md
  OUTCOME_HORIZON_POLICY.md
  CASE_MEMORY_POLICY.md
  RESEARCH_DB_PROMOTION_POLICY.md
  NO_PRODUCTION_BOUNDARY.md
```

## 0.3 核心规则

```text
1. 所有数据必须标记 source、as_of_date、ingested_at。
2. 所有历史回测字段必须声明 pit_safe。
3. 当前截面数据不得伪装成历史 PIT 数据。
4. T20 必须严格 20 个 forward trading days。
5. T60 必须严格 60 个 forward trading days。
6. 不足窗口不得用最后价格替代。
7. 单案例只能形成 lesson，不能形成 rule。
8. 任何研究数据不得直接进入 production。
```

## 0.4 产出

```text
ResearchDB 总宪法
数据可信度分级
PIT 规则
Outcome Horizon 规则
Promotion 规则
No Production 硬边界
```

## 0.5 验收标准

```text
1. 目录存在。
2. 宪法文件存在。
3. 所有规则有测试/verify。
4. 不改变 RC1 / production 状态。
```

---

# Phase 1｜5年实盘真相库

## 1.1 阶段目标

把过去 5 年实盘数据整理成 Z-MATRIX 的“账户真相底座”。

优先级最高。  
因为所有研究最终都必须被账户结果检验。

## 1.2 必须建立的数据表

```text
data/research_db/account/
  account_daily_snapshot.csv
  trade_ledger.csv
  position_ledger.csv
  cashflow_ledger.csv
  holding_pnl_ledger.csv
  account_drawdown_ledger.csv
  capital_curve.csv
```

## 1.3 trade_ledger 必填字段

```csv
trade_id,ticker,name,trade_date,side,price,quantity,amount,fee,stamp_duty,slippage,source,thesis_id,signal_id,account_id
```

## 1.4 position_ledger 必填字段

```csv
date,ticker,name,quantity,market_value,cost_basis,unrealized_pnl,realized_pnl,position_pct,holding_days,thesis_id
```

## 1.5 account_daily_snapshot 必填字段

```csv
date,total_equity,cash,market_value,daily_pnl,cumulative_return,max_drawdown,exposure,turnover
```

## 1.6 必须补的标签

```text
trade_role:
  LONG_TERM_CORE
  MID_TERM_ROTATION
  SHORT_TERM_EVENT
  WATCH_ONLY
  MISTAKE_REVIEW

action_type:
  BUY
  SELL
  REDUCE
  ADD
  WATCH
  PASS
  MANUAL_OVERRIDE

data_status:
  REAL_ACCOUNT
  MANUAL_IMPORT
  PARTIAL_RECONSTRUCTED
  ESTIMATED
```

## 1.7 产出

```text
5年账户收益曲线
每笔交易净收益
持仓期间最大回撤
交易频率与换手
交易按行业/主题/时间归因
```

## 1.8 验收标准

```text
1. 能重建每一天账户权益。
2. 能追溯每笔交易。
3. 能计算单笔交易真实净收益。
4. 能计算持仓周期与回撤。
5. 能输出年度 / 月度 / 行业 / 个股 PnL。
```

---

# Phase 2｜标的主数据 + 行业/产业链映射库

## 2.1 阶段目标

让每只股票能被系统正确归入：

```text
行业
二级行业
三级行业
主题
产业链
产业链位置
同类公司
基准指数
主题篮子
```

这一步是 31 行业研究的前置底座。

## 2.2 必须建立的数据表

```text
data/research_db/universe/
  security_master.csv
  industry_classification.csv
  chain_mapping.csv
  theme_mapping.csv
  peer_group_mapping.csv
  benchmark_mapping.csv
  stock_role_mapping.csv
```

## 2.3 security_master 字段

```csv
ticker,name,exchange,listing_date,listing_status,market_cap_float,market_cap_total,sw_l1,sw_l2,sw_l3
```

## 2.4 chain_mapping 字段

```csv
ticker,chain_id,chain_name,chain_layer,chain_position,value_capture_grade,evidence_grade,updated_at
```

## 2.5 chain_layer 标准

```text
HARDWARE_BOTTLENECK
DELIVERY_PLATFORM
APPLICATION_ADAPTER
RESOURCE_UPSTREAM
CHANNEL_DISTRIBUTION
FINANCIAL_BETA
DEFENSIVE_ANCHOR
```

## 2.6 value_capture_grade

```text
A：卡瓶颈，利润弹性高，财报有兑现
B：产业映射强，但直接财报证据不足
C：有题材，利润/现金流/估值有短板
D：纯概念或证据不足
```

## 2.7 产出

```text
个股 → 行业 → 主题 → 产业链 → 同类股 → 基准
```

## 2.8 验收标准

```text
1. 每只历史交易股票必须有行业映射。
2. 每只当前观察股票必须有行业和基准。
3. 高频研究股票必须有产业链位置。
4. 不能只用“概念标签”替代产业链位置。
```

---

# Phase 3｜行情/基准/Outcome 验证库

## 3.1 阶段目标

建立信号、交易、观察对象的后验结果验证系统。

这一步回答：

```text
当时看对了吗？
跑赢行业了吗？
跑赢主题了吗？
是不是只是大盘涨了？
最大浮盈是多少？
最大回撤是多少？
T20/T60 是否真正成熟？
```

## 3.2 必须建立的数据表

```text
data/research_db/market/
  daily_price_5y.parquet
  index_daily.parquet
  industry_benchmark_daily.parquet
  theme_basket_daily.parquet
  limit_board_daily.csv
  suspension_daily.csv

data/research_db/outcome/
  signal_outcome_t1_t3_t5_t10_t20_t60.parquet
  trade_outcome.parquet
  watchlist_outcome.parquet
  benchmark_alpha_outcome.parquet
```

## 3.3 Outcome Horizon 标准

```text
T1  = 1 个 forward trading day
T3  = 3 个 forward trading days
T5  = 5 个 forward trading days
T10 = 10 个 forward trading days
T20 = 20 个 forward trading days
T60 = 60 个 forward trading days
```

不足窗口：

```json
{
  "ready": false,
  "blocked_reason": "INSUFFICIENT_FORWARD_TRADING_DAYS"
}
```

## 3.4 必须计算

```text
gross_return
net_return_after_cost
benchmark_return
industry_return
theme_return
alpha_vs_market
alpha_vs_industry
alpha_vs_theme
max_favorable_excursion
max_adverse_excursion
invalidation_date
recovery_after_invalidation
```

## 3.5 交易成本模型

最低支持：

```text
commission
stamp_duty
slippage
limit_up_buy_failure
limit_down_sell_failure
suspension
one_price_limit_board
```

## 3.6 验收标准

```text
1. 每个 signal_id 都可追踪 T1/T3/T5/T10/T20/T60。
2. T20/T60 不足时必须阻断。
3. 每笔历史交易都有 alpha_vs_industry。
4. 每个 watchlist 观察对象可计算“错过收益”。
5. 所有净收益必须扣除交易成本与成交失败模拟。
```

---

# Phase 4｜FactorFactory 因子与信号验证库

## 4.1 阶段目标

把历史交易信号、观察信号、R-Matrix 信号、ZC35 催化信号、B-Matrix 当前截面信号，全部纳入因子验证框架。

## 4.2 必须建立的数据表

```text
data/research_db/factor/
  factor_registry.csv
  factor_observation.parquet
  factor_ic_result.csv
  factor_rankic_result.csv
  factor_decile_return.csv
  factor_promotion_ledger.jsonl
```

## 4.3 因子注册字段

```csv
factor_id,factor_name,matrix_layer,data_source,pit_safe,frequency,ttl_days,trust_level,missing_policy,production_allowed
```

## 4.4 第一批因子

```text
R-Matrix:
  trend_position
  rotation_stage
  invalidation_status
  volatility_regime

ZC35:
  catalyst_grade
  residual_power
  stack_status
  sell_on_news_risk
  scheduled_event_flag

B-Matrix:
  roe
  gross_margin
  net_margin
  revenue_growth
  net_profit_growth
  operating_cashflow
  debt_ratio
  pe
  pb
  ps
  industry_percentile
  financial_freshness

ZC40:
  limit_board_status
  fillability
  slippage_risk
  route_quality

ZC50:
  holding_alpha
  drawdown_status
  risk_budget_status
  account_permission
```

## 4.5 验证指标

```text
IC
RankIC
Decile Return
T5/T20/T60 Alpha
sector_holdout
walkforward
net_executable_return
sample_size
missing_rate
```

## 4.6 晋级规则

```text
单次有效 → observation
3次同类有效 → factor_candidate
跨行业有效 → research_factor
跨行情有效 → paper_factor
永远不得直接 production
```

## 4.7 验收标准

```text
1. 每个因子必须在 registry 注册。
2. 每个因子必须声明 pit_safe。
3. 每个因子必须有 missing_policy。
4. 所有验证必须使用严格 T horizon。
5. 无 IC/RankIC/Decile 验证，不得称为有效因子。
```

---

# Phase 5｜AutoCaseForge 案例记忆与自动内化系统

## 5.1 阶段状态

本阶段工程说明书已完成，作为独立文件纳入总路线图：

```text
《AutoCaseForge v1.0｜工程落地执行说明书》
```

其定位为：

```text
事件触发、自动建案、人工确认、跨案例验证、系统记忆内化
```

## 5.2 本阶段核心目标

```text
1. 自动落盘：不再依赖人工想起来才复盘。
2. 自动排队：每天生成 review_queue.md，让人只做确认。
3. 自动内化：每周/月生成 case memory report，把个案沉淀为系统记忆候选。
```

## 5.3 AutoCaseForge 主链

```text
Event Collector
→ Case Trigger Engine
→ Auto Case Builder
→ Outcome Updater
→ Review Queue
→ Rule Candidate Queue
→ Cross Case Validator
→ Memory Integrator
```

## 5.4 必须接入的数据源

```text
watchlist.csv
holdings.csv
research_universe.csv
events.jsonl
daily_prices.csv
benchmark_prices.csv
catalyst_events.jsonl
human_actions.jsonl
```

## 5.5 必须生成的五个 ledger

```text
event_ledger.jsonl
case_ledger.jsonl
decision_ledger.jsonl
outcome_ledger.jsonl
rule_candidate_ledger.jsonl
memory_candidate_ledger.jsonl
```

## 5.6 12 类触发器

```text
R1：watchlist 个股单日涨跌幅 >= 5% → PRICE_EVENT
R2：watchlist 个股 5日涨跌幅 >= 12% → MOMENTUM_EVENT
R3：候选股 T5 跑赢行业 >= 5% → TRUE_SIGNAL_CANDIDATE
R4：候选股 T5 跑输行业 <= -5% → FALSE_POSITIVE_CANDIDATE
R5：观察股大涨但未入选 → MISSED_OPPORTUNITY
R6：ZC35 residual_power < 0.2 → CATALYST_EXHAUSTION
R7：ZC35 stack_status=VACUUM → CATALYST_VACUUM
R8：scheduled_event T0 后下跌 >= 3% → SELL_ON_NEWS
R9：一字涨停且系统有入场信号 → EXECUTION_FAILURE
R10：跌停无法卖出 → EXIT_FAILURE
R11：持仓跑输行业 >= 5% → ACCOUNT_ALPHA_NEGATIVE
R12：R/B/D/ZC35/ZC40/ZC50 冲突 → SYSTEM_CONFLICT
```

## 5.7 晋级军规

```text
单案例只能形成 lesson，不能形成 rule。
3 个同类案例只能形成 rule_candidate。
10 个跨标的案例才能形成 research_rule。
20 个跨标的 + 跨行情案例才能进入 paper_rule。
任何案例都不能直接 production。
```

## 5.8 本阶段验收标准

```text
1. 能自动从事件生成 case draft。
2. 能写入五大 ledger。
3. 能生成 review_queue.md。
4. 能严格更新 T5/T20/T60 outcome。
5. 能生成 rule_candidate，但 promotion_allowed=false。
6. 能输出 weekly_case_report 和 monthly_memory_report。
7. 能把系统记忆候选写入 memory_candidate_ledger。
```

---

# Phase 6｜事件催化与 ZC35 生命周期数据库

## 6.1 阶段目标

把 ZC35 从单案例研究原型，扩展为跨标的、跨事件、跨行业的催化生命周期数据库。

## 6.2 必须建立的数据表

```text
data/research_db/event/
  event_ledger.jsonl
  catalyst_ledger.jsonl
  scheduled_event_calendar.csv
  sell_on_news_ledger.jsonl
  catalyst_decay_observation.csv
  catalyst_cross_case_validation.csv
```

## 6.3 事件字段

```json
{
  "event_id": "",
  "ticker": "",
  "event_date": "",
  "event_type": "",
  "scheduled": false,
  "source": "",
  "catalyst_grade": "",
  "surprise_level": "",
  "business_relevance": "",
  "financial_validation": "",
  "residual_power": 0.0,
  "half_life_days": null,
  "full_decay_days": null,
  "sell_on_news_risk": "",
  "paper_trackable": false,
  "production_allowed": false
}
```

## 6.4 事件分类

```text
POLICY_SIGNAL
EARNINGS_RELEASE
PRODUCT_BREAKTHROUGH
ORDER_ANNOUNCEMENT
INDUSTRY_CONFERENCE
IPO_RUMOR
SUPPLY_CHAIN_CONFIRMATION
FINANCIAL_VALIDATION
SCHEDULED_EVENT
UNSCHEDULED_SURPRISE
SELL_ON_NEWS
```

## 6.5 关键研究问题

```text
1. 什么类型的利好半衰期最长？
2. 什么类型的利好最容易“买预期卖事实”？
3. 哪些 scheduled event 实际是兑现窗口？
4. 哪些 unscheduled surprise 真能带来超额收益？
5. 催化 stack_status=VACUUM 时，R-Matrix 信号是否应降级？
```

## 6.6 验收标准

```text
1. 至少 30 个事件案例。
2. 至少 10 个 sell-on-news 案例。
3. 至少 3 个行业覆盖。
4. 每个事件都可追踪 T1/T3/T5/T20。
5. ZC35 规则不得基于单标的晋级。
```

---

# Phase 7｜财务截面与 B-Matrix 研究数据库

## 7.1 阶段目标

建立 B-Matrix 的财务、估值、行业分位、数据新鲜度底座。

当前优先做 current snapshot，不强行伪造历史 PIT。

## 7.2 必须建立的数据表

```text
data/research_db/finance/
  financial_snapshot.csv
  valuation_snapshot.csv
  industry_percentile.csv
  financial_freshness.csv
  b_matrix_current_snapshot.csv
```

## 7.3 核心字段

```text
roe
gross_margin
net_margin
revenue_growth
net_profit_growth
operating_cashflow
debt_ratio
pe
pb
ps
industry_percentile
report_date
as_of_date
freshness_status
pit_safe
```

## 7.4 Parser-Scorer 原则

LLM 只做事实抽取，不做连续分数打分。

允许 LLM 输出：

```text
bool
enum
evidence_refs
fact_value
```

禁止 LLM 输出：

```text
moat_score = 8.5
growth_score = 7.2
buy_score = 9
```

分数必须由确定性 scorer 根据 YAML / Python 配置计算。

## 7.5 验收标准

```text
1. 每个 B 因子有字段来源。
2. 每个字段有 freshness_status。
3. 每个字段声明 pit_safe。
4. 当前截面和历史 PIT 分离。
5. B-Matrix 输出只能 research/paper，不得 production。
```

---

# Phase 8｜产业链/行业知识库

## 8.1 阶段目标

建立行业与产业链知识库，但按“骨架优先、深研聚焦”的方式推进。

## 8.2 不采用的错误路线

```text
一开始写 31 个行业长篇百科。
```

原因：

```text
1. 耗时巨大。
2. 不直接验证收益。
3. 很难维护 freshness。
4. 容易变成静态知识库。
5. 无法回答个股 alpha 与账户结果。
```

## 8.3 正确路线

```text
先建 31 行业骨架卡
再做 8 条高频主线深研
最后扩展到完整行业库
```

## 8.4 31 行业骨架卡字段

```yaml
industry_id:
industry_name:
cycle_type:
macro_drivers:
micro_drivers:
financial_metrics_focus:
valuation_metrics_focus:
benchmark_index:
main_etfs:
representative_stocks:
high_beta_stocks:
defensive_stocks:
related_chains:
common_traps:
freshness_status:
updated_at:
```

## 8.5 首批 8 条高频主线

```text
1. 人形机器人 / 减速器 / 丝杠 / 传感器
2. 华为昇腾 / 国产算力
3. AI 服务器 / 液冷 / 电源 / 光模块
4. 储能 / 逆变器 / 户储
5. 电力设备 / 特高压 / 智能电网
6. 半导体设备 / 材料
7. 黄金 / 铜 / 小金属
8. 创新药 / CXO / 医疗器械
```

## 8.6 每条产业链深研必须输出

```text
chain_map
value_capture_map
listed_company_mapping
evidence_grade
financial_validation
catalyst_calendar
benchmark_basket
common_false_signal
watchlist_candidate_pool
```

## 8.7 验收标准

```text
1. 31 行业都有骨架卡。
2. 首批 8 条主线有完整 chain_map。
3. 每条链都有代表公司与基准篮子。
4. 每条链都有常见假信号库。
5. 每条链都能与 CaseForge、FactorFactory、B-Matrix 互相引用。
```

---

# Phase 9｜个人操盘画像与系统建议层

## 9.1 阶段目标

基于前 8 阶段数据，生成你的个人操盘画像。

这不是情绪化总结，而是数据化画像。

## 9.2 必须回答的问题

```text
1. 你最擅长哪些行业/主线？
2. 你最容易亏在哪些模式？
3. 你的胜率来自持有、轮动、事件还是择时？
4. 你是更适合中低频跨期，还是短线事件？
5. 你在哪些行情中表现最好？
6. 哪些信号对你有效，哪些信号会诱导你犯错？
7. 你应该降低哪些类型的交易？
8. 你应该强化哪些类型的研究？
```

## 9.3 输出物

```text
data/research_db/personal_profile/
  operator_profile.json
  edge_map.md
  weakness_map.md
  forbidden_trade_patterns.md
  preferred_setup_library.md
  account_style_recommendation.md
```

## 9.4 操盘画像维度

```text
holding_period_edge
industry_edge
catalyst_edge
execution_weakness
account_risk_tolerance
drawdown_behavior
sell_discipline
missed_opportunity_pattern
overtrading_pattern
case_learning_velocity
```

## 9.5 验收标准

```text
1. 画像必须由数据生成，不是主观判断。
2. 每个结论必须引用 trade/case/outcome 证据。
3. 输出只能是 research/paper 建议。
4. 不得生成自动交易指令。
```

---

# Phase 10｜Research Cockpit 与月度内化机制

## 10.1 阶段目标

把所有数据库与知识库整合成一个月度运行机制。

## 10.2 每日流程

```text
1. 更新 watchlist / holdings / daily_prices。
2. 运行 AutoCaseForge daily。
3. 生成 review_queue.md。
4. 记录新事件、新冲突、新 outcome。
```

## 10.3 每周流程

```text
1. 更新 T5/T20/T60 到期结果。
2. 生成 weekly_case_report。
3. 更新 error_heatmap。
4. 更新 rule_candidate_queue。
5. 检查账户 alpha 与持仓风险。
```

## 10.4 每月流程

```text
1. 生成 monthly_memory_report。
2. 执行 cross-case validation。
3. 更新 factor_validation_report。
4. 更新 operator_profile。
5. 更新 industry/chain freshness。
6. 输出 system_learning_report。
```

## 10.5 月度系统内化报告必须包含

```text
本月新增案例
本月关闭案例
本月命中案例
本月错判案例
本月错过机会
本月催化失效
本月执行失败
本月账户 alpha
本月规则候选
本月可晋级/不可晋级清单
下月研究优先级
```

## 10.6 验收标准

```text
1. 每月能输出一份系统学习报告。
2. 每月能更新个人操盘画像。
3. 每月能生成规则候选队列。
4. 每月能明确“哪些规则不能晋级”。
5. 系统不会因为案例积累而自动 production。
```

---

# 11. 推荐执行顺序与批次规划

## Batch RDB-0：ResearchDB Constitution

```text
目标：冻结数据库宪法、目录、字段规范、PIT/Outcome/Promotion 规则。
预计产出：docs/research_db/ + verify_research_db_constitution.sh
```

## Batch RDB-1：Account Truth Import

```text
目标：导入 5 年交易、持仓、账户曲线。
预计产出：account/ 数据表 + account_truth_report.md
```

## Batch RDB-2：Universe & Mapping

```text
目标：建立股票主数据、行业、主题、产业链、基准映射。
预计产出：security_master + chain_mapping + benchmark_mapping
```

## Batch RDB-3：Market & Outcome Engine

```text
目标：建立行情、基准、T horizon、alpha、成本模型。
预计产出：signal_outcome / trade_outcome / watchlist_outcome
```

## Batch RDB-4：Factor Validation Layer

```text
目标：把信号与因子纳入 IC/RankIC/Decile 验证。
预计产出：factor_registry + factor_validation_report
```

## Batch RDB-5：AutoCaseForge v1.0

```text
状态：工程说明书已完成。
目标：实现自动建案、五大 ledger、review queue、weekly/monthly memory。
```

## Batch RDB-6：ZC35 Event Catalyst DB

```text
目标：把催化生命周期扩展为跨案例事件数据库。
预计产出：catalyst_ledger + sell_on_news_ledger + decay_observation
```

## Batch RDB-7：B-Matrix Financial Snapshot

```text
目标：建立财务与估值截面库。
预计产出：financial_snapshot + valuation_snapshot + industry_percentile
```

## Batch RDB-8：Industry & Chain Knowledge Base

```text
目标：31 行业骨架 + 8 条主线深研。
预计产出：industries/ + chains/ + false_signal_library/
```

## Batch RDB-9：Personal Operator Profile

```text
目标：生成你的个人操盘画像和系统建议边界。
预计产出：operator_profile + edge_map + weakness_map
```

## Batch RDB-10：Research Cockpit

```text
目标：整合每日/每周/每月运行机制。
预计产出：monthly_memory_report + system_learning_report
```

---

# 12. 成功标准

这个大工程完成后，Z-MATRIX-OS 应能做到：

```text
1. 自动读取 5 年实盘数据。
2. 自动重建账户真相。
3. 自动计算每笔交易和每个信号的后验结果。
4. 自动区分市场 beta、行业 beta、主题 beta、个股 alpha。
5. 自动沉淀错判、命中、错过、执行失败、催化失效案例。
6. 自动生成每周案例报告和每月系统学习报告。
7. 自动发现规则候选，但不自动晋级。
8. 自动更新个人操盘画像。
9. 支持行业/产业链知识与实盘案例相互引用。
10. 逐步成长为个人操盘分析建议系统。
```

但它仍必须坚持：

```text
不自动下单
不接 broker
不启 runtime
不输出 BUY / SELL / AUTO_EXECUTE
不把研究规则直接 production
```

---

# 13. 最终导航图

```text
过去5年实盘数据
      ↓
Account Truth DB
      ↓
Trade / Signal / Outcome Ledger
      ↓
Industry / Chain / Benchmark Mapping
      ↓
FactorFactory Validation
      ↓
AutoCaseForge Case Memory
      ↓
ZC35 Event Catalyst DB
      ↓
B-Matrix Financial Snapshot
      ↓
Industry & Chain Knowledge Base
      ↓
Personal Operator Profile
      ↓
Research Cockpit
      ↓
个人操盘分析建议系统
```

---

# 14. 最终裁决

当前最优路线不是：

```text
先写 31 个行业板块研究
```

而是：

```text
先把过去 5 年实盘数据结构化
再把每个信号结果验证清楚
再把行业/产业链作为归因与候选生成底座
再用 AutoCaseForge 自动沉淀案例
最后反哺行业知识库与个人操盘画像
```

一句话：

```text
先让系统知道你过去为什么赢、为什么输、为什么错过；
再让系统学习行业、学习因子、学习催化、学习你本人。
```

这才是 Z-MATRIX-OS 从“研究平台”成长为“个人操盘分析建议系统”的正确路径。
