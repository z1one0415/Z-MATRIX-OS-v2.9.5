# Phase 2：标的主数据 + 行业/产业链映射库｜A+加固执行版

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

# Phase 2：标的主数据 + 行业/产业链映射库

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 2  
> **阶段名称**：Universe & Industry/Chain Mapping｜标的主数据 + 行业/产业链映射库  
> **前置阶段**：Phase 0：ResearchDB 宪法与目录冻结；Phase 1：5年实盘真相库  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：标的主数据治理 / 行业分类 / 产业链映射 / 主题映射 / 同类股与基准映射  
> **阶段目标**：建立所有历史交易标的、当前持仓、候选池、观察池、研究池的统一主数据，并完成行业、主题、产业链位置、同类股、benchmark 映射，为后续 Outcome 验证、FactorFactory、CaseForge、B-Matrix、ZC35、行业知识库提供统一归因底座。  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 2 不是“写 31 个行业深研”，也不是“做选股策略”。

Phase 2 的唯一目标是：

```text
让系统知道每一只股票属于什么行业、什么主题、什么产业链、处在什么价值环节、应该跟谁比较、应该用哪个基准评价。
```

如果没有 Phase 2，后续系统无法正确回答：

```text
1. 某笔交易到底跑赢了行业，还是只是跟着板块涨？
2. 某个标的是产业链核心瓶颈，还是边缘概念？
3. 某次亏损是行业 beta 问题，还是个股 alpha 问题？
4. 某个信号在同行中是否有横截面优势？
5. CaseForge 归因应该归到哪个产业链环节？
```

本阶段只允许做：

```text
1. 创建标的主数据 security_master
2. 创建行业分类 industry_classification
3. 创建产业链映射 chain_mapping
4. 创建主题映射 theme_mapping
5. 创建同类股 peer_group_mapping
6. 创建基准 benchmark_mapping
7. 创建股票角色 stock_role_mapping
8. 创建映射质量与证据等级规则
9. 创建导入、校验、冲突检测、报告模块
10. 输出 Universe Mapping Report
```

本阶段禁止：

```text
1. 不生成交易建议
2. 不接 broker
3. 不开启 runtime
4. 不进入 production
5. 不改 RC1 状态
6. 不写 31 行业长篇研究
7. 不把概念标签直接当产业链位置
8. 不用单一来源无证据映射高置信结论
9. 不自动晋级任何产业链规则
```

---

# 一、Phase 2 的核心价值

Phase 1 解决的是：

```text
我过去买了什么、赚了多少、亏了多少。
```

Phase 2 解决的是：

```text
我买的这些股票，到底属于什么行业、什么产业链、什么主题，应该跟谁比较。
```

Phase 2 完成后，系统必须能回答：

```text
1. 002472 双环传动属于哪个行业、哪个机器人产业链环节？
2. 锦浪科技应该跟哪些逆变器公司比较？
3. 某笔交易跑输行业，是行业整体弱，还是个股弱？
4. 某个概念股是否真的处于产业链价值捕获环节？
5. 某条主线有哪些代表股票、核心股票、高 beta 股票、防御股票？
6. 某个 CaseForge 案例应该归入哪个行业/产业链/主题？
```

---

# 二、Phase 2 的输入边界

## 2.1 输入来源

允许输入：

```text
Phase 1 的 trade_ledger.csv
Phase 1 的 position_ledger.csv
Phase 1 的 watchlist_ledger.csv
Phase 1 的 candidate_ledger.csv
Phase 1 的 research_universe_ledger.csv
人工维护的股票池
人工维护的产业链表
公开行业分类数据
公开指数/ETF信息
公司公开主营业务信息
系统已有 stock_profiles
```

## 2.2 数据状态

每条映射必须有：

```text
mapping_status
evidence_grade
data_status
updated_at
review_required
```

## 2.3 默认规则

```text
1. 历史交易过的股票必须优先映射。
2. 当前持仓必须优先映射。
3. 当前观察池/候选池必须优先映射。
4. 高频研究股票必须有产业链位置。
5. 全市场股票可后续分批补，不作为 Phase 2 完成前置条件。
```

---

# 三、必须创建的数据目录

Phase 2 必须基于 Phase 0 的 `data/research_db/universe/` 扩展。

```text
data/research_db/universe/
  README.md

  raw/
    README.md
    manual_imports/
      .gitkeep
    external_exports/
      .gitkeep

  staging/
    imported_security_master_raw.csv
    imported_industry_classification_raw.csv
    imported_chain_mapping_raw.csv
    imported_theme_mapping_raw.csv
    import_error_rows.csv

  normalized/
    security_master.csv
    industry_classification.csv
    chain_mapping.csv
    theme_mapping.csv
    peer_group_mapping.csv
    benchmark_mapping.csv
    stock_role_mapping.csv
    mapping_quality_ledger.csv

  reports/
    universe_mapping_report.md
    chain_mapping_report.md
    benchmark_mapping_report.md
    mapping_conflict_report.md
    missing_mapping_report.md

data/research_db/knowledge/
  industries/
    README.md
    industry_card_template.md
  chains/
    README.md
    chain_card_template.md
```

真实外部导入数据如含版权或私有数据，不得提交。

---

# 四、必须创建的代码模块

```text
zmatrix/research_db/universe/
  __init__.py
  security_master_schema.py
  industry_schema.py
  chain_schema.py
  theme_schema.py
  peer_group_schema.py
  benchmark_schema.py
  stock_role_schema.py
  universe_loader.py
  universe_normalizer.py
  mapping_validator.py
  mapping_conflict_detector.py
  chain_position_classifier.py
  benchmark_resolver.py
  peer_group_builder.py
  mapping_quality_scorer.py
  universe_mapping_report.py
```

---

# 五、核心数据表规范

## 5.1 security_master.csv

### 字段

```csv
ticker,name,exchange,list_date,listing_status,market_type,security_type,currency,company_short_name,company_full_name,source,data_status,updated_at,quality_status
```

### exchange 枚举

```text
SSE
SZSE
BSE
HKEX
NASDAQ
NYSE
UNKNOWN
```

### listing_status 枚举

```text
LISTED
DELISTED
SUSPENDED
UNKNOWN
```

### security_type 枚举

```text
A_SHARE
ETF
INDEX
HK_STOCK
US_STOCK
FUND
BOND
OTHER
```

### 硬规则

```text
ticker 不得为空。
name 不得为空。
ticker + exchange 必须唯一。
quality_status=ERROR 的标的不得进入后续映射。
```

---

## 5.2 industry_classification.csv

### 字段

```csv
ticker,name,classification_system,industry_l1,industry_l2,industry_l3,industry_l4,source,as_of_date,data_status,updated_at,quality_status
```

### classification_system 枚举

```text
SW
CSRC
CITIC
GICS
MANUAL
UNKNOWN
```

### 硬规则

```text
历史交易标的必须至少有 industry_l1。
当前持仓和观察池标的必须至少有 industry_l2。
行业分类 source 必须记录。
manual 分类必须 review_required=true。
```

---

## 5.3 chain_mapping.csv

### 字段

```csv
ticker,name,chain_id,chain_name,chain_layer,chain_position,value_capture_grade,business_relevance,financial_validation,evidence_grade,source,as_of_date,updated_at,review_required,quality_status
```

### chain_layer 枚举

```text
UPSTREAM_RESOURCE
CORE_COMPONENT
HARDWARE_BOTTLENECK
SYSTEM_INTEGRATOR
DELIVERY_PLATFORM
APPLICATION_ADAPTER
CHANNEL_DISTRIBUTION
SERVICE_PROVIDER
FINANCIAL_BETA
DEFENSIVE_ANCHOR
UNKNOWN
```

### chain_position 示例

```text
机器人链：
  precision_reducer
  harmonic_reducer
  planetary_reducer
  screw
  motor
  sensor
  controller
  ontology
  integrator
  application

AI算力链：
  gpu
  asic
  server
  optical_module
  liquid_cooling
  power_supply
  idc
  application

储能逆变器链：
  inverter
  pcs
  battery_cell
  bms
  ems
  system_integration
  overseas_channel
```

### value_capture_grade

```text
A：核心瓶颈，利润弹性强，财务可验证
B：产业位置重要，财务验证中等
C：有主题映射，但利润传导弱
D：纯概念或证据不足
UNKNOWN：无法判断
```

### business_relevance

```text
HIGH
MEDIUM
LOW
UNKNOWN
```

### financial_validation

```text
VALIDATED
PARTIAL
UNVERIFIED
CONTRADICTED
UNKNOWN
```

### evidence_grade

```text
A：公告/财报/订单/客户/收入结构强证据
B：公开资料与主营业务匹配
C：概念标签或研报提及，但缺财务验证
D：弱关联或市场传闻
```

### 硬规则

```text
不能只因为概念标签就赋予 A/B value_capture_grade。
evidence_grade=C/D 的映射必须 review_required=true。
financial_validation=UNVERIFIED 的映射不得用于高置信结论。
```

---

## 5.4 theme_mapping.csv

### 字段

```csv
ticker,name,theme_id,theme_name,theme_type,theme_strength,theme_source,theme_start_date,theme_end_date,active_status,evidence_grade,updated_at,quality_status
```

### theme_type 枚举

```text
POLICY_THEME
TECH_THEME
RESOURCE_THEME
CYCLE_THEME
DEFENSIVE_THEME
EVENT_THEME
NARRATIVE_THEME
UNKNOWN
```

### theme_strength

```text
CORE
SECONDARY
MARGINAL
NOISE
UNKNOWN
```

### active_status

```text
ACTIVE
DECAYING
EXHAUSTED
INACTIVE
UNKNOWN
```

### 硬规则

```text
主题映射不得替代产业链映射。
theme_strength=CORE 必须有证据。
NARRATIVE_THEME 默认 review_required=true。
```

---

## 5.5 peer_group_mapping.csv

### 字段

```csv
peer_group_id,peer_group_name,ticker,name,peer_role,comparison_priority,source,updated_at,quality_status
```

### peer_role 枚举

```text
LEADER
CORE_PEER
HIGH_BETA_PEER
DEFENSIVE_PEER
UPSTREAM_PEER
DOWNSTREAM_PEER
SUBSTITUTE
BENCHMARK_ONLY
UNKNOWN
```

### comparison_priority

```text
P1_DIRECT
P2_CLOSE
P3_REFERENCE
P4_WEAK
```

### 作用

用于：

```text
同行对比
行业 alpha
估值横截面
因子 RankIC
CaseForge 归因
```

---

## 5.6 benchmark_mapping.csv

### 字段

```csv
ticker,name,benchmark_type,benchmark_id,benchmark_name,benchmark_role,priority,source,updated_at,quality_status
```

### benchmark_type

```text
MARKET_INDEX
INDUSTRY_INDEX
THEME_BASKET
PEER_BASKET
ETF
CUSTOM_BASKET
UNKNOWN
```

### benchmark_role

```text
PRIMARY
SECONDARY
REFERENCE
HEDGE_PROXY
UNKNOWN
```

### 硬规则

```text
每个历史交易标的必须至少有一个 PRIMARY benchmark。
每个当前持仓必须有 MARKET_INDEX + INDUSTRY_INDEX。
核心研究标的必须有 THEME_BASKET 或 PEER_BASKET。
```

---

## 5.7 stock_role_mapping.csv

### 字段

```csv
ticker,name,role_type,role_scope,role_reason,confidence,source,updated_at,quality_status
```

### role_type 枚举

```text
LONG_TERM_CORE
MID_TERM_ROTATION
SHORT_TERM_EVENT
HIGH_BETA
DEFENSIVE_ANCHOR
WATCH_ONLY
CASE_STUDY
DO_NOT_TOUCH
UNKNOWN
```

### 作用

辅助 ZC50 与 CaseForge 判断：

```text
这是底仓候选？
这是周期轮动？
这是短线事件？
这是只观察不交易？
这是历史错误案例？
```

---

## 5.8 mapping_quality_ledger.csv

### 字段

```csv
mapping_id,ticker,mapping_type,quality_status,evidence_grade,review_required,conflict_status,missing_fields,updated_at,notes
```

### conflict_status

```text
NO_CONFLICT
CONFLICTED_INDUSTRY
CONFLICTED_CHAIN
CONFLICTED_THEME
CONFLICTED_BENCHMARK
DATA_INSUFFICIENT
```

---

# 六、核心处理流程

Phase 2 的处理流程必须固定为：

```text
Universe Source Import
→ Security Master Normalize
→ Industry Classification Normalize
→ Chain Mapping Normalize
→ Theme Mapping Normalize
→ Peer Group Build
→ Benchmark Resolve
→ Mapping Quality Score
→ Conflict Detection
→ Mapping Reports
→ Closeout
```

---

## 6.1 Universe Source Import

输入：

```text
Phase 1 trade_ledger
Phase 1 position_ledger
Phase 1 watchlist_ledger
Phase 1 candidate_ledger
manual stock list
manual chain mapping
external industry classification
```

输出：

```text
staging/imported_*_raw.csv
```

---

## 6.2 Security Master Normalize

必须统一：

```text
ticker 格式
exchange
name
listing_status
security_type
```

示例：

```text
300763 → 300763.SZ
002472 → 002472.SZ
600519 → 600519.SH
```

---

## 6.3 Industry Classification Normalize

必须把不同来源行业分类统一为：

```text
industry_l1
industry_l2
industry_l3
industry_l4
classification_system
```

---

## 6.4 Chain Mapping Normalize

必须区分：

```text
概念标签
产业链位置
价值捕获等级
财务验证
```

禁止：

```text
把“机器人概念”直接等同于“机器人核心瓶颈”
```

---

## 6.5 Theme Mapping Normalize

必须记录：

```text
主题是否活跃
主题是否衰减
主题证据等级
主题来源
```

---

## 6.6 Peer Group Build

peer group 生成必须基于：

```text
同细分行业
同产业链位置
同商业模式
同财务结构
同交易属性
```

不能只基于概念标签。

---

## 6.7 Benchmark Resolve

benchmark resolver 必须为每个核心标的绑定：

```text
market benchmark
industry benchmark
theme benchmark / peer basket
```

---

## 6.8 Conflict Detection

必须检测：

```text
同一 ticker 多个行业冲突
产业链位置冲突
主题强度冲突
benchmark 缺失
peer group 空缺
```

冲突输出到：

```text
mapping_conflict_report.md
```

---

# 七、代码模块设计

## 7.1 security_master_schema.py

必须定义：

```python
SECURITY_MASTER_REQUIRED_FIELDS = [
    "ticker",
    "name",
    "exchange",
    "listing_status",
    "security_type",
]
```

提供：

```python
def normalize_ticker(ticker: str, exchange: str | None = None) -> str:
    ...

def validate_security_master_row(row: dict) -> dict:
    ...
```

---

## 7.2 industry_schema.py

必须定义：

```python
INDUSTRY_CLASSIFICATION_SYSTEMS = [
    "SW",
    "CSRC",
    "CITIC",
    "GICS",
    "MANUAL",
    "UNKNOWN",
]
```

提供：

```python
def validate_industry_row(row: dict) -> dict:
    ...
```

---

## 7.3 chain_schema.py

必须定义：

```python
CHAIN_LAYERS = [
    "UPSTREAM_RESOURCE",
    "CORE_COMPONENT",
    "HARDWARE_BOTTLENECK",
    "SYSTEM_INTEGRATOR",
    "DELIVERY_PLATFORM",
    "APPLICATION_ADAPTER",
    "CHANNEL_DISTRIBUTION",
    "SERVICE_PROVIDER",
    "FINANCIAL_BETA",
    "DEFENSIVE_ANCHOR",
    "UNKNOWN",
]
```

提供：

```python
def validate_chain_mapping_row(row: dict) -> dict:
    ...
```

---

## 7.4 benchmark_resolver.py

提供：

```python
def resolve_primary_benchmark(ticker: str, industry_row: dict, theme_rows: list[dict] | None = None) -> dict:
    ...
```

返回：

```json
{
  "ticker": "002472.SZ",
  "benchmark_type": "INDUSTRY_INDEX",
  "benchmark_id": "SW_AUTO_PARTS",
  "benchmark_role": "PRIMARY",
  "quality_status": "READY"
}
```

---

## 7.5 chain_position_classifier.py

提供：

```python
def classify_chain_position(row: dict) -> dict:
    ...
```

规则：

```text
如果只有 theme_name，没有 business evidence → UNKNOWN / review_required
如果 chain_position 存在但 evidence_grade C/D → review_required
如果 financial_validation=VALIDATED 且 evidence_grade A/B → READY
```

---

## 7.6 peer_group_builder.py

提供：

```python
def build_peer_group(ticker: str, universe_rows: list[dict], chain_rows: list[dict]) -> list[dict]:
    ...
```

---

## 7.7 mapping_quality_scorer.py

提供：

```python
def score_mapping_quality(row: dict) -> dict:
    ...
```

输出：

```json
{
  "quality_score": 0.85,
  "quality_status": "READY",
  "review_required": false,
  "blocked_reason": null
}
```

### 质量状态

```text
READY
PARTIAL
REVIEW_REQUIRED
DATA_INSUFFICIENT
CONFLICTED
ERROR
```

---

## 7.8 mapping_conflict_detector.py

提供：

```python
def detect_mapping_conflicts(rows: list[dict]) -> dict:
    ...
```

必须输出：

```text
industry_conflicts
chain_conflicts
theme_conflicts
benchmark_missing
peer_group_missing
```

---

## 7.9 universe_mapping_report.py

提供：

```python
def generate_universe_mapping_report(summary: dict, output_path: str) -> dict:
    ...
```

报告必须输出：

```text
总标的数
历史交易标的映射完成率
当前持仓映射完成率
观察池映射完成率
缺失行业数
缺失 benchmark 数
冲突映射数
需要人工复核数
```

---

# 八、测试要求

## 8.1 测试目录

```text
tests/research_db/universe/
  test_security_master_schema.py
  test_industry_schema.py
  test_chain_schema.py
  test_theme_schema.py
  test_benchmark_resolver.py
  test_peer_group_builder.py
  test_chain_position_classifier.py
  test_mapping_quality_scorer.py
  test_mapping_conflict_detector.py
  test_universe_mapping_report.py
  test_no_production_boundary.py
```

---

## 8.2 必须测试的场景

### security_master

```text
ticker 标准化
ticker + exchange 唯一
缺 ticker → ERROR
缺 name → ERROR
```

### industry_schema

```text
classification_system 合法
历史交易标的至少有 industry_l1
当前持仓至少有 industry_l2
manual 分类需要 review_required
```

### chain_schema

```text
chain_layer 合法
value_capture_grade 合法
只有概念无证据 → review_required
financial_validation=UNVERIFIED 不得 READY
```

### theme_schema

```text
theme_strength 合法
NARRATIVE_THEME 默认 review_required
EXHAUSTED theme 不得作为 active core
```

### benchmark_resolver

```text
历史交易标的必须生成 PRIMARY benchmark
当前持仓必须生成 MARKET + INDUSTRY benchmark
缺行业 → DATA_INSUFFICIENT
```

### peer_group_builder

```text
同 chain_position 生成 direct peer
只有同 theme 不得直接 P1_DIRECT
```

### mapping_conflict_detector

```text
同 ticker 多个 l1 冲突
同 ticker 多个 chain_position 冲突
benchmark 缺失
```

### no_production_boundary

```text
所有输出 production_allowed=false
real_trade_allowed=false
broker_order_allowed=false
runtime_enabled=false
```

---

# 九、verify 脚本

新增：

```text
scripts/verify_research_db_phase2_universe_mapping.sh
```

内容必须执行：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 2 Universe Mapping Verification ═══"

python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/universe/

python3 - <<'PY'
from pathlib import Path

required_modules = [
    "zmatrix/research_db/universe/security_master_schema.py",
    "zmatrix/research_db/universe/industry_schema.py",
    "zmatrix/research_db/universe/chain_schema.py",
    "zmatrix/research_db/universe/theme_schema.py",
    "zmatrix/research_db/universe/peer_group_schema.py",
    "zmatrix/research_db/universe/benchmark_schema.py",
    "zmatrix/research_db/universe/stock_role_schema.py",
    "zmatrix/research_db/universe/universe_loader.py",
    "zmatrix/research_db/universe/universe_normalizer.py",
    "zmatrix/research_db/universe/mapping_validator.py",
    "zmatrix/research_db/universe/mapping_conflict_detector.py",
    "zmatrix/research_db/universe/chain_position_classifier.py",
    "zmatrix/research_db/universe/benchmark_resolver.py",
    "zmatrix/research_db/universe/peer_group_builder.py",
    "zmatrix/research_db/universe/mapping_quality_scorer.py",
    "zmatrix/research_db/universe/universe_mapping_report.py",
]

for p in required_modules:
    assert Path(p).exists(), f"Missing module: {p}"

required_files = [
    "data/research_db/universe/normalized/security_master.csv",
    "data/research_db/universe/normalized/industry_classification.csv",
    "data/research_db/universe/normalized/chain_mapping.csv",
    "data/research_db/universe/normalized/theme_mapping.csv",
    "data/research_db/universe/normalized/peer_group_mapping.csv",
    "data/research_db/universe/normalized/benchmark_mapping.csv",
    "data/research_db/universe/normalized/stock_role_mapping.csv",
    "data/research_db/universe/normalized/mapping_quality_ledger.csv",
]

for p in required_files:
    assert Path(p).exists(), f"Missing normalized file: {p}"

for p in Path("zmatrix/research_db/universe").rglob("*.py"):
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

print("✅ ResearchDB Phase 2 Universe Mapping verification PASS")
PY

echo "═══ ResearchDB Phase 2 PASS ═══"
```

---

# 十、样例 fixture

允许创建测试 fixture：

```text
tests/fixtures/universe/
  sample_security_master.csv
  sample_industry_classification.csv
  sample_chain_mapping.csv
  sample_theme_mapping.csv
  sample_benchmark_mapping.csv
```

这些 fixture 必须是虚构或极少量公开示例数据，不得包含付费版权全量数据。

---

# 十一、报告要求

## 11.1 universe_mapping_report.md

必须包含：

```text
标的总数
历史交易标的数
当前持仓标的数
观察池标的数
行业映射完成率
产业链映射完成率
benchmark 映射完成率
peer group 映射完成率
review_required 数量
conflict 数量
```

## 11.2 chain_mapping_report.md

必须包含：

```text
chain_id
chain_name
覆盖股票数量
A/B/C/D value_capture 分布
financial_validation 分布
evidence_grade 分布
review_required 清单
```

## 11.3 benchmark_mapping_report.md

必须包含：

```text
缺失 benchmark 股票
只有 market benchmark 的股票
有 industry benchmark 的股票
有 theme/peer benchmark 的股票
```

## 11.4 mapping_conflict_report.md

必须包含：

```text
行业冲突
产业链冲突
主题冲突
benchmark 缺失
peer group 缺失
需要人工处理清单
```

## 11.5 missing_mapping_report.md

必须包含：

```text
缺 security master
缺 industry
缺 chain
缺 theme
缺 peer group
缺 benchmark
```

---

# 十二、Acceptance Matrix

新增：

```text
docs/research_db/PHASE2_ACCEPTANCE_MATRIX.md
```

内容：

```markdown
# ResearchDB Phase 2 Acceptance Matrix

| Item | Requirement | Status |
|---|---|---|
| P2-1 | Security master schema | DONE |
| P2-2 | Industry classification schema | DONE |
| P2-3 | Chain mapping schema | DONE |
| P2-4 | Theme mapping schema | DONE |
| P2-5 | Peer group mapping schema | DONE |
| P2-6 | Benchmark mapping schema | DONE |
| P2-7 | Stock role mapping schema | DONE |
| P2-8 | Mapping quality ledger | DONE |
| P2-9 | Conflict detector | DONE |
| P2-10 | Benchmark resolver | DONE |
| P2-11 | Peer group builder | DONE |
| P2-12 | Universe mapping report | DONE |
| P2-13 | Tests | DONE |
| P2-14 | Verify script | DONE |
| P2-15 | No production boundary | DONE |

Final Status: PHASE2_READY_FOR_MARKET_OUTCOME_ENGINE  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  
```

---

# 十三、Closeout Report

新增：

```text
docs/research_db/PHASE2_CLOSEOUT_REPORT.md
```

内容必须包含：

```markdown
# ResearchDB Phase 2 Closeout Report

## Final Status

ResearchDB Phase 2: PASS  
Next Phase: Phase 3 Market & Outcome Engine  
Production: BLOCKED  
Broker/runtime: BLOCKED  
Real trade: BLOCKED  

## Completed

- Security master schema
- Industry classification schema
- Chain mapping schema
- Theme mapping schema
- Peer group mapping schema
- Benchmark mapping schema
- Stock role mapping schema
- Mapping quality ledger
- Conflict detector
- Benchmark resolver
- Peer group builder
- Universe mapping report
- Tests
- Verify script

## Hard Boundaries

- No real trade
- No broker
- No runtime
- No production
- No automatic rule promotion
- No concept-to-chain direct promotion

## Data Import Status

Full universe imported: FALSE / TRUE  
Historical trade universe mapped: FALSE / TRUE  
Current holdings mapped: FALSE / TRUE  
Watchlist mapped: FALSE / TRUE  

## Next Step

Proceed to Phase 3: Market & Outcome Engine.

Phase 3 may create:
- daily_price_5y.parquet
- index_daily.parquet
- industry_benchmark_daily.parquet
- theme_basket_daily.parquet
- signal_outcome_t1_t3_t5_t10_t20_t60.parquet

Phase 3 must not:
- generate trade signal
- enable production
- modify RC1 status
```

---

# 十四、执行批次

## Batch P2-A：目录与 schema

```text
创建 universe raw/staging/normalized/reports 目录
创建 knowledge industries/chains 模板
创建 security/industry/chain/theme/benchmark/peer/role schema
```

Commit：

```bash
git add .
git commit -m "researchdb-phase2-a: add universe mapping directories and schemas"
```

## Batch P2-B：映射逻辑

```text
实现 universe_loader / normalizer / validator / chain classifier / benchmark resolver / peer builder
```

Commit：

```bash
git add .
git commit -m "researchdb-phase2-b: implement universe mapping logic"
```

## Batch P2-C：质量与冲突检测

```text
实现 mapping_quality_scorer / mapping_conflict_detector / mapping reports
```

Commit：

```bash
git add .
git commit -m "researchdb-phase2-c: implement mapping quality and conflict detection"
```

## Batch P2-D：测试与 verify

```text
创建 tests/research_db/universe/
创建 verify_research_db_phase2_universe_mapping.sh
跑全量测试
```

Commit：

```bash
git add .
git commit -m "researchdb-phase2-d: add universe mapping tests and verification"
```

## Batch P2-E：closeout

```text
更新 PHASE2_ACCEPTANCE_MATRIX.md
更新 PHASE2_CLOSEOUT_REPORT.md
跑 verify
```

Commit：

```bash
git add .
git commit -m "researchdb-phase2-e: close phase2 universe mapping foundation"
```

---

# 十五、运行命令

OpenClaw 必须执行：

```bash
python -m compileall zmatrix tests scripts

PYTHONPATH=. python3 -m pytest -q tests/research_db/universe/

bash scripts/verify_research_db_phase2_universe_mapping.sh
```

建议同时复跑 Phase 0 / Phase 1：

```bash
bash scripts/verify_research_db_phase0.sh
bash scripts/verify_research_db_phase1_account_truth.sh
```

如果任何一条失败：

```text
不得提交 closeout。
不得进入 Phase 3。
```

---

# 十六、完成报告格式

OpenClaw 完成后必须输出：

```text
## ResearchDB Phase 2 完成报告

commit:
branch:

### Directories
- universe/raw:
- universe/staging:
- universe/normalized:
- universe/reports:
- knowledge/industries:
- knowledge/chains:

### Schemas
- security_master:
- industry_classification:
- chain_mapping:
- theme_mapping:
- peer_group_mapping:
- benchmark_mapping:
- stock_role_mapping:
- mapping_quality_ledger:

### Code
- security_master_schema:
- industry_schema:
- chain_schema:
- theme_schema:
- peer_group_schema:
- benchmark_schema:
- stock_role_schema:
- universe_loader:
- universe_normalizer:
- mapping_validator:
- mapping_conflict_detector:
- chain_position_classifier:
- benchmark_resolver:
- peer_group_builder:
- mapping_quality_scorer:
- universe_mapping_report:

### Reports
- universe_mapping_report:
- chain_mapping_report:
- benchmark_mapping_report:
- mapping_conflict_report:
- missing_mapping_report:

### Tests
- tests/research_db/universe:
- verify_research_db_phase2_universe_mapping.sh:
- verify_research_db_phase0.sh:
- verify_research_db_phase1_account_truth.sh:

### Data Safety
- external raw data tracked:
- paid/copyright data tracked:
- production flags:

### Final Status
ResearchDB Phase 2: PASS / FAIL
Next Phase: Phase 3 Market & Outcome Engine
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十七、通过标准

Phase 2 只有在以下全部满足时通过：

```text
1. universe 目录存在。
2. normalized 7 张主表存在。
3. 标的主数据 schema 明确。
4. 行业分类 schema 明确。
5. 产业链映射 schema 明确。
6. 主题映射 schema 明确。
7. peer group / benchmark / role schema 明确。
8. chain_position_classifier 可运行。
9. benchmark_resolver 可运行。
10. peer_group_builder 可运行。
11. mapping_quality_scorer 可运行。
12. conflict_detector 可运行。
13. universe_mapping_report 可生成。
14. tests/research_db/universe/ 全部通过。
15. verify_research_db_phase2_universe_mapping.sh 通过。
16. 不存在 production/broker/runtime/real_trade flags。
17. Closeout Report 允许进入 Phase 3。
```

---

# 十八、阶段结束后的状态

Phase 2 完成后，系统状态应为：

```text
ResearchDB Phase 2: PASS
ResearchDB Status: READY_FOR_MARKET_OUTCOME_ENGINE
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
RC1 status: unchanged
```

Phase 2 完成后，并不意味着已经完成全市场产业链研究。  
它意味着：

```text
系统已经具备把历史交易、当前持仓、观察池、候选池映射到行业/主题/产业链/基准/同类股的工程能力。
```

---

# 十九、真实数据填充建议

当 Phase 2 工程完成后，真实填充建议分三步：

## Step 1：先映射历史交易标的

```text
从 Phase 1 trade_ledger 中提取所有 ticker。
优先补 security_master、industry_classification、benchmark_mapping。
```

## Step 2：再映射当前持仓和观察池

```text
当前持仓必须有 industry_l2 + benchmark。
观察池必须有 industry_l1 + benchmark。
重点候选必须有 chain_mapping。
```

## Step 3：最后补高频产业链

优先顺序：

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

不要一开始平均铺开 31 行业深研。  
先把你的历史交易和当前研究池打透。

---

# 二十、与后续阶段关系

## 对 Phase 3 的支持

Phase 3 需要：

```text
industry_benchmark
theme_benchmark
peer_group
```

来计算：

```text
alpha_vs_industry
alpha_vs_theme
peer_relative_return
```

## 对 Phase 4 的支持

FactorFactory 需要：

```text
industry_classification
peer_group
sector_holdout
cross_section_rank
```

来做：

```text
IC
RankIC
Decile Return
Sector Holdout
```

## 对 Phase 5 的支持

AutoCaseForge 需要：

```text
chain_mapping
theme_mapping
benchmark_mapping
stock_role_mapping
```

来判断：

```text
case_type
module_attribution
industry_alpha
missed_opportunity
false_positive
```

## 对 Phase 8 的支持

行业知识库需要：

```text
industry_card
chain_card
company_mapping
false_signal_library
```

而 Phase 2 是所有这些知识卡的主键系统。

---

# 二十一、最终裁决

Phase 2 的本质是：

```text
给所有股票建立“身份系统”和“比较系统”。
```

没有 Phase 2，系统无法判断：

```text
股票涨跌到底是市场、行业、主题、产业链，还是个股自身 alpha。
```

完成 Phase 2 后，Z-MATRIX-OS 才能进入真正的后验验证阶段：

```text
Phase 3：行情 / 基准 / Outcome 验证库
```

这一步会把你的 5 年交易结果和行业/主题/基准连接起来，真正开始回答：

```text
我到底有没有 alpha？
```


---

# Phase 2 A+ 额外加固项

## P2-A+ 映射证据卡

每一条 `chain_mapping` 必须可生成 Evidence Card：

```json
{
  "ticker": "",
  "mapping_type": "CHAIN_MAPPING",
  "claim": "",
  "evidence_grade": "A/B/C/D",
  "evidence_refs": [],
  "financial_validation": "VALIDATED/PARTIAL/UNVERIFIED/CONTRADICTED",
  "review_required": true,
  "production_allowed": false
}
```

## P2-A+ 概念标签阻断测试

新增测试必须证明：

```text
只有 theme_name=机器人，不能自动给 chain_layer=HARDWARE_BOTTLENECK。
只有概念标签，value_capture_grade 不得高于 C。
financial_validation=UNVERIFIED 时，quality_status 不得 READY。
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
