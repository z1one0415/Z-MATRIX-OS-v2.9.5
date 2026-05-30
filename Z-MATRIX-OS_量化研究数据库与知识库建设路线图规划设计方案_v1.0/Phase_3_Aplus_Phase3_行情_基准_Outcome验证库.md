# Phase 3：行情/基准/Outcome 验证库｜A+加固执行版

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

# Phase 3：行情/基准/Outcome 验证库

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 3  
> **阶段名称**：Market & Benchmark Outcome Engine｜行情/基准/Outcome 验证库  
> **前置阶段**：Phase 0：ResearchDB 宪法与目录冻结；Phase 1：5年实盘真相库；Phase 2：标的主数据 + 行业/产业链映射库  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：行情数据治理 / 基准收益计算 / 严格 Forward Horizon / 交易成本模型 / 后验 Outcome 验证 / Alpha 归因  
> **阶段目标**：建立所有交易、信号、观察仓、候选仓在 T1/T3/T5/T10/T20/T60 的后验验证库，计算个股收益、行业基准收益、主题基准收益、市场收益、净可执行收益、最大浮盈、最大浮亏、alpha 与成交失败风险，为 Phase 4 FactorFactory、Phase 5 AutoCaseForge、Phase 9 个人操盘画像提供量化事实底座。  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 3 是 Z-MATRIX-OS 从“记录过去”进入“验证过去”的关键阶段。

Phase 1 解决：

```text
我过去买了什么、赚了多少、亏了多少。
```

Phase 2 解决：

```text
我买的股票属于什么行业、产业链、主题，应该跟谁比较。
```

Phase 3 解决：

```text
这些交易、信号、观察对象，在真实行情中到底有没有 alpha？
```

本阶段只允许做：

```text
1. 建立个股日线行情库
2. 建立指数/行业/主题/peer benchmark 行情库
3. 建立严格 T1/T3/T5/T10/T20/T60 Outcome 计算引擎
4. 建立交易成本与可执行收益模型
5. 建立 watchlist/candidate/trade/signal 后验验证表
6. 建立 limit-up / limit-down / suspension / one-price board 执行阻断字段
7. 输出 Outcome 验证报告
```

本阶段禁止：

```text
1. 不生成买卖建议
2. 不接 broker
3. 不开启 runtime
4. 不进入 production
5. 不改 RC1 状态
6. 不把不足 T20/T60 的样本标为 READY
7. 不用最后价格代替不足 forward trading days
8. 不把毛收益当净收益
9. 不忽略涨跌停、停牌、一字板、滑点
10. 不自动晋级因子或规则
```

---

# 一、Phase 3 的核心价值

Phase 3 要回答 10 个研究问题：

```text
1. 每个信号 T5/T20/T60 后到底涨了还是跌了？
2. 涨跌是个股 alpha，还是行业 beta？
3. 某笔交易跑赢了行业、主题、同行，还是只是跟随市场？
4. 观察仓没买的股票后来涨了多少？
5. 候选仓筛选是否有召回能力？
6. 某个 R-Matrix 信号是否有后验胜率？
7. 某个 ZC35 催化信号是否在半衰期内兑现？
8. 某个 B-Matrix 截面因子是否对应未来收益？
9. 纸面收益扣除交易成本和成交失败后还剩多少？
10. 哪些收益在真实执行中根本拿不到？
```

没有 Phase 3，FactorFactory 无法验证，CaseForge 无法归因，个人操盘画像无法成立。

---

# 二、Phase 3 输入边界

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

## 2.3 Phase 3 自有输入

```text
个股日线行情
指数日线行情
行业指数行情
主题篮子行情
ETF 行情
涨跌停状态
停牌状态
交易日历
复权因子
```

---

# 三、必须创建的数据目录

```text
data/research_db/market/
  README.md

  raw/
    README.md
    daily_price_imports/
      .gitkeep
    index_price_imports/
      .gitkeep
    benchmark_price_imports/
      .gitkeep

  staging/
    imported_daily_price_raw.csv
    imported_index_daily_raw.csv
    imported_industry_benchmark_raw.csv
    imported_theme_basket_raw.csv
    imported_trade_calendar_raw.csv
    import_error_rows.csv

  normalized/
    daily_price_5y.parquet
    index_daily.parquet
    industry_benchmark_daily.parquet
    theme_basket_daily.parquet
    peer_basket_daily.parquet
    etf_daily.parquet
    limit_board_daily.csv
    suspension_daily.csv
    trade_calendar.csv
    adjustment_factor.csv

  reports/
    market_data_quality_report.md
    benchmark_coverage_report.md
    missing_price_report.md
    limit_board_report.md
    trade_calendar_report.md

data/research_db/outcome/
  README.md

  normalized/
    signal_outcome_t1_t3_t5_t10_t20_t60.parquet
    trade_outcome.parquet
    watchlist_outcome.parquet
    candidate_outcome.parquet
    benchmark_alpha_outcome.parquet
    executable_return_outcome.parquet
    outcome_quality_ledger.csv

  reports/
    outcome_validation_report.md
    account_alpha_report.md
    watchlist_opportunity_report.md
    signal_horizon_report.md
    executable_return_report.md
```

---

# 四、必须创建的代码模块

```text
zmatrix/research_db/outcome/
  __init__.py
  trade_calendar.py
  market_price_schema.py
  benchmark_schema.py
  price_loader.py
  price_normalizer.py
  benchmark_resolver.py
  forward_horizon.py
  return_calculator.py
  alpha_calculator.py
  execution_cost_model.py
  executable_return.py
  limit_board_detector.py
  suspension_detector.py
  outcome_builder.py
  signal_outcome_builder.py
  trade_outcome_builder.py
  watchlist_outcome_builder.py
  candidate_outcome_builder.py
  outcome_quality_checker.py
  outcome_report.py
```

---

# 五、核心数据表规范

## 5.1 daily_price_5y.parquet

### 字段

```csv
date,ticker,name,open,high,low,close,pre_close,volume,amount,turnover,pct_chg,adj_factor,adj_open,adj_high,adj_low,adj_close,source,data_status,quality_status
```

### 硬规则

```text
date + ticker 必须唯一。
close 不得为空。
pct_chg 必须可由 close/pre_close 校验。
复权价格必须保留 adj_close。
quality_status=ERROR 的行情不得进入 outcome。
```

---

## 5.2 index_daily.parquet

### 字段

```csv
date,index_id,index_name,open,high,low,close,pre_close,volume,amount,pct_chg,source,data_status,quality_status
```

### index 类型

```text
MARKET_INDEX
BROAD_INDEX
STYLE_INDEX
INDUSTRY_INDEX
THEME_INDEX
CUSTOM_BASKET
```

---

## 5.3 industry_benchmark_daily.parquet

### 字段

```csv
date,benchmark_id,benchmark_name,industry_l1,industry_l2,open,high,low,close,pre_close,pct_chg,source,data_status,quality_status
```

---

## 5.4 theme_basket_daily.parquet

### 字段

```csv
date,theme_id,theme_name,basket_method,constituents_count,close,pre_close,pct_chg,equal_weight_return,float_mcap_weight_return,source,data_status,quality_status
```

### basket_method

```text
EQUAL_WEIGHT
FLOAT_MCAP_WEIGHT
CUSTOM_WEIGHT
MANUAL
```

---

## 5.5 peer_basket_daily.parquet

### 字段

```csv
date,peer_group_id,peer_group_name,constituents_count,equal_weight_return,median_return,top_quartile_return,bottom_quartile_return,source,data_status,quality_status
```

---

## 5.6 limit_board_daily.csv

### 字段

```csv
date,ticker,name,limit_up,limit_down,one_price_limit_up,one_price_limit_down,open_board,close_board,limit_up_price,limit_down_price,quality_status
```

### 规则

```text
one_price_limit_up = open=high=low=close 且 pct_chg 达涨停阈值
one_price_limit_down = open=high=low=close 且 pct_chg 达跌停阈值
```

---

## 5.7 suspension_daily.csv

### 字段

```csv
date,ticker,name,suspended,suspension_reason,resume_date,quality_status
```

---

## 5.8 trade_calendar.csv

### 字段

```csv
date,is_trading_day,market,previous_trading_day,next_trading_day,holiday_name
```

---

# 六、Outcome 表规范

## 6.1 signal_outcome_t1_t3_t5_t10_t20_t60.parquet

### 字段

```csv
signal_id,ticker,name,signal_date,horizon,required_forward_days,available_forward_days,ready,blocked_reason,entry_price,exit_date,exit_price,gross_return,market_return,industry_return,theme_return,peer_return,alpha_vs_market,alpha_vs_industry,alpha_vs_theme,alpha_vs_peer,max_favorable_excursion,max_adverse_excursion,net_executable_return,execution_blocked,execution_blocked_reason,quality_status
```

### 硬规则

```text
T20 必须 required_forward_days=20。
T60 必须 required_forward_days=60。
available_forward_days < required_forward_days 时：
  ready=false
  blocked_reason=INSUFFICIENT_FORWARD_TRADING_DAYS
  gross_return=null
  alpha=null
  fallback_last_price_allowed=false
```

---

## 6.2 trade_outcome.parquet

### 字段

```csv
trade_id,ticker,name,trade_date,side,horizon,ready,entry_price,exit_date,exit_price,gross_return,net_return_after_cost,industry_return,theme_return,alpha_vs_industry,alpha_vs_theme,mfe,mae,execution_blocked,quality_status
```

---

## 6.3 watchlist_outcome.parquet

### 字段

```csv
watch_id,ticker,name,watch_date,horizon,ready,watch_price,exit_date,exit_price,gross_return,industry_return,theme_return,alpha_vs_industry,missed_opportunity_flag,mfe,mae,quality_status
```

### missed_opportunity_flag

```text
true，当观察对象未买入，但 T5/T20 跑赢行业超过阈值。
```

---

## 6.4 candidate_outcome.parquet

### 字段

```csv
candidate_id,ticker,name,candidate_date,horizon,ready,candidate_score,candidate_price,exit_date,exit_price,gross_return,industry_return,theme_return,alpha_vs_industry,true_signal_candidate,false_positive_candidate,quality_status
```

---

## 6.5 benchmark_alpha_outcome.parquet

### 字段

```csv
object_id,object_type,ticker,name,date,horizon,stock_return,market_return,industry_return,theme_return,peer_return,alpha_vs_market,alpha_vs_industry,alpha_vs_theme,alpha_vs_peer,quality_status
```

---

## 6.6 executable_return_outcome.parquet

### 字段

```csv
object_id,object_type,ticker,date,horizon,gross_return,commission,stamp_duty,slippage,limit_up_buy_failure,limit_down_sell_failure,suspension_block,one_price_limit_board_block,net_executable_return,executable,blocked_reason,quality_status
```

---

## 6.7 outcome_quality_ledger.csv

### 字段

```csv
outcome_id,object_type,ticker,horizon,quality_status,ready,blocked_reason,missing_price,missing_benchmark,missing_calendar,execution_data_missing,updated_at
```

---

# 七、严格 Forward Horizon 规则

## 7.1 支持 horizon

```python
HORIZON_DAYS = {
    "T1": 1,
    "T3": 3,
    "T5": 5,
    "T10": 10,
    "T20": 20,
    "T60": 60,
}
```

## 7.2 交易日规则

```text
forward trading days 必须基于 trade_calendar。
自然日不得替代交易日。
停牌日不得算作有效 exit 价格。
T20/T60 不足，不得用最后可见价格。
```

## 7.3 不足窗口返回

```json
{
  "horizon": "T20",
  "required_forward_days": 20,
  "available_forward_days": 18,
  "ready": false,
  "blocked_reason": "INSUFFICIENT_FORWARD_TRADING_DAYS",
  "fallback_last_price_allowed": false
}
```

---

# 八、收益计算规则

## 8.1 毛收益

```text
gross_return = exit_price / entry_price - 1
```

## 8.2 市场 alpha

```text
alpha_vs_market = stock_return - market_return
```

## 8.3 行业 alpha

```text
alpha_vs_industry = stock_return - industry_return
```

## 8.4 主题 alpha

```text
alpha_vs_theme = stock_return - theme_return
```

## 8.5 同类股 alpha

```text
alpha_vs_peer = stock_return - peer_return
```

## 8.6 MFE / MAE

```text
MFE = horizon 内最高价 / entry_price - 1
MAE = horizon 内最低价 / entry_price - 1
```

---

# 九、交易成本与可执行收益模型

## 9.1 成本字段

```text
commission
stamp_duty
transfer_fee
slippage
```

## 9.2 最低默认参数

```text
commission_bps = 2.5
stamp_duty_bps = 5.0 on SELL only
transfer_fee_bps = 0.1
default_slippage_bps = 5.0
```

注意：默认参数只用于 paper research，不代表真实券商费率。

## 9.3 执行阻断

必须支持：

```text
limit_up_buy_failure
limit_down_sell_failure
suspension_block
one_price_limit_board_block
missing_price_block
liquidity_data_missing
```

## 9.4 不可执行返回

```json
{
  "executable": false,
  "net_executable_return": null,
  "blocked_reason": "ONE_PRICE_LIMIT_UP_BUY_FAILURE"
}
```

## 9.5 硬规则

```text
不可执行样本不得计算 net_executable_return。
不可成交收益不得当成真实可获得 alpha。
```

---

# 十、代码模块设计

## 10.1 trade_calendar.py

提供：

```python
def get_forward_trading_date(start_date: str, horizon_days: int, calendar_rows: list[dict]) -> dict:
    ...

def count_available_forward_days(start_date: str, end_date: str, calendar_rows: list[dict]) -> int:
    ...

def validate_forward_horizon(start_date: str, horizon: str, calendar_rows: list[dict]) -> dict:
    ...
```

必须支持：

```text
INSUFFICIENT_FORWARD_TRADING_DAYS
MISSING_TRADE_CALENDAR
```

---

## 10.2 market_price_schema.py

提供：

```python
def validate_daily_price_row(row: dict) -> dict:
    ...
```

必须验证：

```text
date
ticker
close
pre_close
pct_chg
quality_status
```

---

## 10.3 price_loader.py

提供：

```python
def load_daily_prices(path: str) -> list[dict]:
    ...

def get_price(ticker: str, date: str, price_rows: list[dict], price_field: str = "adj_close") -> dict:
    ...
```

---

## 10.4 benchmark_resolver.py

提供：

```python
def resolve_benchmarks(ticker: str, benchmark_mapping_rows: list[dict]) -> dict:
    ...
```

返回：

```json
{
  "market_benchmark": "...",
  "industry_benchmark": "...",
  "theme_benchmark": "...",
  "peer_benchmark": "..."
}
```

---

## 10.5 return_calculator.py

提供：

```python
def calculate_return(entry_price: float, exit_price: float) -> dict:
    ...

def calculate_mfe_mae(entry_price: float, path_rows: list[dict]) -> dict:
    ...
```

---

## 10.6 alpha_calculator.py

提供：

```python
def calculate_alpha(stock_return: float, benchmark_return: float | None) -> dict:
    ...
```

如果 benchmark 缺失：

```json
{
  "alpha": null,
  "quality_status": "MISSING_BENCHMARK"
}
```

---

## 10.7 execution_cost_model.py

提供：

```python
def calculate_transaction_cost(side: str, amount: float, config: dict | None = None) -> dict:
    ...
```

返回：

```json
{
  "commission": 0.0,
  "stamp_duty": 0.0,
  "transfer_fee": 0.0,
  "slippage": 0.0,
  "total_cost": 0.0
}
```

---

## 10.8 limit_board_detector.py

提供：

```python
def detect_limit_board(price_row: dict) -> dict:
    ...
```

输出：

```json
{
  "limit_up": false,
  "limit_down": false,
  "one_price_limit_up": false,
  "one_price_limit_down": false
}
```

---

## 10.9 executable_return.py

提供：

```python
def calculate_executable_return(
    side: str,
    entry_price: float,
    exit_price: float,
    amount: float,
    entry_limit_status: dict,
    exit_limit_status: dict,
    suspension_status: dict | None = None,
    cost_config: dict | None = None,
) -> dict:
    ...
```

必须处理：

```text
买入日一字涨停 → executable=false
卖出日一字跌停 → executable=false
停牌 → executable=false
否则扣成本计算 net_executable_return
```

---

## 10.10 outcome_builder.py

提供通用 outcome 构建：

```python
def build_outcome_for_object(
    object_id: str,
    object_type: str,
    ticker: str,
    start_date: str,
    entry_price: float,
    horizons: list[str],
    price_rows: list[dict],
    benchmark_rows: dict,
    calendar_rows: list[dict],
) -> list[dict]:
    ...
```

---

## 10.11 signal_outcome_builder.py

```python
def build_signal_outcomes(signal_rows: list[dict], market_data: dict) -> list[dict]:
    ...
```

---

## 10.12 trade_outcome_builder.py

```python
def build_trade_outcomes(trade_rows: list[dict], market_data: dict) -> list[dict]:
    ...
```

---

## 10.13 watchlist_outcome_builder.py

```python
def build_watchlist_outcomes(watchlist_rows: list[dict], market_data: dict) -> list[dict]:
    ...
```

---

## 10.14 candidate_outcome_builder.py

```python
def build_candidate_outcomes(candidate_rows: list[dict], market_data: dict) -> list[dict]:
    ...
```

---

## 10.15 outcome_quality_checker.py

```python
def check_outcome_quality(outcome_rows: list[dict]) -> dict:
    ...
```

---

## 10.16 outcome_report.py

```python
def generate_outcome_validation_report(summary: dict, output_path: str) -> dict:
    ...
```

---

# 十一、测试要求

## 11.1 测试目录

```text
tests/research_db/outcome/
  test_trade_calendar.py
  test_market_price_schema.py
  test_price_loader.py
  test_benchmark_resolver.py
  test_forward_horizon_strict.py
  test_return_calculator.py
  test_alpha_calculator.py
  test_execution_cost_model.py
  test_limit_board_detector.py
  test_executable_return.py
  test_signal_outcome_builder.py
  test_trade_outcome_builder.py
  test_watchlist_outcome_builder.py
  test_candidate_outcome_builder.py
  test_outcome_quality_checker.py
  test_outcome_report.py
  test_no_production_boundary.py
```

---

## 11.2 必须测试的场景

### trade_calendar

```text
T20 available=20 → ready=true
T20 available=19 → ready=false
T60 available=60 → ready=true
T60 available=59 → ready=false
自然日不得替代交易日
```

### price_loader

```text
能获取某 ticker 某 date 的 adj_close
价格缺失 → MISSING_PRICE
停牌日价格缺失 → SUSPENSION_OR_MISSING_PRICE
```

### alpha_calculator

```text
stock_return=10%, benchmark=6% → alpha=4%
benchmark 缺失 → MISSING_BENCHMARK
```

### executable_return

```text
买入日一字涨停 → executable=false
卖出日一字跌停 → executable=false
停牌 → executable=false
普通交易 → net_executable_return 扣成本
```

### signal_outcome_builder

```text
信号 T5/T20 输出完整
T20 不足阻断
alpha_vs_industry 正确
```

### watchlist_outcome_builder

```text
观察股未买但 T5 跑赢行业超过阈值 → missed_opportunity_flag=true
```

### outcome_quality_checker

```text
缺 price
缺 benchmark
缺 calendar
缺 execution data
都必须进入 quality ledger
```

### no_production_boundary

```text
所有 outcome 输出 production_allowed=false
real_trade_allowed=false
broker_order_allowed=false
runtime_enabled=false
```

---

# 十二、verify 脚本

新增：

```text
scripts/verify_research_db_phase3_market_outcome.sh
```

内容必须执行：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 3 Market Outcome Verification ═══"

python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/outcome/

python3 - <<'PY'
from pathlib import Path

required_modules = [
    "zmatrix/research_db/outcome/trade_calendar.py",
    "zmatrix/research_db/outcome/market_price_schema.py",
    "zmatrix/research_db/outcome/benchmark_schema.py",
    "zmatrix/research_db/outcome/price_loader.py",
    "zmatrix/research_db/outcome/price_normalizer.py",
    "zmatrix/research_db/outcome/benchmark_resolver.py",
    "zmatrix/research_db/outcome/forward_horizon.py",
    "zmatrix/research_db/outcome/return_calculator.py",
    "zmatrix/research_db/outcome/alpha_calculator.py",
    "zmatrix/research_db/outcome/execution_cost_model.py",
    "zmatrix/research_db/outcome/executable_return.py",
    "zmatrix/research_db/outcome/limit_board_detector.py",
    "zmatrix/research_db/outcome/suspension_detector.py",
    "zmatrix/research_db/outcome/outcome_builder.py",
    "zmatrix/research_db/outcome/signal_outcome_builder.py",
    "zmatrix/research_db/outcome/trade_outcome_builder.py",
    "zmatrix/research_db/outcome/watchlist_outcome_builder.py",
    "zmatrix/research_db/outcome/candidate_outcome_builder.py",
    "zmatrix/research_db/outcome/outcome_quality_checker.py",
    "zmatrix/research_db/outcome/outcome_report.py",
]

for p in required_modules:
    assert Path(p).exists(), f"Missing module: {p}"

required_dirs = [
    "data/research_db/market/normalized",
    "data/research_db/market/reports",
    "data/research_db/outcome/normalized",
    "data/research_db/outcome/reports",
]

for p in required_dirs:
    assert Path(p).exists(), f"Missing dir: {p}"

for p in Path("zmatrix/research_db/outcome").rglob("*.py"):
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

print("✅ ResearchDB Phase 3 Market Outcome verification PASS")
PY

echo "═══ ResearchDB Phase 3 PASS ═══"
```

---

# 十三、样例 fixture

允许创建：

```text
tests/fixtures/outcome/
  sample_trade_calendar.csv
  sample_daily_prices.csv
  sample_index_daily.csv
  sample_benchmark_mapping.csv
  sample_signal_ledger.csv
  sample_trade_ledger.csv
  sample_watchlist_ledger.csv
  sample_limit_board_daily.csv
  sample_suspension_daily.csv
```

fixture 必须是虚构数据或极小公开示例，不得包含私有账户完整交易数据。

---

# 十四、报告要求

## 14.1 market_data_quality_report.md

必须包含：

```text
行情覆盖股票数
行情覆盖日期范围
缺失价格数量
重复 date+ticker 数量
复权字段覆盖率
停牌数据覆盖率
涨跌停数据覆盖率
```

## 14.2 benchmark_coverage_report.md

必须包含：

```text
有 market benchmark 的标的数
有 industry benchmark 的标的数
有 theme benchmark 的标的数
有 peer benchmark 的标的数
缺失 benchmark 标的清单
```

## 14.3 outcome_validation_report.md

必须包含：

```text
信号数
T5 ready 数
T20 ready 数
T60 ready 数
INSUFFICIENT_FORWARD_TRADING_DAYS 数
平均 gross return
平均 net executable return
平均 alpha_vs_industry
正 alpha 比例
最大 MFE
最大 MAE
```

## 14.4 account_alpha_report.md

必须包含：

```text
交易总数
跑赢行业交易数
跑输行业交易数
alpha 贡献最高交易
alpha 贡献最低交易
按行业 alpha 汇总
按主题 alpha 汇总
```

## 14.5 watchlist_opportunity_report.md

必须包含：

```text
观察对象数量
错过机会数量
T5 跑赢行业 > 5% 的对象
T20 跑赢行业 > 10% 的对象
最大错过收益
```

## 14.6 executable_return_report.md

必须包含：

```text
纸面收益
净可执行收益
交易成本影响
涨停买入失败数量
跌停卖出失败数量
停牌阻断数量
一字板阻断数量
```

---

# 十五、Acceptance Matrix

新增：

```text
docs/research_db/PHASE3_ACCEPTANCE_MATRIX.md
```

内容：

```markdown
# ResearchDB Phase 3 Acceptance Matrix

| Item | Requirement | Status |
|---|---|---|
| P3-1 | Market daily price schema | DONE |
| P3-2 | Index / benchmark schema | DONE |
| P3-3 | Trade calendar | DONE |
| P3-4 | Strict forward horizon | DONE |
| P3-5 | Return calculator | DONE |
| P3-6 | Alpha calculator | DONE |
| P3-7 | Execution cost model | DONE |
| P3-8 | Limit board detector | DONE |
| P3-9 | Suspension detector | DONE |
| P3-10 | Signal outcome builder | DONE |
| P3-11 | Trade outcome builder | DONE |
| P3-12 | Watchlist outcome builder | DONE |
| P3-13 | Candidate outcome builder | DONE |
| P3-14 | Outcome quality checker | DONE |
| P3-15 | Outcome reports | DONE |
| P3-16 | Tests | DONE |
| P3-17 | Verify script | DONE |
| P3-18 | No production boundary | DONE |

Final Status: PHASE3_READY_FOR_FACTOR_VALIDATION_LAYER  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  
```

---

# 十六、Closeout Report

新增：

```text
docs/research_db/PHASE3_CLOSEOUT_REPORT.md
```

内容必须包含：

```markdown
# ResearchDB Phase 3 Closeout Report

## Final Status

ResearchDB Phase 3: PASS  
Next Phase: Phase 4 FactorFactory Validation Layer  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  

## Completed

- Market daily price schema
- Index / benchmark schema
- Trade calendar
- Strict forward horizon
- Return calculator
- Alpha calculator
- Execution cost model
- Limit board detector
- Suspension detector
- Signal outcome builder
- Trade outcome builder
- Watchlist outcome builder
- Candidate outcome builder
- Outcome quality checker
- Outcome reports
- Tests
- Verify script

## Hard Boundaries

- No real trade
- No broker
- No runtime
- No production
- No automatic rule promotion
- No fallback last price for insufficient T20/T60
- No paper gain treated as executable gain

## Data Import Status

Market price data imported: FALSE / TRUE  
Benchmark data imported: FALSE / TRUE  
Outcome generated: FALSE / TRUE  

## Next Step

Proceed to Phase 4: FactorFactory Validation Layer.

Phase 4 may create:
- factor_registry.csv
- factor_observation.parquet
- factor_ic_result.csv
- factor_rankic_result.csv
- factor_decile_return.csv
- factor_promotion_ledger.jsonl

Phase 4 must not:
- generate trade signal
- enable production
- modify RC1 status
```

---

# 十七、执行批次

## Batch P3-A：目录与 schema

```text
创建 market/outcome raw/staging/normalized/reports 目录
创建 price / index / benchmark / trade_calendar / outcome schema
```

Commit：

```bash
git add .
git commit -m "researchdb-phase3-a: add market outcome directories and schemas"
```

## Batch P3-B：行情与交易日历

```text
实现 trade_calendar / price_loader / price_normalizer / benchmark_resolver
```

Commit：

```bash
git add .
git commit -m "researchdb-phase3-b: implement market price and calendar loaders"
```

## Batch P3-C：收益、alpha、可执行收益

```text
实现 forward_horizon / return_calculator / alpha_calculator / execution_cost_model / executable_return / limit_board / suspension
```

Commit：

```bash
git add .
git commit -m "researchdb-phase3-c: implement outcome return and executable return models"
```

## Batch P3-D：Outcome builders

```text
实现 signal/trade/watchlist/candidate outcome builders
```

Commit：

```bash
git add .
git commit -m "researchdb-phase3-d: implement signal trade watchlist candidate outcomes"
```

## Batch P3-E：报告、测试、verify

```text
实现 outcome_quality_checker / outcome_report
创建 tests/research_db/outcome/
创建 verify_research_db_phase3_market_outcome.sh
```

Commit：

```bash
git add .
git commit -m "researchdb-phase3-e: add outcome tests reports and verification"
```

## Batch P3-F：closeout

```text
更新 PHASE3_ACCEPTANCE_MATRIX.md
更新 PHASE3_CLOSEOUT_REPORT.md
跑 verify
```

Commit：

```bash
git add .
git commit -m "researchdb-phase3-f: close phase3 market outcome foundation"
```

---

# 十八、运行命令

OpenClaw 必须执行：

```bash
python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/outcome/

bash scripts/verify_research_db_phase3_market_outcome.sh
```

建议同时复跑前置阶段：

```bash
bash scripts/verify_research_db_phase0.sh
bash scripts/verify_research_db_phase1_account_truth.sh
bash scripts/verify_research_db_phase2_universe_mapping.sh
```

如果任何一条失败：

```text
不得提交 closeout。
不得进入 Phase 4。
```

---

# 十九、完成报告格式

OpenClaw 完成后必须输出：

```text
## ResearchDB Phase 3 完成报告

commit:
branch:

### Directories
- market/raw:
- market/staging:
- market/normalized:
- market/reports:
- outcome/normalized:
- outcome/reports:

### Schemas
- daily_price_5y:
- index_daily:
- industry_benchmark_daily:
- theme_basket_daily:
- peer_basket_daily:
- limit_board_daily:
- suspension_daily:
- trade_calendar:
- signal_outcome:
- trade_outcome:
- watchlist_outcome:
- candidate_outcome:
- executable_return_outcome:

### Code
- trade_calendar:
- market_price_schema:
- benchmark_schema:
- price_loader:
- price_normalizer:
- benchmark_resolver:
- forward_horizon:
- return_calculator:
- alpha_calculator:
- execution_cost_model:
- executable_return:
- limit_board_detector:
- suspension_detector:
- outcome_builder:
- signal_outcome_builder:
- trade_outcome_builder:
- watchlist_outcome_builder:
- candidate_outcome_builder:
- outcome_quality_checker:
- outcome_report:

### Reports
- market_data_quality_report:
- benchmark_coverage_report:
- outcome_validation_report:
- account_alpha_report:
- watchlist_opportunity_report:
- executable_return_report:

### Tests
- tests/research_db/outcome:
- verify_research_db_phase3_market_outcome.sh:
- previous phase verifies:

### Data Safety
- private raw data tracked:
- production flags:
- fallback last price:
- insufficient T20/T60 misuse:

### Final Status
ResearchDB Phase 3: PASS / FAIL
Next Phase: Phase 4 FactorFactory Validation Layer
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 二十、通过标准

Phase 3 只有在以下全部满足时通过：

```text
1. market/outcome 目录存在。
2. 行情与 benchmark schema 明确。
3. trade_calendar 可运行。
4. T20/T60 strict horizon 可测试。
5. return_calculator 可运行。
6. alpha_calculator 可运行。
7. execution_cost_model 可运行。
8. limit_board_detector 可运行。
9. suspension_detector 可运行。
10. executable_return 可运行。
11. signal_outcome_builder 可运行。
12. trade_outcome_builder 可运行。
13. watchlist_outcome_builder 可运行。
14. candidate_outcome_builder 可运行。
15. outcome_quality_checker 可运行。
16. outcome_report 可生成。
17. tests/research_db/outcome/ 全部通过。
18. verify_research_db_phase3_market_outcome.sh 通过。
19. 不存在 production/broker/runtime/real_trade flags。
20. Closeout Report 允许进入 Phase 4。
```

---

# 二十一、阶段结束后的状态

Phase 3 完成后，系统状态应为：

```text
ResearchDB Phase 3: PASS
ResearchDB Status: READY_FOR_FACTOR_VALIDATION_LAYER
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
RC1 status: unchanged
```

Phase 3 完成后，并不意味着已经完成所有真实行情数据导入。  
它意味着：

```text
系统已经具备安全导入行情、绑定基准、计算严格 forward outcome、计算 alpha、扣除交易成本、识别不可执行收益的工程能力。
```

---

# 二十二、真实数据填充建议

当 Phase 3 工程完成后，真实填充建议分三步：

## Step 1：先补历史交易标的行情

```text
从 Phase 1 trade_ledger 和 Phase 2 security_master 提取所有历史交易 ticker。
补 5 年日线行情。
```

## Step 2：补 benchmark 行情

```text
补 market benchmark
补 industry benchmark
补 theme basket
补 peer basket
```

## Step 3：生成第一版 Outcome

优先顺序：

```text
1. trade_outcome
2. watchlist_outcome
3. candidate_outcome
4. signal_outcome
5. benchmark_alpha_outcome
6. executable_return_outcome
```

---

# 二十三、与后续阶段关系

## 对 Phase 4 的支持

FactorFactory 依赖 Phase 3 的：

```text
T5/T20/T60 future return
alpha_vs_industry
alpha_vs_theme
net_executable_return
```

用于：

```text
IC
RankIC
Decile Return
factor promotion
```

## 对 Phase 5 的支持

AutoCaseForge 依赖 Phase 3 的：

```text
missed_opportunity_flag
false_positive_candidate
true_signal_candidate
mfe
mae
execution_blocked
```

用于自动建案。

## 对 Phase 9 的支持

个人操盘画像依赖 Phase 3 的：

```text
行业 alpha
主题 alpha
持仓 alpha
观察仓错过收益
净可执行收益
最大浮亏
```

---

# 二十四、最终裁决

Phase 3 的本质是：

```text
把历史交易、信号、观察仓从“发生过”升级成“验证过”。
```

没有 Phase 3，你无法判断：

```text
你的研究到底有没有 alpha。
```

完成 Phase 3 后，Z-MATRIX-OS 才能进入真正的因子验证阶段：

```text
Phase 4：FactorFactory 因子与信号验证库
```

这一步会开始回答：

```text
哪些信号、因子、标签、催化、账户状态，真的能解释未来收益？
```


---

# Phase 3 A+ 额外加固项

## P3-A+ Strict Horizon Golden Tests

必须新增 golden fixture：

```text
tests/fixtures/outcome/golden_strict_horizon.csv
```

包含至少：

```text
1. T20 exactly 20 trading days → READY
2. T20 only 19 trading days → BLOCKED
3. T60 exactly 60 trading days → READY
4. T60 only 59 trading days → BLOCKED
5. 停牌日不得作为有效 exit day
```

## P3-A+ Executable Return Contract

所有可执行收益必须返回：

```json
{
  "gross_return": 0.0,
  "net_executable_return": 0.0,
  "executable": true,
  "blocked_reason": null,
  "cost_breakdown": {
    "commission": 0.0,
    "stamp_duty": 0.0,
    "transfer_fee": 0.0,
    "slippage": 0.0
  }
}
```

不可执行时：

```json
{
  "executable": false,
  "net_executable_return": null,
  "blocked_reason": "ONE_PRICE_LIMIT_UP_BUY_FAILURE"
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
