# Phase 5：AutoCaseForge 案例记忆与自动内化系统｜A+加固执行版

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

# 原始 AutoCaseForge v1.0 工程说明书完整吸收区

# AutoCaseForge v1.0｜工程落地执行说明书

> **版本**：v1.0  
> **适用系统**：Z-MATRIX-OS v4.0 FINAL-HARDGATES 之后  
> **执行对象**：OpenClaw 天师 / DeepSeek-v4-pro  
> **系统定位**：事件触发、自动建案、人工确认、跨案例验证、系统记忆内化  
> **硬边界**：Research Only / Paper Only / No Production / No Broker / No Runtime / No Real Trade

---

## 0. 总裁决

AutoCaseForge v1.0 不是“复盘文章生成器”，也不是“自动交易建议系统”。

它是 Z-MATRIX 的 **自动化案例锻造与记忆内化系统**：

```text
事件发生 → 自动记录
触发规则 → 自动建案
行情推进 → 自动更新 outcome
系统冲突 → 自动归因
规则候选 → 自动进入验证队列
人工确认 → 决定是否纳入系统记忆
跨案例达标 → 才允许进入 research rule / paper rule
```

第一阶段核心目标只有三个：

```text
1. 自动落盘：不再依赖人工想起来才复盘。
2. 自动排队：每天生成 review_queue.md，让人只做确认。
3. 自动内化：每周/月生成 case memory report，把个案沉淀为系统记忆候选。
```

必须坚持：

```text
自动化负责留痕，不负责最终裁判。
系统可以生成 case draft，但不能自动晋级规则。
单案例只能形成 lesson，不能形成 rule。
任何案例都不能直接进入 production。
```

---

## 1. 工程边界

### 1.1 允许

```text
1. 新增 data/caseforge/ 文件制数据库。
2. 新增 zmatrix/caseforge/ 模块。
3. 新增 AutoCaseForge 日/周/月运行脚本。
4. 读取 watchlist、holdings、events、daily_prices 等 CSV/JSONL 输入。
5. 自动生成 case draft、ledgers、review queue、weekly report、monthly memory report。
6. 生成 rule candidate，但 promotion_allowed 必须为 false。
7. 输出系统记忆候选，但必须 human_review_required=true。
```

### 1.2 禁止

```text
1. 不得接 broker。
2. 不得开启 runtime。
3. 不得生成真实交易指令。
4. 不得修改 classifier 生产链。
5. 不得修改 RC1 audit 结论。
6. 不得创建 tag。
7. 不得让单案例晋级为规则。
8. 不得自动把 rule_candidate 写入生产策略。
9. 不得输出 BUY / SELL / AUTO_EXECUTE / BROKER_ORDER。
10. 不得把 AUTO_DRAFT 当成 HUMAN_REVIEWED。
```

### 1.3 全局安全字段

所有 AutoCaseForge 输出对象必须包含并保持：

```json
{
  "production_allowed": false,
  "real_trade_allowed": false,
  "broker_order_allowed": false,
  "runtime_enabled": false,
  "auto_buy_allowed": false,
  "auto_sell_allowed": false,
  "paper_only": true,
  "human_review_required": true
}
```

---

## 2. 系统总体架构

```text
AutoCaseForge v1.0

Input Layer
├── watchlist.csv
├── holdings.csv
├── research_universe.csv
├── events.jsonl
├── daily_prices.csv
├── benchmark_prices.csv
├── catalyst_events.jsonl
└── human_actions.jsonl

Event Layer
├── EventCollector
├── EventNormalizer
└── EventLedger

Trigger Layer
├── TriggerEngine
├── 12 Built-in Trigger Rules
└── TriggerResult

Case Layer
├── AutoCaseBuilder
├── 12 Case Cards
├── Structured Case JSON
└── Case Ledger

Outcome Layer
├── OutcomeUpdater
├── ForwardTradingDayGuard
├── AlphaCalculator
└── Outcome Ledger

Review Layer
├── ReviewQueue
├── HumanReviewAction
└── Decision Ledger

Memory Layer
├── RuleCandidateQueue
├── CrossCaseValidator
├── WeeklyCaseReport
├── MonthlyMemoryReport
└── SystemMemoryCandidate
```

---

## 3. 目录结构

必须新增以下目录：

```text
data/caseforge/
├── input/
│   ├── watchlist.csv
│   ├── holdings.csv
│   ├── research_universe.csv
│   ├── events.jsonl
│   ├── daily_prices.csv
│   ├── benchmark_prices.csv
│   ├── catalyst_events.jsonl
│   └── human_actions.jsonl
├── ledgers/
│   ├── event_ledger.jsonl
│   ├── case_ledger.jsonl
│   ├── decision_ledger.jsonl
│   ├── outcome_ledger.jsonl
│   ├── rule_candidate_ledger.jsonl
│   └── memory_candidate_ledger.jsonl
├── structured/
│   └── .gitkeep
├── reviews/
│   └── .gitkeep
├── rule_candidates/
│   └── .gitkeep
├── validation/
│   └── .gitkeep
└── reports/
    ├── review_queue.md
    ├── weekly_case_report.md
    └── monthly_memory_report.md

zmatrix/caseforge/
├── __init__.py
├── case_schema.py
├── event_collector.py
├── event_normalizer.py
├── trigger_engine.py
├── trigger_rules.py
├── auto_case_builder.py
├── ledger_writer.py
├── ledger_reader.py
├── outcome_updater.py
├── forward_day_guard.py
├── alpha_calculator.py
├── review_queue.py
├── rule_candidate_queue.py
├── cross_case_validator.py
├── memory_integrator.py
├── caseforge_report.py
├── scheduler.py
└── safety.py

tests/caseforge/
├── test_case_schema.py
├── test_event_collector.py
├── test_trigger_engine.py
├── test_auto_case_builder.py
├── test_ledger_writer.py
├── test_outcome_updater.py
├── test_forward_day_guard.py
├── test_review_queue.py
├── test_rule_candidate_queue.py
├── test_cross_case_validator.py
├── test_memory_integrator.py
└── test_caseforge_safety.py

scripts/
├── caseforge_daily_run.sh
├── caseforge_weekly_closeout.sh
├── caseforge_monthly_validation.sh
└── verify_autocaseforge_v1.sh

docs/caseforge/
├── AUTOCASEFORGE_V1_SCOPE_LOCK.md
├── AUTOCASEFORGE_V1_SCHEMA.md
├── AUTOCASEFORGE_V1_TRIGGER_RULES.md
├── AUTOCASEFORGE_V1_OPERATION_GUIDE.md
└── AUTOCASEFORGE_V1_CLOSEOUT.md
```

---

## 4. 输入文件规范

### 4.1 watchlist.csv

路径：

```text
data/caseforge/input/watchlist.csv
```

字段：

```csv
ticker,name,added_date,thesis_id,source_module,status,priority,industry,theme
002472,双环传动,2026-05-29,THESIS-002472-001,ZC35,ACTIVE,HIGH,机器人,人形机器人
```

必填：

```text
ticker
added_date
thesis_id
source_module
status
```

---

### 4.2 holdings.csv

```csv
ticker,name,position_pct,cost_price,current_price,entry_date,thesis_id,industry,benchmark_id
002472,双环传动,0.00,0,0,2026-05-29,THESIS-002472-001,机器人,BENCH-ROBOTICS
```

允许空仓，但字段必须存在。

---

### 4.3 research_universe.csv

```csv
ticker,name,industry,theme,last_research_date,research_status
002472,双环传动,机器人,减速器,2026-05-29,ACTIVE
```

---

### 4.4 events.jsonl

每行一个 JSON：

```json
{"event_id":"EVT-20260529-002472-001","ticker":"002472","event_date":"2026-05-29","event_type":"CATALYST_VACUUM","source_module":"ZC35","payload":{"residual_power":0.12,"stack_status":"VACUUM"}}
```

---

### 4.5 daily_prices.csv

```csv
ticker,trade_date,open,high,low,close,volume,pct_chg,limit_up,limit_down,suspended
002472,2026-05-29,0,0,0,0,0,0,false,false,false
```

---

### 4.6 benchmark_prices.csv

```csv
benchmark_id,trade_date,close,pct_chg
BENCH-ROBOTICS,2026-05-29,0,0
```

---

### 4.7 catalyst_events.jsonl

```json
{"event_id":"CAT-002472-20260514-001","ticker":"002472","event_date":"2026-05-14","event_name":"宇树GD01发布","scheduled":false,"catalyst_grade":"S","residual_power":0.12,"stack_status":"VACUUM","paper_trackable":false}
```

---

### 4.8 human_actions.jsonl

```json
{"action_id":"ACT-20260529-001","ticker":"002472","action_date":"2026-05-29","action_type":"WATCH","thesis_id":"THESIS-002472-001","note":"加入观察"}
```

---

## 5. 核心数据结构

必须在 `zmatrix/caseforge/case_schema.py` 中实现。

### 5.1 枚举常量

```python
CASE_STATUS = {
    "AUTO_DRAFT",
    "HUMAN_REVIEW_REQUIRED",
    "HUMAN_APPROVED",
    "REJECTED",
    "CLOSED",
}

CASE_TYPES = {
    "TRUE_POSITIVE",
    "FALSE_POSITIVE",
    "FALSE_NEGATIVE",
    "MISSED_OPPORTUNITY",
    "SELL_ON_NEWS_TRAP",
    "CATALYST_LIFECYCLE",
    "EXECUTION_FAILURE",
    "EXIT_FAILURE",
    "ACCOUNT_FEEDBACK",
    "SYSTEM_CONFLICT",
    "R_MATRIX_VALIDATION",
    "WATCHLIST_EVENT",
}

ERROR_TYPES = {
    "NONE",
    "CATALYST_EXHAUSTION",
    "CATALYST_VACUUM",
    "SELL_ON_NEWS",
    "R_MATRIX_FALSE_POSITIVE",
    "B_MATRIX_SUPPORT_WEAK",
    "D_MATRIX_FLOW_REVERSAL",
    "ZC40_NOT_FILLABLE",
    "ACCOUNT_ALPHA_NEGATIVE",
    "SYSTEM_CONFLICT",
    "INSUFFICIENT_FORWARD_DAYS",
}
```

---

### 5.2 CaseHeader

```python
@dataclass
class CaseHeader:
    case_id: str
    ticker: str
    name: str | None
    case_type: str
    case_date_start: str
    case_date_end: str | None
    status: str = "AUTO_DRAFT"
    data_status: str = "LIVE_CASE_STUDY"
    backtest_validated: bool = False
    cross_ticker_validated: bool = False
    production_allowed: bool = False
    real_trade_allowed: bool = False
    broker_order_allowed: bool = False
    runtime_enabled: bool = False
    paper_only: bool = True
    human_review_required: bool = True
```

---

### 5.3 ThesisCard

```python
@dataclass
class ThesisCard:
    thesis_id: str
    core_view: str
    expected_path: str | None
    expected_horizon: str | None
    confidence: str | None
    source: str
    created_at: str
```

---

### 5.4 SignalStackCard

```python
@dataclass
class SignalStackCard:
    r_matrix: dict = field(default_factory=dict)
    b_matrix: dict = field(default_factory=dict)
    d_matrix: dict = field(default_factory=dict)
    zc35: dict = field(default_factory=dict)
    zc40: dict = field(default_factory=dict)
    zc50: dict = field(default_factory=dict)
    conflict_flags: list[str] = field(default_factory=list)
```

---

### 5.5 CatalystEventCard

```python
@dataclass
class CatalystEventCard:
    event_id: str
    event_name: str
    event_type: str
    scheduled: bool
    catalyst_grade: str
    surprise_level: str | None
    business_relevance: str | None
    financial_validation: str | None
    event_date: str
    residual_power: float | None = None
    stack_status: str | None = None
    sell_on_news_risk: str | None = None
```

---

### 5.6 PricePathCard

```python
@dataclass
class PricePathCard:
    t0_price: float | None = None
    t1_return: float | None = None
    t3_return: float | None = None
    t5_return: float | None = None
    t10_return: float | None = None
    t20_return: float | None = None
    t60_return: float | None = None
    max_favorable_excursion: float | None = None
    max_adverse_excursion: float | None = None
    invalidation_date: str | None = None
    recovery_after_invalidation: bool | None = None
```

T20/T60 必须严格 forward trading days，不足时不能填最后价格。

---

### 5.7 DecisionTimelineCard

```python
@dataclass
class DecisionTimelineItem:
    date: str
    observation: str
    system_action: str
    human_action: str | None
    source_event_id: str | None = None

@dataclass
class DecisionTimelineCard:
    items: list[DecisionTimelineItem] = field(default_factory=list)
```

---

### 5.8 ErrorAttributionCard

```python
@dataclass
class ErrorAttributionCard:
    primary_error_layer: str | None
    secondary_error_layer: str | None
    error_type: str
    lookahead_risk: bool = False
    avoidable: bool | None = None
    system_patch_required: bool = False
```

---

### 5.9 ExpertReviewCard

```python
@dataclass
class ExpertReviewCard:
    reviews: dict = field(default_factory=dict)
    review_status: str = "NOT_REVIEWED"
```

---

### 5.10 OutcomeCard

```python
@dataclass
class OutcomeCard:
    actual_result: str | None = None
    gross_return: float | None = None
    net_return_after_cost: float | None = None
    benchmark_return: float | None = None
    industry_return: float | None = None
    alpha_vs_industry: float | None = None
    max_drawdown: float | None = None
    opportunity_cost: float | None = None
    ready: bool = False
    blocked_reason: str | None = None
```

---

### 5.11 RulePatchCard

```python
@dataclass
class RulePatchCard:
    patch_required: bool
    target_module: str | None
    patch_name: str | None
    proposed_rule: str | None
    promotion_allowed: bool = False
    validation_required: str = "cross_ticker"
```

---

### 5.12 ValidationRequirementCard

```python
@dataclass
class ValidationRequirementCard:
    needs_cross_ticker_validation: bool = True
    minimum_cases_required: int = 10
    minimum_industries_required: int = 3
    minimum_market_regimes_required: int = 2
    promotion_allowed_now: bool = False
```

---

### 5.13 AuditCard

```python
@dataclass
class AuditCard:
    created_at: str
    updated_at: str
    data_sources: list[str]
    evidence_refs: list[str]
    human_notes: list[str] = field(default_factory=list)
    llm_generated: bool = True
    human_reviewed: bool = False
    rc1_scope: bool = False
    production_allowed: bool = False
```

---

### 5.14 StructuredCase

```python
@dataclass
class StructuredCase:
    header: CaseHeader
    thesis: ThesisCard
    signal_stack: SignalStackCard
    catalyst_events: list[CatalystEventCard]
    price_path: PricePathCard
    decision_timeline: DecisionTimelineCard
    error_attribution: ErrorAttributionCard
    expert_review: ExpertReviewCard
    outcome: OutcomeCard
    rule_patch: RulePatchCard
    validation_requirement: ValidationRequirementCard
    audit: AuditCard
```

必须提供：

```python
def to_dict(self) -> dict: ...
def to_json(self) -> str: ...
@classmethod
def from_dict(cls, data: dict) -> "StructuredCase": ...
```

---

## 6. 五大 Ledger

必须在 `zmatrix/caseforge/ledger_writer.py` 实现 append-only 写入。

路径：

```text
data/caseforge/ledgers/event_ledger.jsonl
data/caseforge/ledgers/case_ledger.jsonl
data/caseforge/ledgers/decision_ledger.jsonl
data/caseforge/ledgers/outcome_ledger.jsonl
data/caseforge/ledgers/rule_candidate_ledger.jsonl
data/caseforge/ledgers/memory_candidate_ledger.jsonl
```

### 6.1 LedgerWriter

```python
class LedgerWriter:
    def __init__(self, root: str = "data/caseforge/ledgers"):
        ...

    def append_event(self, record: dict) -> None: ...
    def append_case(self, record: dict) -> None: ...
    def append_decision(self, record: dict) -> None: ...
    def append_outcome(self, record: dict) -> None: ...
    def append_rule_candidate(self, record: dict) -> None: ...
    def append_memory_candidate(self, record: dict) -> None: ...
```

### 6.2 LedgerWriter 硬规则

```text
1. append-only，不得覆盖旧 ledger。
2. 每条记录必须有 created_at。
3. 每条记录必须有 source。
4. 每条记录必须 production_allowed=false。
5. 写入失败必须抛错，不得静默跳过。
```

---

## 7. 事件采集器

文件：

```text
zmatrix/caseforge/event_collector.py
```

### 7.1 EventCollector

```python
class EventCollector:
    def __init__(self, input_root: str = "data/caseforge/input"):
        ...

    def collect_watchlist_events(self) -> list[dict]: ...
    def collect_holding_events(self) -> list[dict]: ...
    def collect_catalyst_events(self) -> list[dict]: ...
    def collect_human_action_events(self) -> list[dict]: ...
    def collect_price_events(self) -> list[dict]: ...
    def collect_all(self) -> list[dict]: ...
```

### 7.2 EventNormalizer

文件：

```text
zmatrix/caseforge/event_normalizer.py
```

所有事件必须标准化为：

```json
{
  "event_id": "EVT-YYYYMMDD-TICKER-NNN",
  "ticker": "002472",
  "event_date": "2026-05-29",
  "event_type": "CATALYST_VACUUM",
  "source_module": "ZC35",
  "payload": {},
  "production_allowed": false,
  "real_trade_allowed": false,
  "broker_order_allowed": false
}
```

---

## 8. 12 条自动触发规则

文件：

```text
zmatrix/caseforge/trigger_rules.py
```

必须内置 12 条规则：

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

### 8.1 TriggerResult

```python
@dataclass
class TriggerResult:
    triggered: bool
    trigger_id: str
    case_type: str | None
    error_type: str | None
    source_module: str
    priority: str
    reason: str
    event_id: str | None
    production_allowed: bool = False
    real_trade_allowed: bool = False
    broker_order_allowed: bool = False
```

### 8.2 TriggerEngine

文件：

```text
zmatrix/caseforge/trigger_engine.py
```

接口：

```python
class TriggerEngine:
    def evaluate_event(self, event: dict, context: dict | None = None) -> list[TriggerResult]: ...
    def evaluate_events(self, events: list[dict], context: dict | None = None) -> list[TriggerResult]: ...
```

规则：

```text
1. 一个 event 可触发多个 TriggerResult。
2. 无 trigger 时只进 event_ledger，不建 case。
3. trigger 结果 production_allowed 必须 false。
4. SYSTEM_CONFLICT 优先级最高。
```

---

## 9. AutoCaseBuilder

文件：

```text
zmatrix/caseforge/auto_case_builder.py
```

接口：

```python
class AutoCaseBuilder:
    def build_case(self, event: dict, trigger: TriggerResult, context: dict | None = None) -> StructuredCase: ...
    def save_case(self, case: StructuredCase, output_root: str = "data/caseforge/structured") -> str: ...
```

### 9.1 建案规则

```text
1. case_id 格式：ZCASE-YYYY-NNNN。
2. 默认 status=AUTO_DRAFT。
3. 默认 human_review_required=true。
4. 默认 production_allowed=false。
5. 字段不足必须写 DATA_INSUFFICIENT。
6. 不得因为字段不足而跳过建案，除非 ticker/event_date/source_module 缺失。
```

### 9.2 质量门

满足以下才进入 case_ledger：

```text
ticker 有
trigger 有
event_date 有
source_module 有
case_type 可推断
audit 字段完整
production_allowed=false
```

否则只写 event_ledger。

---

## 10. OutcomeUpdater

文件：

```text
zmatrix/caseforge/outcome_updater.py
zmatrix/caseforge/forward_day_guard.py
```

### 10.1 ForwardTradingDayGuard

```python
class ForwardTradingDayGuard:
    @staticmethod
    def count_forward_days(trade_dates: list[str], start_date: str, horizon: int) -> int: ...

    @staticmethod
    def horizon_ready(trade_dates: list[str], start_date: str, horizon: int) -> dict: ...
```

规则：

```text
T5  必须有 >= 5 个 forward trading days。
T20 必须有 >= 20 个 forward trading days。
T60 必须有 >= 60 个 forward trading days。
不足返回 ready=false、reason=INSUFFICIENT_FORWARD_DAYS。
禁止用最后价格代替目标 horizon 价格。
```

### 10.2 OutcomeUpdater

```python
class OutcomeUpdater:
    def update_case_outcome(self, case: StructuredCase, price_rows: list[dict], benchmark_rows: list[dict]) -> StructuredCase: ...
```

必须计算：

```text
T1/T3/T5/T10/T20/T60 return
benchmark_return
alpha_vs_benchmark
max_favorable_excursion
max_adverse_excursion
ready / blocked_reason
```

---

## 11. ReviewQueue

文件：

```text
zmatrix/caseforge/review_queue.py
```

接口：

```python
class ReviewQueue:
    def build_queue(self, cases: list[StructuredCase]) -> str: ...
    def save_queue(self, markdown: str, path: str = "data/caseforge/reports/review_queue.md") -> None: ...
```

输出必须包含：

```markdown
# AutoCaseForge Review Queue

## Summary
- AUTO_DRAFT: x
- HUMAN_REVIEW_REQUIRED: x
- HIGH_PRIORITY: x

## Cases
### ZCASE-2026-0001｜002472 双环传动
- Trigger: CATALYST_VACUUM
- Case Type: FALSE_POSITIVE
- Error Type: CATALYST_EXHAUSTION
- Suggested Action: REVIEW
- Human Review Required: TRUE
- Production Allowed: FALSE
```

不得出现：

```text
BUY
SELL
AUTO_EXECUTE
```

---

## 12. RuleCandidateQueue

文件：

```text
zmatrix/caseforge/rule_candidate_queue.py
```

### 12.1 RuleCandidate

```python
@dataclass
class RuleCandidate:
    rule_id: str
    rule_name: str
    target_module: str
    source_cases: list[str]
    case_count: int
    industries: list[str]
    regimes: list[str]
    status: str
    promotion_allowed: bool = False
    production_allowed: bool = False
    human_review_required: bool = True
```

### 12.2 晋级军规

```text
1 个 case：LESSON_ONLY
3 个同类 case：RULE_CANDIDATE
10 个跨标的 case：RESEARCH_RULE_CANDIDATE
20 个跨标的 + 跨行情 case：PAPER_RULE_CANDIDATE
任何数量都不能 production。
```

少于 10 个案例时：

```text
status=INSUFFICIENT_CASES
promotion_allowed=false
```

---

## 13. CrossCaseValidator

文件：

```text
zmatrix/caseforge/cross_case_validator.py
```

接口：

```python
class CrossCaseValidator:
    def validate_rule_candidate(self, cases: list[StructuredCase], rule_name: str) -> dict: ...
```

必须检查：

```text
case_count
unique_tickers
unique_industries
unique_market_regimes
case_type_consistency
error_type_consistency
minimum_cases_required=10
minimum_industries_required=3
minimum_market_regimes_required=2
```

输出：

```json
{
  "status": "INSUFFICIENT_CASES",
  "promotion_allowed": false,
  "production_allowed": false,
  "blocked_reason": "MINIMUM_CASES_NOT_MET"
}
```

---

## 14. MemoryIntegrator

文件：

```text
zmatrix/caseforge/memory_integrator.py
```

作用：把案例周报/月报整理成系统记忆候选，但不直接写入长期 memory。

接口：

```python
class MemoryIntegrator:
    def build_memory_candidates(self, cases: list[StructuredCase], rule_candidates: list[RuleCandidate]) -> list[dict]: ...
    def save_memory_candidates(self, candidates: list[dict], ledger_path: str = "data/caseforge/ledgers/memory_candidate_ledger.jsonl") -> None: ...
```

输出：

```json
{
  "memory_id": "MEM-CF-202606-001",
  "memory_type": "ERROR_PATTERN",
  "summary": "ZC35 catalyst vacuum frequently invalidates R-Matrix continuation signals.",
  "supporting_cases": ["ZCASE-2026-0001"],
  "confidence": "LOW",
  "promotion_allowed": false,
  "human_review_required": true
}
```

### 14.1 记忆内化军规

```text
1. 单案例只生成 LOW confidence memory candidate。
2. 少于 3 个案例不得生成 rule memory。
3. 少于 10 个案例不得生成 research rule memory。
4. human_reviewed=false 时不得写入正式系统记忆。
5. memory candidate 只能进 ledger，不得修改 RC1 / production 策略。
```

---

## 15. Scheduler

文件：

```text
zmatrix/caseforge/scheduler.py
```

注意：scheduler 不是后台常驻服务，只是命令编排器。

```python
class CaseForgeScheduler:
    def run_daily(self) -> dict: ...
    def run_weekly(self) -> dict: ...
    def run_monthly(self) -> dict: ...
```

---

## 16. 脚本

### 16.1 caseforge_daily_run.sh

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHONPATH=. python3 - <<'PY'
from zmatrix.caseforge.scheduler import CaseForgeScheduler
r = CaseForgeScheduler().run_daily()
print(r)
PY
```

每日职责：

```text
collect events
apply triggers
build auto draft cases
write ledgers
generate review_queue.md
```

---

### 16.2 caseforge_weekly_closeout.sh

周度职责：

```text
update outcomes
close expired cases
generate weekly_case_report.md
update rule_candidate_ledger
```

---

### 16.3 caseforge_monthly_validation.sh

月度职责：

```text
cross-case validation
memory candidate generation
monthly_memory_report.md
```

---

### 16.4 verify_autocaseforge_v1.sh

必须运行：

```bash
#!/usr/bin/env bash
set -euo pipefail

python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/caseforge/

bash scripts/caseforge_daily_run.sh
bash scripts/caseforge_weekly_closeout.sh
bash scripts/caseforge_monthly_validation.sh

python3 - <<'PY'
from pathlib import Path

required = [
    "data/caseforge/ledgers/event_ledger.jsonl",
    "data/caseforge/ledgers/case_ledger.jsonl",
    "data/caseforge/reports/review_queue.md",
]
for r in required:
    assert Path(r).exists(), f"missing {r}"

for p in Path("zmatrix/caseforge").rglob("*.py"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    for token in [
        "real_trade_allowed=True",
        "broker_order_allowed=True",
        "runtime_enabled=True",
        "auto_buy_allowed=True",
        "auto_sell_allowed=True",
        "production_allowed=True",
        "AUTO_EXECUTE",
        "BROKER_ORDER",
    ]:
        assert token not in text, f"Forbidden token {token} in {p}"

print("✅ AutoCaseForge v1.0 verification PASS")
PY
```

---

## 17. 初始样本：002472 双环传动

必须用现有 ZC35 双环传动档案生成第一个 AUTO_DRAFT case。

输入来源：

```text
data/stock_profiles/002472_双环传动_catalyst_profile.json
```

输出：

```text
data/caseforge/structured/ZCASE-2026-0001.json
```

建议字段：

```json
{
  "case_id": "ZCASE-2026-0001",
  "ticker": "002472",
  "name": "双环传动",
  "case_type": "FALSE_POSITIVE",
  "error_type": "CATALYST_EXHAUSTION",
  "source_module": "ZC35",
  "data_status": "LIVE_CASE_STUDY",
  "backtest_validated": false,
  "cross_ticker_validated": false,
  "production_allowed": false,
  "status": "AUTO_DRAFT"
}
```

必须生成 review_queue 条目。

---

## 18. 测试要求

### 18.1 test_case_schema.py

必须测试：

```text
StructuredCase 可序列化/反序列化
所有安全字段默认为 false
human_review_required 默认为 true
```

### 18.2 test_trigger_engine.py

必须测试 12 条规则至少 6 条：

```text
price event
momentum event
catalyst exhaustion
catalyst vacuum
execution failure
account alpha negative
system conflict
```

### 18.3 test_auto_case_builder.py

必须测试：

```text
TriggerResult → StructuredCase
case status=AUTO_DRAFT
production_allowed=false
字段不足显示 DATA_INSUFFICIENT
```

### 18.4 test_ledger_writer.py

必须测试：

```text
append-only
created_at 自动存在
production_allowed=false
jsonl 可读
```

### 18.5 test_outcome_updater.py

必须测试：

```text
T5 ready
T20 insufficient
T60 insufficient
禁止 fallback last price
alpha_vs_benchmark
```

### 18.6 test_review_queue.py

必须测试：

```text
生成 review_queue.md
包含 HUMAN_REVIEW_REQUIRED
不包含 BUY/SELL/AUTO_EXECUTE
```

### 18.7 test_rule_candidate_queue.py

必须测试：

```text
1 case → LESSON_ONLY
3 cases → RULE_CANDIDATE
<10 cases → INSUFFICIENT_CASES
promotion_allowed=false
```

### 18.8 test_cross_case_validator.py

必须测试：

```text
少于 10 cases → INSUFFICIENT_CASES
少于 3 industries → INSUFFICIENT_INDUSTRY_COVERAGE
少于 2 regimes → INSUFFICIENT_REGIME_COVERAGE
```

### 18.9 test_memory_integrator.py

必须测试：

```text
单案例生成 LOW confidence memory candidate
human_review_required=true
promotion_allowed=false
不写正式系统记忆
```

### 18.10 test_caseforge_safety.py

必须测试：

```text
全 caseforge 模块无 forbidden flags
所有 outputs production_allowed=false
所有 scripts 不接 broker/runtime
```

---

## 19. 分批执行计划

### Batch CF-0：Scope + Skeleton

新增目录、scope 文档、schema 骨架。

Commit：

```bash
git commit -m "autocaseforge-v1-cf0: add scope and schema skeleton"
```

---

### Batch CF-1：Event + Trigger + Ledger

实现 event_collector、trigger_engine、ledger_writer。

Commit：

```bash
git commit -m "autocaseforge-v1-cf1: implement event trigger and ledgers"
```

---

### Batch CF-2：Auto Case Builder + Review Queue

实现自动建案和 review_queue。

Commit：

```bash
git commit -m "autocaseforge-v1-cf2: implement auto case builder and review queue"
```

---

### Batch CF-3：Outcome + Rule Candidate + Memory

实现 outcome_updater、rule_candidate_queue、cross_case_validator、memory_integrator。

Commit：

```bash
git commit -m "autocaseforge-v1-cf3: implement outcome rule candidate and memory candidates"
```

---

### Batch CF-4：Scripts + First Case + Verify

实现 daily/weekly/monthly 脚本，生成 002472 第一个 AUTO_DRAFT case，完成 verify。

Commit：

```bash
git commit -m "autocaseforge-v1-cf4: add scripts first case and verification"
```

---

## 20. 完成报告格式

执行完成后必须输出：

```text
## AutoCaseForge v1.0 完成报告

commit:
branch:

### CF-0 Scope + Schema
- directories:
- schema:
- docs:

### CF-1 Event + Trigger + Ledger
- event collector:
- trigger rules:
- ledgers:

### CF-2 Auto Case + Review Queue
- auto case builder:
- structured case:
- review_queue.md:

### CF-3 Outcome + Rule + Memory
- forward day guard:
- outcome updater:
- rule candidate queue:
- cross case validator:
- memory integrator:

### CF-4 Scripts + First Case
- daily script:
- weekly script:
- monthly script:
- first case:
- verify_autocaseforge_v1.sh:

### Tests
- tests/caseforge:
- passed:

### Safety
real_trade_allowed=False
broker_order_allowed=False
runtime_enabled=False
auto_buy_allowed=False
auto_sell_allowed=False
production_allowed=False

### Final Status
AutoCaseForge v1.0: RESEARCH_AUTOMATION_READY
RC1 impact: NONE
Production impact: NONE
```

---

## 21. 验收标准

AutoCaseForge v1.0 只有在以下全部满足时通过：

```text
1. data/caseforge 目录完整。
2. zmatrix/caseforge 模块完整。
3. 12 条 trigger rules 存在。
4. event/case/decision/outcome/rule/memory 6 类 ledger 可写。
5. AutoCaseBuilder 可生成 StructuredCase。
6. ReviewQueue 可生成 review_queue.md。
7. OutcomeUpdater 严格 forward trading days。
8. RuleCandidateQueue 阻止单案例晋级。
9. CrossCaseValidator 少于 10 案例返回 INSUFFICIENT_CASES。
10. MemoryIntegrator 只生成 memory candidate，不写正式记忆。
11. 002472 首个 AUTO_DRAFT case 生成。
12. tests/caseforge 全部通过。
13. verify_autocaseforge_v1.sh 通过。
14. 全模块无 production/broker/runtime/real_trade。
15. 不修改 RC1 Audit、Scorecard、Tag、Production 状态。
```

---

## 22. 最终裁决

完成后允许声明：

```text
AutoCaseForge v1.0 = RESEARCH_AUTOMATION_READY
```

不得声明：

```text
Production Ready
Broker Ready
Runtime Ready
Auto Trading Ready
Rule Promotion Ready
```

AutoCaseForge v1.0 的本质是：

```text
自动发现值得复盘的事实，自动落盘成案例草稿，自动形成记忆候选；
但最终确认、规则晋级、系统记忆写入，必须由人工裁决。
```


---

# Phase 5 与 ResearchDB Phase 0–4 的强接口

本 Phase 必须消费以下上游输入，不能自行发明字段：

```text
Phase 1：trade_ledger / position_ledger / account_daily_snapshot / watchlist_ledger
Phase 2：security_master / industry_classification / chain_mapping / benchmark_mapping
Phase 3：signal_outcome / trade_outcome / watchlist_outcome / executable_return_outcome
Phase 4：factor_registry / factor_validation / factor_promotion_ledger
```

如果上游文件不存在，AutoCaseForge 必须输出：

```json
{
  "status": "BLOCKED",
  "blocked_reason": "UPSTREAM_DATA_MISSING",
  "missing_inputs": []
}
```

不得自行造数。

# Phase 5 与 Phase 6–10 的输出接口

AutoCaseForge 输出必须被下游消费：

```text
Phase 6：event_ledger / catalyst cases / sell-on-news cases
Phase 7：B-Matrix false positive / financial mismatch cases
Phase 8：false_signal_library / chain cases
Phase 9：weakness_map / forbidden_trade_patterns
Phase 10：monthly_memory_report / cockpit review queue
```

# Phase 5 A+ 执行补强

原始《AutoCaseForge v1.0｜工程落地执行说明书》为本 Phase 主体，不得再压缩。OpenClaw 必须完整实现其中所有章节，尤其是：

```text
1. 输入文件规范
2. 5.1 枚举常量
3. 12 张卡完整字段
4. LedgerWriter append-only 硬规则
5. EventCollector / EventNormalizer
6. TriggerResult
7. Case Quality Gate
8. ForwardTradingDayGuard
9. ReviewQueue 固定格式
10. RuleCandidate 结构
11. CrossCaseValidator
12. MemoryIntegrator 内化军规
13. 002472 双环传动首个 AUTO_DRAFT case
14. 18 章测试要求
15. 19 章分批执行计划
```

如果任一项未完成，Phase 5 不得 Closeout。


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
