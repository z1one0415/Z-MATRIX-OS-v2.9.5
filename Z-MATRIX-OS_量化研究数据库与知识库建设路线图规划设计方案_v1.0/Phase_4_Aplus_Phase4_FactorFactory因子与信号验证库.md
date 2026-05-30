# Phase 4：FactorFactory 因子与信号验证库｜A+加固执行版

> **版本**：A+ Hardened Execution Spec
> **用途**：交给 OpenClaw 天师 / deepseek-v4-pro 执行，要求无漂移、无歧义、可测试、可审计、可长期维护。
> **重要说明**：本文档在原 Phase 设计基础上加入防漂移执行层。若原文与加固层冲突，以加固层为准。


---

# A/A+ 加固执行层｜DeepSeek-v4-Pro / OpenClaw 防漂移军规

> 本节为强制执行层。下方原始设计内容不得被摘要化、不得被自由解释、不得被“等价实现”替代。OpenClaw / deepseek-v4-pro 必须按本文档的目录、文件、函数、测试、verify、closeout 顺序落地。

## A0. 执行等级

```text
目标执行等级：A / A+
允许产出：research-only / paper-only 工程代码、schema、fixture、测试、报告、verify
禁止产出：真实交易、broker 接口、runtime daemon、production 开关、自动买卖、RC 状态变更
```

## A1. 全局硬门

所有新增代码、报告、JSON、YAML、Ledger、测试输出必须保持：

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

禁止在业务输出中出现：

```text
BUY
SELL
STRONG_BUY
AUTO_BUY
AUTO_SELL
BROKER_ORDER
PLACE_ORDER
SEND_ORDER
EXECUTE_TRADE
PRODUCTION_READY
REAL_TRADE_READY
```

如果作为“禁止词清单”出现在文档或测试里，必须加 `allowlist: forbidden-token-definition` 注释，不得被业务模块输出。

## A2. 执行方式

```text
1. 每个 Batch 独立 commit。
2. 每个 Batch 完成后必须运行对应测试。
3. Closeout 前必须运行本 Phase verify。
4. Phase verify 失败，不得提交 Closeout。
5. 不得自动进入下一 Phase。
6. 不得顺手修其他 Phase。
7. 不得修改 RC1 / production / broker / runtime 状态。
```

## A3. 文件实现优先级

OpenClaw 必须按顺序实现：

```text
1. docs / data 目录与 README
2. schema / enum / constants
3. pure function modules
4. fixture
5. unit tests
6. report generator
7. verify script
8. acceptance matrix
9. closeout report
```

禁止先写报告再补代码，禁止只创建空文件通过验收。

## A4. 测试与验收硬规则

每个 Phase 必须至少具备：

```text
1. Schema validation tests
2. Enum validation tests
3. Missing data tests
4. Safety boundary tests
5. Verify script test
6. Report generation smoke test
7. No-production scan
8. Closeout consistency test
```

测试不得只检查“文件存在”。每个核心函数必须至少有：

```text
正常样本
缺失字段样本
非法枚举样本
边界样本
安全阻断样本
```

## A5. Closeout 输出格式

每个 Phase 完成后必须输出：

```text
commit:
branch:
phase:
status:
files_created:
files_modified:
tests_run:
verify_run:
known_limitations:
blocked_items:
safety_state:
next_phase_allowed:
```

`safety_state` 必须逐项列出：

```text
real_trade_allowed=False
broker_order_allowed=False
runtime_enabled=False
auto_buy_allowed=False
auto_sell_allowed=False
production_allowed=False
paper_only=True
human_review_required=True
```

## A6. 失败即停规则

出现以下任一情况必须停止，不得继续：

```text
1. 任何测试失败。
2. verify 脚本失败。
3. 发现 production/broker/runtime/real_trade flag。
4. 原始私有数据被 git track。
5. T20/T60 不足却被标为 ready。
6. CURRENT_SNAPSHOT_ONLY 被用于历史回测。
7. 单案例被晋级为规则。
8. LLM 输出连续主观评分。
9. 报告给出 BUY/SELL/AUTO_EXECUTE。
```

---

# 原始 Phase 设计内容

# Phase 4：FactorFactory 因子与信号验证库

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 4  
> **阶段名称**：FactorFactory Validation Layer｜因子与信号验证库  
> **前置阶段**：Phase 0：ResearchDB 宪法与目录冻结；Phase 1：5年实盘真相库；Phase 2：标的主数据 + 行业/产业链映射库；Phase 3：行情/基准/Outcome 验证库  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：因子注册 / 因子观测 / IC / RankIC / Decile Return / Walk-Forward / Sector Holdout / 因子晋级淘汰 / 研究信号可信度验证  
> **阶段目标**：把 R-Matrix、B-Matrix、D-Matrix、ZC35、ZC40、ZC50、Research Council、CaseForge 产生的所有信号与标签，统一注册为可验证因子，基于 Phase 3 的 T1/T3/T5/T10/T20/T60 Outcome 进行 IC、RankIC、Decile Return、行业中性、滚动窗口、净可执行收益验证，形成“因子是否有效、在哪些行业有效、在哪些行情失效、能否进入 paper rule”的审计结果。  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 4 是 Z-MATRIX-OS 从“后验验证”进入“因子科学”的关键阶段。

Phase 1 解决：

```text
我过去真实交易和账户曲线是什么。
```

Phase 2 解决：

```text
每个标的属于什么行业、产业链、主题、同类组和基准。
```

Phase 3 解决：

```text
每个交易、信号、观察对象后续到底产生了多少收益和 alpha。
```

Phase 4 解决：

```text
哪些信号、标签、因子、催化、账户状态，真的能解释未来收益。
```

本阶段只允许做：

```text
1. 建立因子注册表
2. 建立因子观测表
3. 建立 IC / RankIC / Decile Return 验证
4. 建立 Walk-Forward 验证
5. 建立 Sector Holdout 验证
6. 建立净可执行收益验证
7. 建立因子质量评分
8. 建立因子晋级/淘汰 ledger
9. 输出 Factor Validation Report
```

本阶段禁止：

```text
1. 不生成买卖建议
2. 不接 broker
3. 不开启 runtime
4. 不进入 production
5. 不改 RC1 状态
6. 不把单次有效因子直接晋级
7. 不把未满 T20/T60 的样本标为有效
8. 不把 LLM 主观分数作为因子值
9. 不把 CURRENT_SNAPSHOT_ONLY 当历史 PIT 因子
10. 不把毛收益当净可执行收益
```

---

# 一、Phase 4 的核心价值

Phase 4 要回答 12 个问题：

```text
1. R-Matrix 的位置/轮动/失效标签是否有预测力？
2. ZC35 的催化等级、残余能量、真空状态是否能解释未来收益？
3. B-Matrix 的财务质量、估值、成长、现金流字段是否有效？
4. ZC40 的成交可得性是否解释纸面收益和实得收益差异？
5. ZC50 的账户状态是否决定某些信号应降级？
6. 哪些因子只在某些行业有效？
7. 哪些因子只在牛市有效，熊市失效？
8. 哪些因子 IC 正但净可执行收益为负？
9. 哪些因子 Decile 单调性好？
10. 哪些因子过拟合？
11. 哪些因子需要淘汰？
12. 哪些因子可进入 paper-only rule candidate？
```

没有 Phase 4，系统只能“讲逻辑”。  
完成 Phase 4 后，系统才能说：

```text
这个信号有统计证据支持，还是只是叙事幻觉。
```

---

# 二、Phase 4 输入边界

## 2.1 来自 Phase 1 的输入

```text
data/research_db/account/normalized/trade_ledger.csv
data/research_db/account/normalized/position_ledger.csv
data/research_db/account/normalized/holding_pnl_ledger.csv
data/research_db/signal/manual_decision_ledger.csv
data/research_db/watchlist/watchlist_ledger.csv
data/research_db/watchlist/candidate_ledger.csv
```

## 2.2 来自 Phase 2 的输入

```text
data/research_db/universe/normalized/security_master.csv
data/research_db/universe/normalized/industry_classification.csv
data/research_db/universe/normalized/chain_mapping.csv
data/research_db/universe/normalized/theme_mapping.csv
data/research_db/universe/normalized/peer_group_mapping.csv
data/research_db/universe/normalized/benchmark_mapping.csv
```

## 2.3 来自 Phase 3 的输入

```text
data/research_db/outcome/normalized/signal_outcome_t1_t3_t5_t10_t20_t60.parquet
data/research_db/outcome/normalized/trade_outcome.parquet
data/research_db/outcome/normalized/watchlist_outcome.parquet
data/research_db/outcome/normalized/candidate_outcome.parquet
data/research_db/outcome/normalized/benchmark_alpha_outcome.parquet
data/research_db/outcome/normalized/executable_return_outcome.parquet
```

## 2.4 来自现有 Z-MATRIX 模块的输入

```text
R-Matrix 信号
B-Matrix 当前截面字段
D-Matrix 事件/资金流字段
ZC35 催化生命周期字段
ZC40 执行质量字段
ZC50 账户治理字段
Research Council reviewer 输出
CaseForge case/error/rule_candidate 标签
```

---

# 三、必须创建的数据目录

```text
data/research_db/factor/
  README.md

  registry/
    factor_registry.csv
    factor_group_registry.csv
    factor_source_registry.csv
    factor_version_registry.csv

  observations/
    factor_observation.parquet
    factor_observation_quality_ledger.csv
    factor_missing_ledger.csv
    factor_pit_status_ledger.csv

  validation/
    factor_ic_result.csv
    factor_rankic_result.csv
    factor_decile_return.csv
    factor_decile_monotonicity.csv
    factor_walkforward_result.csv
    factor_sector_holdout_result.csv
    factor_regime_holdout_result.csv
    factor_net_executable_result.csv
    factor_stability_result.csv

  promotion/
    factor_promotion_ledger.jsonl
    factor_rejection_ledger.jsonl
    factor_watchlist.jsonl
    factor_retirement_ledger.jsonl

  reports/
    factor_validation_report.md
    factor_ic_report.md
    factor_decile_report.md
    factor_promotion_report.md
    factor_rejection_report.md
    factor_quality_report.md
```

---

# 四、必须创建的代码模块

```text
zmatrix/research_db/factor/
  __init__.py
  factor_registry_schema.py
  factor_observation_schema.py
  factor_group_schema.py
  factor_source_policy.py
  factor_versioning.py
  factor_loader.py
  factor_observation_builder.py
  factor_pit_checker.py
  factor_missing_policy.py
  ic_calculator.py
  rankic_calculator.py
  decile_return_calculator.py
  monotonicity_checker.py
  walkforward_validator.py
  sector_holdout_validator.py
  regime_holdout_validator.py
  executable_factor_validator.py
  factor_quality_scorer.py
  factor_promotion_gate.py
  factor_rejection_policy.py
  factor_validation_report.py
```

---

# 五、核心数据表规范

## 5.1 factor_registry.csv

### 字段

```csv
factor_id,factor_name,factor_group,matrix_layer,data_source,source_module,factor_type,value_type,pit_safe,pit_status,frequency,ttl_days,trust_level,missing_policy,neutralization_required,benchmark_required,production_allowed,paper_allowed,version,status,created_at,updated_at,notes
```

### factor_group 枚举

```text
R_MATRIX
B_MATRIX
D_MATRIX
ZC35_CATALYST
ZC40_EXECUTION
ZC50_ACCOUNT
RESEARCH_COUNCIL
CASEFORGE
MARKET_REGIME
INDUSTRY_CHAIN
CUSTOM
```

### matrix_layer 枚举

```text
R
B
D
ZC35
ZC40
ZC50
COUNCIL
CASE
REGIME
ACCOUNT
UNKNOWN
```

### factor_type 枚举

```text
NUMERIC
BOOLEAN
ENUM
ORDINAL
CATEGORY
TEXT_DERIVED_ENUM
```

### value_type 枚举

```text
FLOAT
INT
BOOL
ENUM
STRING
```

### pit_status 枚举

```text
PIT_SAFE
PIT_UNSAFE
CURRENT_SNAPSHOT_ONLY
UNKNOWN_PIT_STATUS
BLOCKED_FOR_BACKTEST
```

### missing_policy 枚举

```text
DROP_SAMPLE
FILL_NEUTRAL
FILL_GROUP_MEDIAN
FLAG_MISSING
BLOCK_FACTOR
```

### status 枚举

```text
REGISTERED
OBSERVING
VALIDATING
RESEARCH_ACCEPTED
PAPER_CANDIDATE
REJECTED
RETIRED
BLOCKED
```

### 硬规则

```text
production_allowed 必须为 false。
pit_status=UNKNOWN_PIT_STATUS 不得进入 validation。
pit_status=CURRENT_SNAPSHOT_ONLY 不得进入历史回测。
factor_type=TEXT_DERIVED_ENUM 必须遵守 Parser-Scorer Split。
```

---

## 5.2 factor_observation.parquet

### 字段

```csv
observation_id,factor_id,ticker,name,observation_date,factor_value,raw_value,normalized_value,rank_value,industry_l1,industry_l2,chain_id,theme_id,regime_id,source_module,source_event_id,pit_status,trust_level,missing_flag,quality_status,version
```

### 硬规则

```text
observation_id 必须唯一。
factor_id 必须在 factor_registry 中存在。
observation_date 不得为空。
factor_value 可为空，但 missing_flag 必须为 true。
pit_status 不得为空。
quality_status=ERROR 的样本不得进入 validation。
```

---

## 5.3 factor_ic_result.csv

### 字段

```csv
factor_id,factor_name,horizon,return_field,sample_size,ic_mean,ic_median,ic_std,ic_positive_ratio,t_stat,p_value,coverage,missing_rate,start_date,end_date,quality_status
```

### return_field 枚举

```text
gross_return
alpha_vs_market
alpha_vs_industry
alpha_vs_theme
alpha_vs_peer
net_executable_return
```

---

## 5.4 factor_rankic_result.csv

### 字段

```csv
factor_id,factor_name,horizon,return_field,sample_size,rankic_mean,rankic_median,rankic_std,rankic_positive_ratio,t_stat,p_value,coverage,missing_rate,start_date,end_date,quality_status
```

---

## 5.5 factor_decile_return.csv

### 字段

```csv
factor_id,factor_name,horizon,return_field,decile,sample_size,mean_return,median_return,win_rate,mean_alpha,median_alpha,mfe_mean,mae_mean,net_executable_mean,quality_status
```

### Decile 规则

```text
decile=1 表示最低因子值组。
decile=10 表示最高因子值组。
因子方向必须在 registry 中声明 factor_direction。
```

---

## 5.6 factor_decile_monotonicity.csv

### 字段

```csv
factor_id,factor_name,horizon,return_field,monotonicity_score,top_bottom_spread,top_bottom_t_stat,decile_slope,quality_status
```

---

## 5.7 factor_walkforward_result.csv

### 字段

```csv
factor_id,factor_name,train_start,train_end,test_start,test_end,horizon,train_ic,test_ic,train_rankic,test_rankic,decile_spread_train,decile_spread_test,stability_status,quality_status
```

### stability_status

```text
STABLE
DECAYING
REVERSING
INSUFFICIENT_SAMPLE
```

---

## 5.8 factor_sector_holdout_result.csv

### 字段

```csv
factor_id,factor_name,holdout_industry,train_sample,test_sample,train_ic,test_ic,train_rankic,test_rankic,holdout_status,quality_status
```

### holdout_status

```text
GENERALIZES
SECTOR_SPECIFIC
FAILS_HOLDOUT
INSUFFICIENT_SAMPLE
```

---

## 5.9 factor_regime_holdout_result.csv

### 字段

```csv
factor_id,factor_name,regime_id,horizon,sample_size,ic,rankic,decile_spread,net_executable_return,regime_status,quality_status
```

### regime_status

```text
WORKS_IN_REGIME
FAILS_IN_REGIME
REGIME_SENSITIVE
INSUFFICIENT_SAMPLE
```

---

## 5.10 factor_net_executable_result.csv

### 字段

```csv
factor_id,factor_name,horizon,paper_return_mean,net_executable_return_mean,execution_drag,blocked_sample_count,blocked_ratio,execution_status,quality_status
```

### execution_status

```text
EXECUTABLE_ALPHA
PAPER_ONLY_ALPHA
EXECUTION_DRAGGED
NOT_EXECUTABLE
INSUFFICIENT_EXECUTION_DATA
```

---

## 5.11 factor_promotion_ledger.jsonl

每行结构：

```json
{
  "promotion_id": "PROMO-FACTOR-0001",
  "factor_id": "",
  "from_status": "VALIDATING",
  "to_status": "RESEARCH_ACCEPTED",
  "decision": "PROMOTE / REJECT / WATCH / RETIRE",
  "decision_date": "",
  "evidence": {
    "ic": "",
    "rankic": "",
    "decile": "",
    "walkforward": "",
    "sector_holdout": "",
    "net_executable": ""
  },
  "blocked_reasons": [],
  "production_allowed": false,
  "human_review_required": true
}
```

---

# 六、第一批因子注册范围

Phase 4 第一版不得追求全市场全因子，先注册 Z-MATRIX 当前最关键因子。

## 6.1 R-Matrix 因子

```text
r_trend_position
r_rotation_stage
r_invalidation_status
r_volatility_regime
r_breakout_strength
r_drawdown_recovery_type
```

## 6.2 ZC35 催化因子

```text
zc35_catalyst_grade
zc35_residual_power
zc35_stack_status
zc35_sell_on_news_risk
zc35_scheduled_event_flag
zc35_catalyst_vacuum_flag
zc35_paper_trackable
```

注意：

```text
禁止使用 tradeable 字段。
必须使用 paper_trackable。
```

## 6.3 B-Matrix 财务截面因子

```text
b_roe
b_gross_margin
b_net_margin
b_revenue_growth
b_net_profit_growth
b_operating_cashflow
b_debt_ratio
b_pe
b_pb
b_ps
b_industry_percentile
b_financial_freshness
```

注意：

```text
如果当前只有 current snapshot，则 pit_status=CURRENT_SNAPSHOT_ONLY。
CURRENT_SNAPSHOT_ONLY 不得进入历史回测。
```

## 6.4 ZC40 执行因子

```text
zc40_limit_board_status
zc40_one_price_board_flag
zc40_fillability
zc40_slippage_risk
zc40_route_quality
zc40_suspension_flag
```

## 6.5 ZC50 账户因子

```text
zc50_holding_alpha
zc50_drawdown_status
zc50_risk_budget_status
zc50_position_concentration
zc50_account_permission
```

## 6.6 CaseForge 因子

```text
case_type
error_type
module_attribution
rule_candidate_flag
case_quality_score
cross_case_count
```

## 6.7 Research Council 因子

```text
council_verdict
council_conflict_flag
council_data_insufficient_flag
reviewer_risk_flags_count
reviewer_score_trace_quality
```

---

# 七、因子验证方法

## 7.1 IC

```text
IC = corr(factor_value, future_return)
```

必须支持 return_field：

```text
gross_return
alpha_vs_market
alpha_vs_industry
alpha_vs_theme
alpha_vs_peer
net_executable_return
```

## 7.2 RankIC

```text
RankIC = corr(rank(factor_value), rank(future_return))
```

适合处理：

```text
非线性因子
排序因子
枚举映射因子
```

## 7.3 Decile Return

按因子值分 10 组，比较：

```text
top decile
bottom decile
top-bottom spread
decile monotonicity
```

## 7.4 Walk-Forward

不得只在全样本上验证。必须支持：

```text
train window
test window
rolling window
expanding window
```

## 7.5 Sector Holdout

必须支持：

```text
剔除某行业训练
在该行业测试
```

用于判断：

```text
因子是行业特异，还是跨行业有效。
```

## 7.6 Regime Holdout

必须支持：

```text
bull
bear
range
liquidity_contraction
policy_shock
```

用于判断：

```text
因子是否行情敏感。
```

## 7.7 Net Executable Validation

必须使用 Phase 3 的：

```text
net_executable_return
execution_blocked
execution_blocked_reason
```

判断：

```text
纸面 alpha 是否能交易到。
```

---

# 八、因子质量评分

## 8.1 factor_quality_scorer 输出

```json
{
  "factor_id": "",
  "quality_score": 0.0,
  "sample_score": 0.0,
  "ic_score": 0.0,
  "rankic_score": 0.0,
  "decile_score": 0.0,
  "stability_score": 0.0,
  "holdout_score": 0.0,
  "execution_score": 0.0,
  "missing_penalty": 0.0,
  "lookahead_penalty": 0.0,
  "final_status": "WATCH"
}
```

## 8.2 评分参考

```text
sample_score：样本数、覆盖率
ic_score：IC均值、正IC比例
rankic_score：RankIC均值、正RankIC比例
decile_score：top-bottom spread、单调性
stability_score：walk-forward 稳定性
holdout_score：行业/行情外推能力
execution_score：净可执行收益
missing_penalty：缺失率惩罚
lookahead_penalty：PIT风险惩罚
```

---

# 九、因子晋级/淘汰规则

## 9.1 状态路径

```text
REGISTERED
→ OBSERVING
→ VALIDATING
→ RESEARCH_ACCEPTED
→ PAPER_CANDIDATE
```

淘汰路径：

```text
VALIDATING → REJECTED
PAPER_CANDIDATE → RETIRED
```

## 9.2 晋级最低门槛

```text
sample_size >= 100
missing_rate <= 30%
pit_status != UNKNOWN_PIT_STATUS
ic_positive_ratio >= 55%
rankic_positive_ratio >= 55%
top_bottom_spread > 0
walkforward_status != REVERSING
net_executable_return 不得显著为负
production_allowed=false
```

## 9.3 直接阻断条件

```text
PIT_UNSAFE
UNKNOWN_PIT_STATUS
CURRENT_SNAPSHOT_ONLY 用于历史回测
sample_size < 30
missing_rate > 60%
decile 完全无单调性
walkforward 反转
net_executable_return 为负且纸面收益为正
execution_blocked_ratio > 50%
```

## 9.4 CaseForge 规则约束

```text
单案例不得晋级因子。
少于 3 个同类案例只能 LESSON_ONLY。
少于 10 个跨标的案例只能 RULE_CANDIDATE。
少于 20 个跨行情案例不得进入 PAPER_CANDIDATE。
```

---

# 十、代码模块设计

## 10.1 factor_registry_schema.py

必须定义：

```python
REQUIRED_FACTOR_REGISTRY_FIELDS = [
    "factor_id",
    "factor_name",
    "factor_group",
    "matrix_layer",
    "data_source",
    "factor_type",
    "value_type",
    "pit_status",
    "missing_policy",
    "production_allowed",
    "version",
    "status",
]
```

提供：

```python
def validate_factor_registry_row(row: dict) -> dict:
    ...
```

---

## 10.2 factor_observation_schema.py

提供：

```python
def validate_factor_observation_row(row: dict) -> dict:
    ...
```

必须验证：

```text
factor_id
ticker
observation_date
pit_status
quality_status
```

---

## 10.3 factor_pit_checker.py

提供：

```python
def check_factor_pit_safety(factor_row: dict, observation_row: dict) -> dict:
    ...
```

必须阻断：

```text
CURRENT_SNAPSHOT_ONLY 历史回测
UNKNOWN_PIT_STATUS validation
PIT_UNSAFE validation
```

---

## 10.4 ic_calculator.py

提供：

```python
def calculate_ic(factor_values: list[float], future_returns: list[float]) -> dict:
    ...
```

输出：

```json
{
  "ic": 0.0,
  "sample_size": 0,
  "quality_status": "READY"
}
```

---

## 10.5 rankic_calculator.py

提供：

```python
def calculate_rankic(factor_values: list[float], future_returns: list[float]) -> dict:
    ...
```

---

## 10.6 decile_return_calculator.py

提供：

```python
def calculate_decile_returns(rows: list[dict], factor_field: str, return_field: str) -> list[dict]:
    ...
```

---

## 10.7 monotonicity_checker.py

提供：

```python
def check_decile_monotonicity(decile_rows: list[dict]) -> dict:
    ...
```

---

## 10.8 walkforward_validator.py

提供：

```python
def run_walkforward_validation(rows: list[dict], factor_id: str, horizon: str, return_field: str) -> dict:
    ...
```

---

## 10.9 sector_holdout_validator.py

提供：

```python
def run_sector_holdout(rows: list[dict], factor_id: str, holdout_industry: str) -> dict:
    ...
```

---

## 10.10 regime_holdout_validator.py

提供：

```python
def run_regime_holdout(rows: list[dict], factor_id: str, regime_id: str) -> dict:
    ...
```

---

## 10.11 executable_factor_validator.py

提供：

```python
def validate_net_executable_factor(rows: list[dict], factor_id: str) -> dict:
    ...
```

---

## 10.12 factor_quality_scorer.py

提供：

```python
def score_factor_quality(validation_summary: dict) -> dict:
    ...
```

---

## 10.13 factor_promotion_gate.py

提供：

```python
def evaluate_factor_promotion(factor_row: dict, validation_summary: dict) -> dict:
    ...
```

返回：

```json
{
  "decision": "PROMOTE / WATCH / REJECT / RETIRE",
  "to_status": "RESEARCH_ACCEPTED",
  "blocked_reasons": [],
  "production_allowed": false,
  "human_review_required": true
}
```

---

## 10.14 factor_validation_report.py

提供：

```python
def generate_factor_validation_report(summary: dict, output_path: str) -> dict:
    ...
```

---

# 十一、测试要求

## 11.1 测试目录

```text
tests/research_db/factor/
  test_factor_registry_schema.py
  test_factor_observation_schema.py
  test_factor_pit_checker.py
  test_factor_missing_policy.py
  test_ic_calculator.py
  test_rankic_calculator.py
  test_decile_return_calculator.py
  test_monotonicity_checker.py
  test_walkforward_validator.py
  test_sector_holdout_validator.py
  test_regime_holdout_validator.py
  test_executable_factor_validator.py
  test_factor_quality_scorer.py
  test_factor_promotion_gate.py
  test_factor_validation_report.py
  test_no_production_boundary.py
```

---

## 11.2 必须测试的场景

### factor_registry_schema

```text
缺 factor_id → ERROR
缺 pit_status → ERROR
production_allowed=True → ERROR
CURRENT_SNAPSHOT_ONLY + historical_backtest → BLOCKED
```

### factor_pit_checker

```text
PIT_SAFE → READY
PIT_UNSAFE → BLOCKED
UNKNOWN_PIT_STATUS → BLOCKED
CURRENT_SNAPSHOT_ONLY 进入历史验证 → BLOCKED
```

### ic_calculator

```text
正相关数据 → ic > 0
负相关数据 → ic < 0
样本不足 → INSUFFICIENT_SAMPLE
常数因子 → INVALID_FACTOR_VARIANCE
```

### rankic_calculator

```text
排序正相关 → rankic > 0
排序负相关 → rankic < 0
重复值可处理
```

### decile_return_calculator

```text
可分 10 组
样本不足时降低 quality_status
top decile / bottom decile 正确
```

### monotonicity_checker

```text
单调上升 → monotonicity_score 高
随机分布 → monotonicity_score 低
反向单调 → direction warning
```

### walkforward_validator

```text
train/test 都足够 → READY
test IC 与 train 同向 → STABLE
test IC 反向 → REVERSING
样本不足 → INSUFFICIENT_SAMPLE
```

### sector_holdout_validator

```text
holdout 行业样本足够 → 可验证
holdout 后失效 → FAILS_HOLDOUT
```

### executable_factor_validator

```text
纸面收益为正但 net executable 为负 → EXECUTION_DRAGGED
blocked_ratio 高 → NOT_EXECUTABLE
```

### factor_promotion_gate

```text
低样本 → WATCH
PIT_UNSAFE → REJECT
decile 无单调 → WATCH/REJECT
walkforward reversing → REJECT
net executable negative → REJECT
合格因子 → RESEARCH_ACCEPTED / PAPER_CANDIDATE
production_allowed 永远 false
```

---

# 十二、verify 脚本

新增：

```text
scripts/verify_research_db_phase4_factor_factory.sh
```

内容必须执行：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 4 FactorFactory Verification ═══"

python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/factor/

python3 - <<'PY'
from pathlib import Path

required_modules = [
    "zmatrix/research_db/factor/factor_registry_schema.py",
    "zmatrix/research_db/factor/factor_observation_schema.py",
    "zmatrix/research_db/factor/factor_group_schema.py",
    "zmatrix/research_db/factor/factor_source_policy.py",
    "zmatrix/research_db/factor/factor_versioning.py",
    "zmatrix/research_db/factor/factor_loader.py",
    "zmatrix/research_db/factor/factor_observation_builder.py",
    "zmatrix/research_db/factor/factor_pit_checker.py",
    "zmatrix/research_db/factor/factor_missing_policy.py",
    "zmatrix/research_db/factor/ic_calculator.py",
    "zmatrix/research_db/factor/rankic_calculator.py",
    "zmatrix/research_db/factor/decile_return_calculator.py",
    "zmatrix/research_db/factor/monotonicity_checker.py",
    "zmatrix/research_db/factor/walkforward_validator.py",
    "zmatrix/research_db/factor/sector_holdout_validator.py",
    "zmatrix/research_db/factor/regime_holdout_validator.py",
    "zmatrix/research_db/factor/executable_factor_validator.py",
    "zmatrix/research_db/factor/factor_quality_scorer.py",
    "zmatrix/research_db/factor/factor_promotion_gate.py",
    "zmatrix/research_db/factor/factor_rejection_policy.py",
    "zmatrix/research_db/factor/factor_validation_report.py",
]

for p in required_modules:
    assert Path(p).exists(), f"Missing module: {p}"

required_dirs = [
    "data/research_db/factor/registry",
    "data/research_db/factor/observations",
    "data/research_db/factor/validation",
    "data/research_db/factor/promotion",
    "data/research_db/factor/reports",
]

for p in required_dirs:
    assert Path(p).exists(), f"Missing dir: {p}"

for p in Path("zmatrix/research_db/factor").rglob("*.py"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    for token in [
        "real_trade_allowed=True",
        "broker_order_allowed=True",
        "runtime_enabled=True",
        "auto_buy_allowed=True",
        "auto_sell_allowed=True",
        "production_allowed=True",
    ]:
        assert token not in text, f"Forbidden production flag {token} in {p}"

print("✅ ResearchDB Phase 4 FactorFactory verification PASS")
PY

echo "═══ ResearchDB Phase 4 PASS ═══"
```

---

# 十三、样例 fixture

允许创建：

```text
tests/fixtures/factor/
  sample_factor_registry.csv
  sample_factor_observation.csv
  sample_factor_outcome.csv
  sample_sector_holdout.csv
  sample_regime_holdout.csv
  sample_executable_return.csv
```

fixture 必须是虚构数据或极小公开示例，不得包含真实账户完整数据。

---

# 十四、报告要求

## 14.1 factor_validation_report.md

必须包含：

```text
验证因子总数
进入 validation 的因子数
被 PIT 阻断因子数
样本不足因子数
IC 正向因子数
RankIC 正向因子数
Decile 单调因子数
WalkForward 稳定因子数
Sector Holdout 通过因子数
Net Executable 通过因子数
推荐 WATCH / REJECT / RESEARCH_ACCEPTED 清单
```

## 14.2 factor_ic_report.md

必须包含：

```text
factor_id
horizon
return_field
sample_size
ic_mean
rankic_mean
ic_positive_ratio
rankic_positive_ratio
quality_status
```

## 14.3 factor_decile_report.md

必须包含：

```text
factor_id
decile return table
top-bottom spread
monotonicity_score
decile_slope
```

## 14.4 factor_promotion_report.md

必须包含：

```text
可晋级因子
不可晋级因子
阻断原因
需要更多样本因子
PIT 风险因子
执行收益拖累因子
```

## 14.5 factor_rejection_report.md

必须包含：

```text
因子名
拒绝原因
样本数
IC/RankIC
Decile
WalkForward
Execution
是否可未来重测
```

---

# 十五、Acceptance Matrix

新增：

```text
docs/research_db/PHASE4_ACCEPTANCE_MATRIX.md
```

内容：

```markdown
# ResearchDB Phase 4 Acceptance Matrix

| Item | Requirement | Status |
|---|---|---|
| P4-1 | Factor registry schema | DONE |
| P4-2 | Factor observation schema | DONE |
| P4-3 | PIT checker | DONE |
| P4-4 | Missing policy | DONE |
| P4-5 | IC calculator | DONE |
| P4-6 | RankIC calculator | DONE |
| P4-7 | Decile return calculator | DONE |
| P4-8 | Monotonicity checker | DONE |
| P4-9 | Walk-forward validator | DONE |
| P4-10 | Sector holdout validator | DONE |
| P4-11 | Regime holdout validator | DONE |
| P4-12 | Net executable validator | DONE |
| P4-13 | Factor quality scorer | DONE |
| P4-14 | Promotion gate | DONE |
| P4-15 | Rejection policy | DONE |
| P4-16 | Factor validation report | DONE |
| P4-17 | Tests | DONE |
| P4-18 | Verify script | DONE |
| P4-19 | No production boundary | DONE |

Final Status: PHASE4_READY_FOR_AUTOCASEFORGE_INTEGRATION  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  
```

---

# 十六、Closeout Report

新增：

```text
docs/research_db/PHASE4_CLOSEOUT_REPORT.md
```

内容必须包含：

```markdown
# ResearchDB Phase 4 Closeout Report

## Final Status

ResearchDB Phase 4: PASS  
Next Phase: Phase 5 AutoCaseForge Integration  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  

## Completed

- Factor registry schema
- Factor observation schema
- PIT checker
- Missing policy
- IC calculator
- RankIC calculator
- Decile return calculator
- Monotonicity checker
- Walk-forward validator
- Sector holdout validator
- Regime holdout validator
- Net executable validator
- Factor quality scorer
- Promotion gate
- Rejection policy
- Factor validation report
- Tests
- Verify script

## Hard Boundaries

- No real trade
- No broker
- No runtime
- No production
- No automatic rule promotion
- No LLM subjective continuous score
- No CURRENT_SNAPSHOT_ONLY historical backtest
- No insufficient T20/T60 validation
- No paper-only alpha treated as executable alpha

## Data Import Status

Factor registry created: FALSE / TRUE  
Factor observations generated: FALSE / TRUE  
IC/RankIC generated: FALSE / TRUE  
Decile return generated: FALSE / TRUE  

## Next Step

Proceed to Phase 5: AutoCaseForge Integration.

Phase 5 may create:
- event_ledger.jsonl
- case_ledger.jsonl
- decision_ledger.jsonl
- outcome_ledger.jsonl
- rule_candidate_ledger.jsonl
- memory_candidate_ledger.jsonl

Phase 5 must not:
- generate trade signal
- enable production
- modify RC1 status
```

---

# 十七、执行批次

## Batch P4-A：目录与 registry schema

```text
创建 factor registry/observations/validation/promotion/reports 目录
创建 factor_registry_schema / observation_schema / group_schema / source_policy / versioning
```

Commit：

```bash
git add .
git commit -m "researchdb-phase4-a: add factor factory directories and schemas"
```

## Batch P4-B：因子观测与 PIT/Missing

```text
实现 factor_loader / factor_observation_builder / factor_pit_checker / factor_missing_policy
```

Commit：

```bash
git add .
git commit -m "researchdb-phase4-b: implement factor observation and pit checks"
```

## Batch P4-C：IC / RankIC / Decile

```text
实现 ic_calculator / rankic_calculator / decile_return_calculator / monotonicity_checker
```

Commit：

```bash
git add .
git commit -m "researchdb-phase4-c: implement ic rankic and decile validation"
```

## Batch P4-D：稳健性验证

```text
实现 walkforward / sector_holdout / regime_holdout / executable_factor_validator
```

Commit：

```bash
git add .
git commit -m "researchdb-phase4-d: implement factor robustness validators"
```

## Batch P4-E：质量评分与晋级淘汰

```text
实现 factor_quality_scorer / promotion_gate / rejection_policy / validation_report
```

Commit：

```bash
git add .
git commit -m "researchdb-phase4-e: implement factor scoring promotion and reports"
```

## Batch P4-F：测试与 verify

```text
创建 tests/research_db/factor/
创建 verify_research_db_phase4_factor_factory.sh
跑全量测试
```

Commit：

```bash
git add .
git commit -m "researchdb-phase4-f: add factor factory tests and verification"
```

## Batch P4-G：closeout

```text
更新 PHASE4_ACCEPTANCE_MATRIX.md
更新 PHASE4_CLOSEOUT_REPORT.md
跑 verify
```

Commit：

```bash
git add .
git commit -m "researchdb-phase4-g: close phase4 factor factory foundation"
```

---

# 十八、运行命令

OpenClaw 必须执行：

```bash
python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/factor/

bash scripts/verify_research_db_phase4_factor_factory.sh
```

建议同时复跑前置阶段：

```bash
bash scripts/verify_research_db_phase0.sh
bash scripts/verify_research_db_phase1_account_truth.sh
bash scripts/verify_research_db_phase2_universe_mapping.sh
bash scripts/verify_research_db_phase3_market_outcome.sh
```

如果任何一条失败：

```text
不得提交 closeout。
不得进入 Phase 5。
```

---

# 十九、完成报告格式

OpenClaw 完成后必须输出：

```text
## ResearchDB Phase 4 完成报告

commit:
branch:

### Directories
- factor/registry:
- factor/observations:
- factor/validation:
- factor/promotion:
- factor/reports:

### Schemas
- factor_registry:
- factor_observation:
- factor_group:
- factor_source:
- factor_version:

### Code
- factor_registry_schema:
- factor_observation_schema:
- factor_group_schema:
- factor_source_policy:
- factor_versioning:
- factor_loader:
- factor_observation_builder:
- factor_pit_checker:
- factor_missing_policy:
- ic_calculator:
- rankic_calculator:
- decile_return_calculator:
- monotonicity_checker:
- walkforward_validator:
- sector_holdout_validator:
- regime_holdout_validator:
- executable_factor_validator:
- factor_quality_scorer:
- factor_promotion_gate:
- factor_rejection_policy:
- factor_validation_report:

### Reports
- factor_validation_report:
- factor_ic_report:
- factor_decile_report:
- factor_promotion_report:
- factor_rejection_report:

### Tests
- tests/research_db/factor:
- verify_research_db_phase4_factor_factory.sh:
- previous phase verifies:

### Data Safety
- production flags:
- CURRENT_SNAPSHOT_ONLY historical use:
- PIT_UNSAFE validation:
- insufficient T20/T60 use:
- LLM subjective continuous score:

### Final Status
ResearchDB Phase 4: PASS / FAIL
Next Phase: Phase 5 AutoCaseForge Integration
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 二十、通过标准

Phase 4 只有在以下全部满足时通过：

```text
1. factor registry 目录存在。
2. factor observations 目录存在。
3. factor validation 目录存在。
4. factor promotion 目录存在。
5. factor_registry_schema 可运行。
6. factor_observation_schema 可运行。
7. PIT checker 可运行。
8. missing policy 可运行。
9. IC calculator 可运行。
10. RankIC calculator 可运行。
11. Decile return calculator 可运行。
12. Monotonicity checker 可运行。
13. Walk-forward validator 可运行。
14. Sector holdout validator 可运行。
15. Regime holdout validator 可运行。
16. Executable factor validator 可运行。
17. Factor quality scorer 可运行。
18. Promotion gate 可运行。
19. Rejection policy 可运行。
20. Factor validation report 可生成。
21. tests/research_db/factor/ 全部通过。
22. verify_research_db_phase4_factor_factory.sh 通过。
23. 不存在 production/broker/runtime/real_trade flags。
24. Closeout Report 允许进入 Phase 5。
```

---

# 二十一、阶段结束后的状态

Phase 4 完成后，系统状态应为：

```text
ResearchDB Phase 4: PASS
ResearchDB Status: READY_FOR_AUTOCASEFORGE_INTEGRATION
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
RC1 status: unchanged
```

Phase 4 完成后，并不意味着所有因子都已有效。  
它意味着：

```text
系统已经具备注册因子、观测因子、验证 IC/RankIC/Decile、做稳健性检验、做因子晋级淘汰的工程能力。
```

---

# 二十二、真实数据填充建议

当 Phase 4 工程完成后，真实填充建议分三步：

## Step 1：先注册历史交易相关因子

```text
从 Phase 1/2/3 提取：
R-Matrix 信号
ZC35 催化标签
ZC40 执行状态
ZC50 账户状态
行业/主题/链条标签
```

## Step 2：优先验证与你实盘相关的因子

```text
先验证过去 5 年实际交易/观察过的股票。
不要先做全市场因子大海捞针。
```

## Step 3：生成第一版 Factor Validation Report

优先输出：

```text
哪些因子明显无效
哪些因子样本不足
哪些因子只在某些行业有效
哪些因子纸面有效但不可执行
哪些因子值得进入 CaseForge 规则候选
```

---

# 二十三、与后续阶段关系

## 对 Phase 5 的支持

AutoCaseForge 依赖 Phase 4 输出：

```text
factor_validated
factor_rejected
factor_watch
factor_promotion_candidate
```

用于自动建案和规则候选。

## 对 Phase 8 的支持

行业/产业链知识库需要 Phase 4 回答：

```text
哪些行业因子有效？
哪些产业链标签有 alpha？
哪些链条只是叙事？
```

## 对 Phase 9 的支持

个人操盘画像需要 Phase 4 回答：

```text
哪些信号对你有效？
哪些信号反复误导你？
哪些因子适合你的账户？
```

---

# 二十四、最终裁决

Phase 4 的本质是：

```text
把 Z-MATRIX 的研究信号从“看起来有道理”，升级为“经过统计验证”。
```

没有 Phase 4，你无法区分：

```text
真正有预测力的信号
后验解释出来的幻觉
只能纸面有效的信号
执行后无效的信号
只在特定行业有效的信号
```

完成 Phase 4 后，Z-MATRIX-OS 才能进入真正的自动案例记忆阶段：

```text
Phase 5：AutoCaseForge 案例记忆与自动内化系统
```

这一步会把因子验证结果、交易结果、观察结果、催化失效、执行失败、账户反馈自动沉淀成长期记忆。


---

# Phase 4 A+ 额外加固项

## P4-A+ 因子输入禁止 LLM 连续主观分数

新增扫描脚本：

```text
scripts/verify_research_db_phase4_no_llm_subjective_score.sh
```

禁止业务 schema / fixture / output 出现：

```text
moat_score
growth_score
buy_score
quality_score_by_llm
score_from_llm
```

如果是 deterministic scorer 输出，必须字段名包含：

```text
score_trace
rule_based_score
deterministic_score
```

## P4-A+ Promotion Evidence Bundle

每个晋级因子必须生成 evidence bundle：

```json
{
  "factor_id": "",
  "ic_evidence": {},
  "rankic_evidence": {},
  "decile_evidence": {},
  "walkforward_evidence": {},
  "holdout_evidence": {},
  "execution_evidence": {},
  "blocked_reasons": [],
  "human_review_required": true,
  "production_allowed": false
}
```


---

# A/A+ 统一防漂移验收清单

OpenClaw 完成本文档后，必须逐项自检：

```text
[ ] 是否严格按本文档目录创建文件？
[ ] 是否所有 schema 都有 enum 与 required fields？
[ ] 是否所有核心函数都有明确返回结构？
[ ] 是否所有 fixture 都是虚构或非私有样本？
[ ] 是否所有真实私有 raw 数据已被 .gitignore 阻断？
[ ] 是否所有 tests 都运行通过？
[ ] 是否 verify 脚本运行通过？
[ ] 是否 Acceptance Matrix 与真实完成状态一致？
[ ] 是否 Closeout Report 没有夸大完成度？
[ ] 是否 production/broker/runtime/real_trade 全部 BLOCKED？
[ ] 是否没有自动进入下一 Phase？
```

最终状态只能是：

```text
PASS：全部完成，允许人工裁决进入下一 Phase
PARTIAL：有非阻断缺口，不能进入下一 Phase
BLOCKED：存在硬门失败，必须修复
```

---

# 交付给用户的完成报告模板

```text
## <Phase Name> 完成报告

commit:
branch:

### Scope
- phase:
- mode: Research Only / Paper Only
- production:
- broker/runtime:
- real trade:

### Implementation
- docs:
- data directories:
- code modules:
- fixtures:
- reports:

### Tests
- pytest:
- verify script:
- safety scan:

### Acceptance Matrix
- DONE:
- PARTIAL:
- BLOCKED:

### Known Limitations
- ...

### Final Decision
PASS / PARTIAL / BLOCKED

### Next Step
等待人工批准是否进入下一 Phase。
```
