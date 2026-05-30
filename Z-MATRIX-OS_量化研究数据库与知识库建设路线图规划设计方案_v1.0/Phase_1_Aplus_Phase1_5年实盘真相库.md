# Phase 1：5年实盘真相库｜A+加固执行版

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

# Phase 1：5年实盘真相库

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 1  
> **阶段名称**：Account Truth Import｜5年实盘真相库  
> **前置阶段**：Phase 0：ResearchDB 宪法与目录冻结  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：实盘数据导入 / 账户曲线重建 / 交易真相审计 / 后续研究数据库的事实底座  
> **阶段目标**：把过去 5 年真实交易、持仓、账户净值、现金流、观察仓和人工决策记录，整理成可验证、可审计、可复盘、可进入 Outcome / CaseForge / FactorFactory 的结构化真相库。  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 1 是整个 ResearchDB 工程的第一座主梁。

本阶段不是为了“分析股票”，也不是为了“生成策略”，而是为了回答一个最朴素但最关键的问题：

```text
过去 5 年，我到底怎么赚、怎么亏、怎么错过、怎么承受波动？
```

如果没有 Phase 1，后续所有行业研究、因子验证、案例复盘都会失去真实锚点。

本阶段只允许做：

```text
1. 导入 5 年实盘交易数据
2. 导入或重建每日账户权益
3. 导入持仓快照
4. 导入现金流与资金进出
5. 导入观察池 / 候选池 / 人工决策记录
6. 清洗、标准化、校验数据
7. 重建账户资金曲线
8. 生成 Account Truth Report
9. 为 Phase 2 / Phase 3 / Phase 5 提供标准化输入
```

本阶段禁止：

```text
1. 不生成买卖建议
2. 不接 broker
3. 不开启 runtime
4. 不执行真实交易
5. 不修改 RC1 状态
6. 不直接做因子有效性结论
7. 不自动晋级规则
8. 不把不完整数据伪装成完整实盘记录
9. 不把估算数据混入真实账户数据
```

---

# 一、Phase 1 的核心价值

你的过去 5 年实盘数据，不只是交易流水。

它应该被重建成 6 个层面的事实资产：

```text
1. Account Truth：账户每日真相
2. Trade Truth：每笔交易真相
3. Position Truth：持仓过程真相
4. Cashflow Truth：资金进出真相
5. Watchlist Truth：观察仓与错过机会真相
6. Decision Truth：当时为什么做与为什么没做
```

Phase 1 完成后，系统必须能回答：

```text
1. 某一年收益来自哪些股票？
2. 某一次大亏来自哪个行业、哪个模式、哪个持仓周期？
3. 哪些交易是赚钱的，哪些只是大盘上涨带来的 beta？
4. 哪些股票没买但后来大涨？
5. 哪些持仓期间最大浮亏超过账户承受？
6. 哪些交易本来应该早退出？
7. 哪些亏损是选股错，哪些是仓位错，哪些是执行错？
```

---

# 二、Phase 1 的输入边界

## 2.1 允许导入的数据

```text
券商导出的成交记录
券商导出的资金流水
券商导出的历史持仓
券商导出的交割单
人工整理的历史交易表
人工整理的观察池记录
人工整理的候选池记录
人工决策日志
账户每日权益截图或 CSV
历史自选股列表
历史研究记录与 thesis 备注
```

## 2.2 数据状态分级

每一条导入数据必须标记 `data_status`：

```text
BROKER_EXPORT：券商原始导出
BROKER_RECONSTRUCTED：从券商数据重建
MANUAL_IMPORT：人工整理导入
PARTIAL_RECONSTRUCTED：部分重建
ESTIMATED：估算数据
UNKNOWN_SOURCE：来源未知
```

## 2.3 使用规则

```text
BROKER_EXPORT：最高可信，可进入账户真相主表
BROKER_RECONSTRUCTED：可进入主表，但需记录重建逻辑
MANUAL_IMPORT：可进入研究，但需人工复核
PARTIAL_RECONSTRUCTED：只能进入辅助分析
ESTIMATED：不得进入最终收益结论
UNKNOWN_SOURCE：默认阻断
```

---

# 三、必须创建的数据目录

Phase 1 必须基于 Phase 0 的 `data/research_db/account/` 扩展。

```text
data/research_db/account/
  raw/
    README.md
    broker_exports/
      .gitkeep
    manual_imports/
      .gitkeep
    screenshots/
      .gitkeep

  normalized/
    account_daily_snapshot.csv
    trade_ledger.csv
    position_ledger.csv
    cashflow_ledger.csv
    holding_pnl_ledger.csv
    account_drawdown_ledger.csv
    capital_curve.csv

  staging/
    imported_trade_raw.csv
    imported_position_raw.csv
    imported_cashflow_raw.csv
    imported_account_snapshot_raw.csv
    import_error_rows.csv

  reports/
    account_truth_report.md
    import_quality_report.md
    reconciliation_report.md
    missing_data_report.md

data/research_db/signal/
  manual_decision_ledger.csv
  thesis_ledger.csv
  human_action_ledger.csv

data/research_db/watchlist/
  watchlist_ledger.csv
  candidate_ledger.csv
  research_universe_ledger.csv
```

如当前没有 `data/research_db/watchlist/`，本阶段允许新增。

---

# 四、必须创建的代码模块

```text
zmatrix/research_db/account_truth/
  __init__.py
  raw_import_schema.py
  trade_normalizer.py
  position_normalizer.py
  cashflow_normalizer.py
  account_snapshot_normalizer.py
  account_reconciler.py
  capital_curve_builder.py
  holding_pnl_builder.py
  drawdown_calculator.py
  trade_quality_checker.py
  missing_data_detector.py
  account_truth_report.py
  import_audit.py
```

---

# 五、核心数据表规范

## 5.1 account_daily_snapshot.csv

### 字段

```csv
date,account_id,total_equity,cash,market_value,daily_pnl,daily_return,cumulative_return,max_drawdown,exposure,turnover,data_status,source_file,ingested_at,quality_status
```

### 字段说明

```text
date：交易日
account_id：账户标识
total_equity：账户总权益
cash：现金
market_value：证券市值
daily_pnl：当日盈亏
daily_return：当日收益率
cumulative_return：累计收益率
max_drawdown：截至当日最大回撤
exposure：仓位暴露 = market_value / total_equity
turnover：当日换手
data_status：数据状态
source_file：来源文件
ingested_at：导入时间
quality_status：READY / PARTIAL / ERROR
```

### 硬规则

```text
total_equity 不得为空。
date 不得重复。
daily_return 必须可由 total_equity 推导或校验。
quality_status=ERROR 的行不得进入 capital_curve。
```

---

## 5.2 trade_ledger.csv

### 字段

```csv
trade_id,account_id,ticker,name,trade_date,side,price,quantity,amount,fee,stamp_duty,transfer_fee,slippage,total_cost,net_amount,source,data_status,source_file,signal_id,thesis_id,human_action_id,created_at,quality_status
```

### side 枚举

```text
BUY
SELL
DIVIDEND
TRANSFER_IN
TRANSFER_OUT
CORRECTION
```

### 硬规则

```text
BUY / SELL 必须有 ticker、trade_date、price、quantity。
amount = price * quantity。
total_cost = fee + stamp_duty + transfer_fee + slippage。
trade_id 必须唯一。
quality_status=ERROR 的交易不得进入收益归因。
```

---

## 5.3 position_ledger.csv

### 字段

```csv
date,account_id,ticker,name,quantity,market_price,market_value,cost_basis,unrealized_pnl,realized_pnl,total_pnl,position_pct,holding_days,thesis_id,data_status,source_file,quality_status
```

### 硬规则

```text
market_value = quantity * market_price。
position_pct = market_value / account_total_equity。
quantity = 0 的记录可保留为持仓关闭记录。
position_pct 不得超过 1，除非标记为 DATA_ERROR。
```

---

## 5.4 cashflow_ledger.csv

### 字段

```csv
cashflow_id,account_id,date,cashflow_type,amount,source,data_status,source_file,notes,quality_status
```

### cashflow_type 枚举

```text
DEPOSIT
WITHDRAW
DIVIDEND
INTEREST
FEE
TAX
CORRECTION
UNKNOWN
```

---

## 5.5 capital_curve.csv

### 字段

```csv
date,account_id,total_equity,net_deposit_adjusted_equity,daily_return,cumulative_return,max_drawdown,rolling_20d_return,rolling_60d_return,quality_status
```

### 硬规则

```text
资金曲线必须扣除入金/出金影响。
不能把新增入金当成投资收益。
出金也不能误算成亏损。
```

---

## 5.6 holding_pnl_ledger.csv

### 字段

```csv
holding_id,account_id,ticker,name,open_date,close_date,holding_days,buy_amount,sell_amount,realized_pnl,unrealized_pnl,total_return,max_favorable_excursion,max_adverse_excursion,exit_reason,quality_status
```

### 作用

为 Phase 3 Outcome 和 Phase 5 CaseForge 提供：

```text
每个持仓的真实结果
最大浮盈
最大浮亏
持有天数
退出原因
```

---

## 5.7 account_drawdown_ledger.csv

### 字段

```csv
drawdown_id,account_id,start_date,trough_date,end_date,drawdown_pct,duration_days,recovery_days,related_positions,related_trades,quality_status
```

### 作用

识别：

```text
哪些股票导致账户回撤
哪些行业导致连续亏损
哪些持仓穿越了风险预算
```

---

## 5.8 manual_decision_ledger.csv

### 字段

```csv
decision_id,date,ticker,name,decision_type,source_module,original_thesis,expected_horizon,confidence,human_action,notes,linked_trade_id,linked_signal_id,data_status,quality_status
```

### decision_type 枚举

```text
BUY_DECISION
SELL_DECISION
WATCH_DECISION
PASS_DECISION
REDUCE_DECISION
ADD_DECISION
REVIEW_DECISION
```

### 作用

这是把“交易流水”升级为“可学习决策样本”的关键表。

---

## 5.9 watchlist_ledger.csv

### 字段

```csv
watch_id,date,ticker,name,watch_reason,source_module,expected_horizon,watch_status,linked_thesis_id,created_by,data_status,quality_status
```

### watch_status 枚举

```text
ACTIVE
REMOVED
PROMOTED_TO_CANDIDATE
PROMOTED_TO_POSITION
MISSED_OPPORTUNITY_REVIEW
```

---

# 六、核心处理流程

Phase 1 的处理流程必须固定为：

```text
Raw Import
→ Schema Validation
→ Normalization
→ Reconciliation
→ Capital Curve Build
→ Holding PnL Build
→ Drawdown Build
→ Quality Report
→ Account Truth Closeout
```

---

## 6.1 Raw Import

输入：

```text
券商成交 CSV
券商资金流水 CSV
历史持仓 CSV
手工交易 CSV
账户净值 CSV
观察池 CSV
```

输出：

```text
data/research_db/account/staging/imported_*_raw.csv
```

不得直接写入 normalized。

---

## 6.2 Schema Validation

验证：

```text
字段是否存在
日期是否可解析
价格/数量/金额是否为数字
side 是否在枚举内
ticker 是否格式正确
source_file 是否记录
```

失败行写入：

```text
data/research_db/account/staging/import_error_rows.csv
```

---

## 6.3 Normalization

把不同来源统一成标准表：

```text
trade_ledger.csv
position_ledger.csv
cashflow_ledger.csv
account_daily_snapshot.csv
```

必须保留：

```text
source_file
data_status
quality_status
ingested_at
```

---

## 6.4 Reconciliation

必须至少做 5 类核对：

```text
1. 交易金额 = price * quantity
2. 账户总权益 = cash + market_value
3. 持仓市值 = quantity * market_price
4. 入金/出金不计入投资收益
5. 卖出数量不得超过可用持仓，除非标记 DATA_ERROR
```

输出：

```text
data/research_db/account/reports/reconciliation_report.md
```

---

## 6.5 Capital Curve Build

必须生成：

```text
capital_curve.csv
```

并区分：

```text
账户总权益曲线
扣除入金/出金后的投资净值曲线
```

---

## 6.6 Holding PnL Build

必须按 ticker + 持仓周期生成：

```text
holding_pnl_ledger.csv
```

支持：

```text
分批买入
分批卖出
部分持仓未关闭
持仓跨年度
```

第一版可以使用 FIFO 成本法。

必须在文档中声明：

```text
cost_method = FIFO
```

---

## 6.7 Drawdown Build

必须生成：

```text
account_drawdown_ledger.csv
```

至少识别：

```text
最大回撤
回撤开始日
回撤最低点
回撤恢复日
回撤持续天数
回撤期间主要持仓
```

---

# 七、数据质量状态

每张表每行必须有 `quality_status`：

```text
READY
PARTIAL
ERROR
MISSING_REQUIRED_FIELD
RECONCILIATION_FAILED
ESTIMATED_ONLY
```

## 使用规则

```text
READY：可进入后续分析
PARTIAL：可进入研究，但必须标注不足
ERROR：不得进入分析
MISSING_REQUIRED_FIELD：不得进入分析
RECONCILIATION_FAILED：不得进入收益结论
ESTIMATED_ONLY：不得进入最终账户真相
```

---

# 八、OpenClaw 执行边界

## 8.1 允许

```text
创建目录
创建 schema
创建 normalizer
创建 reconciler
创建 report
创建 tests
创建 verify 脚本
使用样例 CSV fixture 测试
```

## 8.2 禁止

```text
不自动猜测缺失交易
不伪造账户净值
不把估算数据标为真实
不连接券商接口
不读取本机隐私文件
不把真实数据提交到 GitHub
不把 raw broker export 提交到 GitHub
```

如需处理真实 5 年数据，必须放在：

```text
data/research_db/account/raw/
```

并确认 `.gitignore` 屏蔽：

```text
data/research_db/account/raw/
data/research_db/account/staging/
*.xlsx
*.xls
*.csv.raw
```

---

# 九、必须新增 .gitignore 规则

如果尚未存在，必须加入：

```gitignore
# ResearchDB raw/private account data
data/research_db/account/raw/
data/research_db/account/staging/
data/research_db/account/reports/private/
*.csv.raw
*.xlsx
*.xls

# Runtime reports
runtime_reports/
```

注意：

```text
normalized 样例数据可以提交；
真实账户 raw 数据不得提交。
```

---

# 十、代码模块设计

## 10.1 raw_import_schema.py

定义原始导入 schema。

```python
REQUIRED_TRADE_FIELDS = [
    "trade_date",
    "ticker",
    "side",
    "price",
    "quantity",
]

REQUIRED_ACCOUNT_FIELDS = [
    "date",
    "total_equity",
]
```

提供：

```python
def validate_required_fields(row: dict, required_fields: list[str]) -> dict:
    ...
```

返回：

```json
{
  "status": "READY",
  "missing_fields": []
}
```

---

## 10.2 trade_normalizer.py

提供：

```python
def normalize_trade_rows(rows: list[dict], source_file: str, account_id: str) -> list[dict]:
    ...
```

必须生成：

```text
trade_id
amount
total_cost
net_amount
quality_status
```

---

## 10.3 position_normalizer.py

提供：

```python
def normalize_position_rows(rows: list[dict], source_file: str, account_id: str) -> list[dict]:
    ...
```

---

## 10.4 cashflow_normalizer.py

提供：

```python
def normalize_cashflow_rows(rows: list[dict], source_file: str, account_id: str) -> list[dict]:
    ...
```

---

## 10.5 account_snapshot_normalizer.py

提供：

```python
def normalize_account_snapshot_rows(rows: list[dict], source_file: str, account_id: str) -> list[dict]:
    ...
```

---

## 10.6 account_reconciler.py

提供：

```python
def reconcile_account_snapshot(snapshot_rows: list[dict], position_rows: list[dict]) -> dict:
    ...

def reconcile_trade_amounts(trade_rows: list[dict]) -> dict:
    ...

def reconcile_sell_quantity(trade_rows: list[dict]) -> dict:
    ...
```

---

## 10.7 capital_curve_builder.py

提供：

```python
def build_capital_curve(account_snapshots: list[dict], cashflows: list[dict]) -> list[dict]:
    ...
```

必须扣除入金/出金影响。

---

## 10.8 holding_pnl_builder.py

提供：

```python
def build_holding_pnl(trade_rows: list[dict], price_rows: list[dict] | None = None, cost_method: str = "FIFO") -> list[dict]:
    ...
```

---

## 10.9 drawdown_calculator.py

提供：

```python
def calculate_drawdown(capital_curve: list[dict]) -> list[dict]:
    ...
```

---

## 10.10 missing_data_detector.py

提供：

```python
def detect_missing_data(*datasets) -> dict:
    ...
```

必须输出：

```text
missing_account_days
missing_trade_fields
missing_position_days
missing_price_days
```

---

## 10.11 account_truth_report.py

提供：

```python
def generate_account_truth_report(summary: dict, output_path: str) -> dict:
    ...
```

输出：

```text
account_truth_report.md
```

---

# 十一、测试要求

## 11.1 测试目录

```text
tests/research_db/account_truth/
  test_raw_import_schema.py
  test_trade_normalizer.py
  test_position_normalizer.py
  test_cashflow_normalizer.py
  test_account_snapshot_normalizer.py
  test_account_reconciler.py
  test_capital_curve_builder.py
  test_holding_pnl_builder.py
  test_drawdown_calculator.py
  test_missing_data_detector.py
  test_no_private_raw_data_tracked.py
```

---

## 11.2 必须测试的场景

### trade_normalizer

```text
BUY 行生成 amount
SELL 行生成 amount
fee/stamp/slippage 汇总 total_cost
缺 ticker → ERROR
trade_id 唯一
```

### account_snapshot_normalizer

```text
total_equity 存在 → READY
total_equity 缺失 → ERROR
daily_return 可计算
date 重复 → ERROR
```

### account_reconciler

```text
cash + market_value = total_equity
price * quantity = market_value
sell quantity 不得超过可用持仓
```

### capital_curve_builder

```text
入金不计入投资收益
出金不计入投资亏损
daily_return 正确
max_drawdown 正确
```

### holding_pnl_builder

```text
单次买入卖出
分批买入
分批卖出
未关闭持仓
FIFO 成本法
```

### missing_data_detector

```text
缺交易日
缺价格
缺持仓
缺账户权益
```

### no_private_raw_data_tracked

```text
git ls-files 不得包含 data/research_db/account/raw/
git ls-files 不得包含 .xlsx/.xls
```

---

# 十二、verify 脚本

新增：

```text
scripts/verify_research_db_phase1_account_truth.sh
```

内容必须执行：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 1 Account Truth Verification ═══"

python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/account_truth/

python3 - <<'PY'
from pathlib import Path
import subprocess

required_modules = [
    "zmatrix/research_db/account_truth/raw_import_schema.py",
    "zmatrix/research_db/account_truth/trade_normalizer.py",
    "zmatrix/research_db/account_truth/position_normalizer.py",
    "zmatrix/research_db/account_truth/cashflow_normalizer.py",
    "zmatrix/research_db/account_truth/account_snapshot_normalizer.py",
    "zmatrix/research_db/account_truth/account_reconciler.py",
    "zmatrix/research_db/account_truth/capital_curve_builder.py",
    "zmatrix/research_db/account_truth/holding_pnl_builder.py",
    "zmatrix/research_db/account_truth/drawdown_calculator.py",
    "zmatrix/research_db/account_truth/missing_data_detector.py",
    "zmatrix/research_db/account_truth/account_truth_report.py",
]

for p in required_modules:
    assert Path(p).exists(), f"Missing module: {p}"

required_dirs = [
    "data/research_db/account/raw",
    "data/research_db/account/normalized",
    "data/research_db/account/staging",
    "data/research_db/account/reports",
    "data/research_db/signal",
    "data/research_db/watchlist",
]

for p in required_dirs:
    assert Path(p).exists(), f"Missing dir: {p}"

tracked = subprocess.check_output(["git", "ls-files"], text=True)
for forbidden in [
    "data/research_db/account/raw/",
    "data/research_db/account/staging/",
]:
    assert forbidden not in tracked, f"Private raw/staging data tracked: {forbidden}"

for ext in [".xlsx", ".xls", ".csv.raw"]:
    assert ext not in tracked, f"Private raw file tracked: {ext}"

for p in Path("zmatrix/research_db/account_truth").rglob("*.py"):
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

print("✅ ResearchDB Phase 1 Account Truth verification PASS")
PY

echo "═══ ResearchDB Phase 1 PASS ═══"
```

---

# 十三、样例 fixture

允许创建测试 fixture：

```text
tests/fixtures/account_truth/
  sample_trades.csv
  sample_positions.csv
  sample_cashflows.csv
  sample_account_snapshots.csv
```

这些 fixture 必须是虚构数据，不得使用真实账户记录。

---

# 十四、报告要求

## 14.1 import_quality_report.md

必须包含：

```text
导入文件数量
导入行数
READY 行数
PARTIAL 行数
ERROR 行数
缺失字段
重复记录
异常金额
```

## 14.2 reconciliation_report.md

必须包含：

```text
账户权益核对
交易金额核对
持仓市值核对
卖出数量核对
现金流核对
失败行清单
```

## 14.3 account_truth_report.md

必须包含：

```text
数据覆盖时间
账户总收益
最大回撤
年度收益
月度收益
交易次数
胜率
平均收益
最大盈利交易
最大亏损交易
持仓周期分布
数据质量说明
不可用数据清单
```

### 注意

本阶段报告只能是账户真相报告，不得输出：

```text
买入建议
卖出建议
推荐股票
策略晋级
RC1 状态变更
```

---

# 十五、Acceptance Matrix

新增：

```text
docs/research_db/PHASE1_ACCEPTANCE_MATRIX.md
```

内容：

```markdown
# ResearchDB Phase 1 Acceptance Matrix

| Item | Requirement | Status |
|---|---|---|
| P1-1 | Account raw/staging/normalized directories | DONE |
| P1-2 | Trade ledger schema | DONE |
| P1-3 | Position ledger schema | DONE |
| P1-4 | Cashflow ledger schema | DONE |
| P1-5 | Account daily snapshot schema | DONE |
| P1-6 | Capital curve builder | DONE |
| P1-7 | Holding PnL builder | DONE |
| P1-8 | Drawdown calculator | DONE |
| P1-9 | Reconciliation logic | DONE |
| P1-10 | Missing data detector | DONE |
| P1-11 | Account truth report | DONE |
| P1-12 | Tests | DONE |
| P1-13 | Verify script | DONE |
| P1-14 | Private raw data not tracked | DONE |

Final Status: PHASE1_READY_FOR_REAL_DATA_IMPORT  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  
```

---

# 十六、Closeout Report

新增：

```text
docs/research_db/PHASE1_CLOSEOUT_REPORT.md
```

内容必须包含：

```markdown
# ResearchDB Phase 1 Closeout Report

## Final Status

ResearchDB Phase 1: PASS  
Next Phase: Phase 2 Universe & Industry Mapping  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  

## Completed

- Account raw/staging/normalized directory
- Trade ledger schema
- Position ledger schema
- Cashflow ledger schema
- Account daily snapshot schema
- Capital curve builder
- Holding PnL builder
- Drawdown calculator
- Reconciliation logic
- Missing data detector
- Account truth report generator
- Tests
- Verify script

## Hard Boundaries

- No real trade
- No broker
- No runtime
- No production
- No automatic rule promotion
- No private raw data tracked

## Data Import Status

Real account data imported: FALSE / TRUE  
If TRUE, raw private data tracked by git: FALSE  
If FALSE, system ready for private local import.

## Next Step

Proceed to Phase 2: Universe & Industry Mapping.

Phase 2 may create:
- security_master.csv
- industry_classification.csv
- chain_mapping.csv
- theme_mapping.csv
- benchmark_mapping.csv

Phase 2 must not:
- generate trade signal
- enable production
- modify RC1 status
```

---

# 十七、执行批次

## Batch P1-A：目录与 schema

```text
创建 account_truth 目录
创建 raw/staging/normalized/reports 目录
创建 csv schema 文档与 README
```

Commit：

```bash
git add .
git commit -m "researchdb-phase1-a: add account truth directories and schemas"
```

## Batch P1-B：normalizer 模块

```text
实现 trade / position / cashflow / account snapshot normalizer
```

Commit：

```bash
git add .
git commit -m "researchdb-phase1-b: implement account truth normalizers"
```

## Batch P1-C：reconciliation + curve

```text
实现 account_reconciler / capital_curve_builder / holding_pnl_builder / drawdown_calculator
```

Commit：

```bash
git add .
git commit -m "researchdb-phase1-c: implement reconciliation and capital curve builders"
```

## Batch P1-D：report + tests + verify

```text
实现 account_truth_report
创建 tests/research_db/account_truth/
创建 verify_research_db_phase1_account_truth.sh
```

Commit：

```bash
git add .
git commit -m "researchdb-phase1-d: add account truth tests and verification"
```

## Batch P1-E：closeout

```text
更新 PHASE1_ACCEPTANCE_MATRIX.md
更新 PHASE1_CLOSEOUT_REPORT.md
跑 verify
```

Commit：

```bash
git add .
git commit -m "researchdb-phase1-e: close phase1 account truth import foundation"
```

---

# 十八、运行命令

OpenClaw 必须执行：

```bash
python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/account_truth/

bash scripts/verify_research_db_phase1_account_truth.sh
```

建议同时复跑 Phase 0：

```bash
bash scripts/verify_research_db_phase0.sh
```

如果任何一条失败：

```text
不得提交 closeout。
不得进入 Phase 2。
```

---

# 十九、完成报告格式

OpenClaw 完成后必须输出：

```text
## ResearchDB Phase 1 完成报告

commit:
branch:

### Directories
- raw:
- staging:
- normalized:
- reports:
- signal:
- watchlist:

### Schemas
- account_daily_snapshot:
- trade_ledger:
- position_ledger:
- cashflow_ledger:
- capital_curve:
- holding_pnl_ledger:
- drawdown_ledger:
- manual_decision_ledger:
- watchlist_ledger:

### Code
- raw_import_schema:
- trade_normalizer:
- position_normalizer:
- cashflow_normalizer:
- account_snapshot_normalizer:
- account_reconciler:
- capital_curve_builder:
- holding_pnl_builder:
- drawdown_calculator:
- missing_data_detector:
- account_truth_report:

### Tests
- tests/research_db/account_truth:
- verify_research_db_phase1_account_truth.sh:
- verify_research_db_phase0.sh:

### Data Safety
- raw broker data tracked:
- staging data tracked:
- xlsx/xls tracked:
- private account data committed:

### Final Status
ResearchDB Phase 1: PASS / FAIL
Next Phase: Phase 2 Universe & Industry Mapping
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 二十、通过标准

Phase 1 只有在以下全部满足时通过：

```text
1. account_truth 模块存在。
2. raw/staging/normalized/reports 目录存在。
3. 账户、交易、持仓、现金流、资金曲线 schema 明确。
4. normalizer 可运行。
5. reconciler 可运行。
6. capital_curve_builder 可运行。
7. holding_pnl_builder 可运行。
8. drawdown_calculator 可运行。
9. missing_data_detector 可运行。
10. account_truth_report 可生成。
11. tests/research_db/account_truth/ 全部通过。
12. verify_research_db_phase1_account_truth.sh 通过。
13. 真实 raw 私有数据未被 git 跟踪。
14. production/broker/runtime/real_trade 全部 BLOCKED。
15. Closeout Report 允许进入 Phase 2。
```

---

# 二十一、阶段结束后的状态

Phase 1 完成后，系统状态应为：

```text
ResearchDB Phase 1: PASS
ResearchDB Status: READY_FOR_REAL_ACCOUNT_DATA_IMPORT
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
RC1 status: unchanged
```

Phase 1 完成后，并不意味着已完成真实 5 年数据导入。  
它意味着：

```text
系统已经具备安全导入、清洗、校验、重建 5 年实盘账户真相的工程能力。
```

真正导入你的私有数据时，必须本地执行，不得把原始券商数据提交云仓。

---

# 二十二、真实数据导入建议

当 Phase 1 工程完成后，真实导入建议分三步：

## Step 1：本地私有导入

```text
把券商导出的原始文件放入：
data/research_db/account/raw/broker_exports/
```

确认：

```bash
git status --short
```

不得出现原始文件。

## Step 2：生成 normalized 数据

运行未来导入脚本：

```bash
scripts/researchdb_import_account_truth.sh
```

生成：

```text
normalized/account_daily_snapshot.csv
normalized/trade_ledger.csv
normalized/position_ledger.csv
normalized/cashflow_ledger.csv
```

## Step 3：生成真相报告

输出：

```text
data/research_db/account/reports/account_truth_report.md
```

这个报告可以作为 Phase 2 / Phase 3 / Phase 5 的输入。

---

# 二十三、最终裁决

Phase 1 的本质是：

```text
把过去 5 年真实账户经历，从“流水记录”升级成“可研究、可归因、可复盘、可内化”的账户真相库。
```

没有 Phase 1，所有行业研究和因子验证都缺少最终裁判。  
完成 Phase 1 后，Z-MATRIX-OS 才真正拥有个人研究数据库的第一块基石：

```text
我的实盘真相。
```

下一阶段：

```text
Phase 2：标的主数据 + 行业/产业链映射库
```


---

# Phase 1 A+ 额外加固项

## P1-A+ 私有数据隔离强制策略

必须新增：

```text
docs/research_db/PHASE1_PRIVATE_DATA_POLICY.md
scripts/verify_research_db_phase1_private_data_guard.sh
```

强制规则：

```text
1. data/research_db/account/raw/ 不得被 git track。
2. data/research_db/account/staging/ 不得被 git track。
3. 真实券商文件不得提交。
4. normalized 可提交的只能是 schema 样例或脱敏样例。
5. 若导入真实数据，只能本地执行，不得推送云仓。
```

## P1-A+ Reconciliation Error Contract

所有 reconciliation 函数失败时必须返回：

```json
{
  "status": "FAILED",
  "error_type": "RECONCILIATION_FAILED",
  "failed_rows": [],
  "blocking": true
}
```

不得静默跳过。


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
