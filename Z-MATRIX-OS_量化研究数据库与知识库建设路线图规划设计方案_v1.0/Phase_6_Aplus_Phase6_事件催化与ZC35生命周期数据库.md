# Phase 6：事件催化与 ZC35 生命周期数据库｜A+加固执行版

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

# Phase 6：事件催化与 ZC35 生命周期数据库

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 6  
> **阶段名称**：Event Catalyst & ZC35 Lifecycle DB｜事件催化与 ZC35 生命周期数据库  
> **前置阶段**：Phase 0–5  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：事件数据库 / 催化分级 / 半衰期 / 卖事实陷阱 / 催化真空 / 跨案例验证  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 6 的目标是把 ZC35 从单案例研究原型，升级为跨标的、跨行业、跨事件类型验证的事件催化数据库。

它不回答：

```text
现在该不该买？
```

它回答：

```text
这个利好是否已经被定价？
这个催化还有多少残余能量？
这个事件是破冰突变，还是兑现窗口？
类似事件历史上有没有 alpha？
```

Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

全阶段必须保持：

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

禁止：

```text
1. 不生成真实交易建议
2. 不接 broker
3. 不开启 runtime
4. 不进入 production
5. 不改 RC1 状态
6. 不自动晋级规则
7. 不输出 BUY / SELL / AUTO_EXECUTE
```


---

# 一、核心研究问题

```text
1. 什么类型的利好半衰期最长？
2. 什么类型的利好最容易买预期卖事实？
3. scheduled event 是机会还是兑现窗口？
4. unscheduled surprise 是否真能带来超额收益？
5. 催化 stack_status=VACUUM 时，R-Matrix 信号是否应降级？
6. 催化等级 S/A/B/C/D 是否对应后验收益差异？
7. residual_power 是否与未来 T5/T20 alpha 相关？
```

---

# 二、数据目录

```text
data/research_db/event/
  README.md

  raw/
    news_imports/
    announcement_imports/
    manual_events/
    .gitkeep

  staging/
    imported_event_raw.jsonl
    imported_catalyst_raw.jsonl
    import_error_rows.jsonl

  normalized/
    event_ledger.jsonl
    catalyst_ledger.jsonl
    scheduled_event_calendar.csv
    catalyst_decay_observation.csv
    sell_on_news_ledger.jsonl
    catalyst_stack_ledger.jsonl
    catalyst_outcome_link.csv
    catalyst_cross_case_validation.csv

  reports/
    catalyst_lifecycle_report.md
    sell_on_news_report.md
    catalyst_decay_report.md
    catalyst_vacuum_report.md
    zc35_cross_case_validation_report.md
```

---

# 三、代码模块

```text
zmatrix/research_db/zc35_event/
  __init__.py
  event_schema.py
  catalyst_schema.py
  catalyst_taxonomy.py
  event_loader.py
  event_normalizer.py
  scheduled_event_classifier.py
  catalyst_grade_classifier.py
  surprise_scorer.py
  residual_power_model.py
  catalyst_stack_engine.py
  sell_on_news_detector.py
  catalyst_outcome_linker.py
  catalyst_cross_case_validator.py
  zc35_event_report.py
```

---

# 四、事件表规范

## 4.1 event_ledger.jsonl

```json
{
  "event_id": "EVT-20260601-002472-001",
  "ticker": "002472.SZ",
  "event_date": "2026-06-01",
  "event_time": null,
  "event_type": "PRODUCT_BREAKTHROUGH",
  "scheduled": false,
  "source": "manual",
  "source_url": "",
  "title": "",
  "summary": "",
  "as_of_date": "2026-06-01",
  "pit_status": "PIT_SAFE",
  "data_status": "MANUAL_IMPORT",
  "quality_status": "READY",
  "production_allowed": false
}
```

## 4.2 catalyst_ledger.jsonl

```json
{
  "catalyst_id": "CAT-20260601-002472-001",
  "event_id": "EVT-20260601-002472-001",
  "ticker": "002472.SZ",
  "catalyst_grade": "S",
  "surprise_level": "HIGH",
  "business_relevance": "HIGH",
  "financial_validation": "UNVERIFIED",
  "scheduled": false,
  "half_life_days": 7,
  "full_decay_days": 15,
  "residual_power": 1.0,
  "sell_on_news_risk": "LOW_AT_BIRTH",
  "paper_trackable": true,
  "production_allowed": false
}
```

---

# 五、事件分类

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
NOISE
```

---

# 六、催化等级

```text
S：超级信号，非计划、低预期、强产业重构
A：强催化，业务关联强，市场未完全定价
B：中等催化，具备交易关注价值
C：弱催化，更多是情绪或确认
D：负催化或噪音
```

必须字段：

```text
catalyst_grade
surprise_level
business_relevance
financial_validation
scheduled
pre_event_runup
crowding_status
residual_power
```

---

# 七、半衰期模型

必须避免旧 bug：

```text
days_since_event < -pre_run_days → residual_power=0
-pre_run_days <= days_since_event < 0 → pre-run ramp
days_since_event == 0 → birth power
0 < days_since_event <= full_decay_days → exponential decay
days_since_event > full_decay_days → residual_power≈0
```

公式实现可用：

```text
power_t = power_0 * exp(-lambda * t)
```

但 `lambda` 必须由配置控制，不得硬编码不可审计。

---

# 八、催化栈状态

`catalyst_stack_engine.py` 必须输出：

```text
ACTIVE_STACK
DECAYING_STACK
EXHAUSTED_STACK
VACUUM
CONFLICTED_STACK
DATA_INSUFFICIENT
```

硬规则：

```text
远期未发生事件不得计入 active stack。
EXHAUSTED 事件不得提升 paper_trackable。
VACUUM + R-Matrix Entry Signal → WATCH_ONLY / SYSTEM_CONFLICT。
```

---

# 九、卖事实识别

`sell_on_news_detector.py` 必须检查：

```text
scheduled=true
event前5日涨幅
event前10日涨幅
成交量拥挤
T0 下跌
T1/T3/T5 回撤
高开低走
放量滞涨
```

输出：

```text
SELL_ON_NEWS_CONFIRMED
SELL_ON_NEWS_RISK
NO_SELL_ON_NEWS
DATA_INSUFFICIENT
```

---

# 十、Outcome 连接

`catalyst_outcome_linker.py` 必须连接 Phase 3：

```text
T1/T3/T5/T10/T20/T60 returns
alpha_vs_industry
alpha_vs_theme
net_executable_return
MFE
MAE
```

不足窗口不得 ready。

---

# 十一、跨案例验证

`catalyst_cross_case_validator.py` 必须输出：

```text
case_count
cross_ticker_count
industry_count
event_type_count
regime_count
validation_status
promotion_allowed=false
```

晋级规则：

```text
<3 案例：LESSON_ONLY
>=3 同类案例：CATALYST_RULE_CANDIDATE
>=10 跨标的：RESEARCH_RULE_CANDIDATE
>=20 跨标的 + >=2 regime：PAPER_RULE_CANDIDATE
production_allowed=false
```

---

# 十二、测试目录

```text
tests/research_db/zc35_event/
  test_event_schema.py
  test_catalyst_schema.py
  test_catalyst_taxonomy.py
  test_scheduled_event_classifier.py
  test_catalyst_grade_classifier.py
  test_surprise_scorer.py
  test_residual_power_model.py
  test_catalyst_stack_engine.py
  test_sell_on_news_detector.py
  test_catalyst_outcome_linker.py
  test_catalyst_cross_case_validator.py
  test_no_production_boundary.py
```

必须测试：

```text
1. 远期未发生事件 residual_power=0
2. 远期未发生事件不进入 active stack
3. scheduled event T0 后跌幅触发 SELL_ON_NEWS_RISK
4. VACUUM + R signal 触发 WATCH_ONLY
5. T20 不足阻断 outcome
6. 单案例不得晋级
7. 所有输出 production_allowed=false
```

---

# 十三、Verify 脚本

```text
scripts/verify_research_db_phase6_zc35_event.sh
```

必须运行：

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/zc35_event/
```

并扫描 forbidden flags。

---

# 十四、报告

必须生成：

```text
catalyst_lifecycle_report.md
sell_on_news_report.md
catalyst_decay_report.md
catalyst_vacuum_report.md
zc35_cross_case_validation_report.md
```

报告必须包含：

```text
事件总数
S/A/B/C/D 分布
scheduled/unscheduled 分布
sell-on-news 数量
VACUUM 案例数
平均 T5/T20 alpha
净可执行收益
不可晋级清单
```

---

# 十五、Acceptance Matrix

```text
docs/research_db/PHASE6_ACCEPTANCE_MATRIX.md
```

Final Status:

```text
PHASE6_READY_FOR_B_MATRIX_FINANCIAL_SNAPSHOT
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十六、执行批次

```text
Batch P6-A：目录 + schema
Batch P6-B：taxonomy + classifier + surprise scorer
Batch P6-C：residual power + stack engine
Batch P6-D：sell-on-news + outcome linker
Batch P6-E：cross-case validator + reports
Batch P6-F：tests + verify
Batch P6-G：closeout
```

---

# 十七、完成报告格式

```text
## ResearchDB Phase 6 完成报告
commit:
branch:

### Directories
- raw:
- staging:
- normalized:
- reports:

### Code
- event_schema:
- catalyst_schema:
- catalyst_taxonomy:
- scheduled_event_classifier:
- catalyst_grade_classifier:
- residual_power_model:
- catalyst_stack_engine:
- sell_on_news_detector:
- catalyst_outcome_linker:
- catalyst_cross_case_validator:

### Tests
- tests/research_db/zc35_event:
- verify_research_db_phase6_zc35_event.sh:

### Final Status
ResearchDB Phase 6: PASS / FAIL
Next Phase: Phase 7 Financial Snapshot & B-Matrix DB
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十八、最终裁决

Phase 6 的本质是：

```text
把“利好消息”从主观叙事，升级为有生命周期、有半衰期、有兑现风险、有后验验证的研究资产。
```


---

# Phase 6 A+ 额外加固项

## P6-A+ ZC35 Config 目录

必须新增：

```text
configs/zc35/catalyst_taxonomy.yaml
configs/zc35/decay_parameters.yaml
configs/zc35/sell_on_news_thresholds.yaml
```

所有半衰期、衰减参数、卖事实阈值必须从配置读取，不得硬编码在函数内部。

## P6-A+ 002472 回归样本

必须新增 fixture：

```text
tests/fixtures/zc35_event/002472_catalyst_vacuum_case.json
```

必须验证：

```text
1. stack_status=VACUUM
2. residual_power < 0.2
3. R signal + VACUUM → WATCH_ONLY
4. production_allowed=false
```

## P6-A+ Sell-on-News Golden Cases

至少 3 个虚构 fixture：

```text
scheduled_event_pre_runup_then_drop.json
unscheduled_surprise_continues.json
weak_noise_no_alpha.json
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
