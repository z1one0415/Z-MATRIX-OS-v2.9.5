# Phase 9：个人操盘画像与系统建议层｜A+加固执行版

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

# Phase 9：个人操盘画像与系统建议层

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 9  
> **阶段名称**：Personal Operator Profile & Advisory Layer｜个人操盘画像与系统建议层  
> **前置阶段**：Phase 0–8  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：账户行为画像 / 优势地图 / 弱点地图 / 禁止模式 / 适配策略 / 系统建议边界  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 9 的目标不是让系统“替你操盘”，而是让系统用过去数据回答：

```text
你适合什么交易；
不适合什么交易；
哪些信号对你有效；
哪些模式会反复诱导你犯错；
你的账户承受能力边界在哪里。
```

输出的是：

```text
个人研究与操作建议层
```

不是：

```text
自动买卖系统
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

# 一、数据目录

```text
data/research_db/personal_profile/
  README.md

  normalized/
    operator_profile.json
    edge_map.json
    weakness_map.json
    forbidden_trade_patterns.json
    preferred_setup_library.json
    account_style_recommendation.json
    behavior_metrics.csv
    decision_quality_ledger.csv

  reports/
    operator_profile_report.md
    edge_map_report.md
    weakness_map_report.md
    forbidden_patterns_report.md
    strategy_fit_report.md
    personal_advisory_boundary.md
```

---

# 二、代码模块

```text
zmatrix/research_db/personal_profile/
  __init__.py
  behavior_schema.py
  trade_behavior_analyzer.py
  edge_detector.py
  weakness_detector.py
  forbidden_pattern_miner.py
  setup_library_builder.py
  account_style_classifier.py
  advisory_boundary.py
  operator_profile_builder.py
  personal_profile_report.py
```

---

# 三、画像维度

必须分析：

```text
holding_period_edge
industry_edge
chain_edge
catalyst_edge
execution_weakness
account_risk_tolerance
drawdown_behavior
sell_discipline
missed_opportunity_pattern
overtrading_pattern
position_sizing_pattern
case_learning_velocity
```

---

# 四、行为指标

```csv
metric_id,metric_name,value,period,source,confidence,quality_status
```

第一批指标：

```text
平均持仓天数
盈利交易平均持仓天数
亏损交易平均持仓天数
最大回撤容忍
止损延迟
止盈提前
错过机会频率
追高亏损频率
卖飞频率
持仓跑输行业频率
短线交易胜率
中期交易胜率
长期持有胜率
```

---

# 五、优势地图 edge_map

```json
{
  "edge_type": "INDUSTRY_EDGE",
  "description": "",
  "evidence_cases": [],
  "supporting_trades": [],
  "alpha_evidence": {},
  "confidence": "MEDIUM",
  "production_allowed": false
}
```

优势必须有数据证据：

```text
交易结果
行业 alpha
CaseForge 案例
FactorFactory 结果
```

禁止凭主观感觉写优势。

---

# 六、弱点地图 weakness_map

弱点类型：

```text
CHASE_HIGH
SELL_TOO_EARLY
HOLD_LOSER_TOO_LONG
CATALYST_EXHAUSTION_UNDERWEIGHTED
EXECUTION_IGNORED
ACCOUNT_RISK_OVERLOAD
MISSED_OPPORTUNITY
OVERTRADING
NARRATIVE_OVERCONFIDENCE
```

每个弱点必须关联：

```text
case_refs
trade_refs
loss_contribution
avoidance_rule_candidate
```

---

# 七、禁止模式 forbidden_trade_patterns

```json
{
  "pattern_id": "FORBID-001",
  "pattern_name": "R_SIGNAL_WITH_ZC35_VACUUM",
  "description": "",
  "trigger_conditions": [],
  "historical_loss_cases": [],
  "recommended_action": "WATCH_ONLY",
  "human_review_required": true,
  "production_allowed": false
}
```

注意：

```text
recommended_action 只能是研究动作：
WATCH_ONLY
PAPER_ONLY
HUMAN_REVIEW_REQUIRED
ACTION_BLOCKED
DATA_INSUFFICIENT
```

禁止：

```text
BUY
SELL
AUTO_EXECUTE
```

---

# 八、适配策略 setup_library

```text
preferred_setup_library.json
```

字段：

```json
{
  "setup_id": "",
  "setup_name": "",
  "required_conditions": [],
  "supporting_cases": [],
  "expected_horizon": "",
  "risk_budget_note": "",
  "paper_allowed": true,
  "production_allowed": false
}
```

---

# 九、账户风格分类

`account_style_classifier.py` 必须输出：

```text
LOW_FREQUENCY_RESEARCH
MID_TERM_ROTATION
EVENT_DRIVEN_PAPER
HIGH_VOLATILITY_UNSUITABLE
OVERTRADING_RISK
DRAWDOWN_SENSITIVE
```

---

# 十、建议边界 advisory_boundary

必须写死：

```text
系统只能给：
RESEARCH_SUPPORT
WATCH_ONLY
PAPER_ONLY
HUMAN_REVIEW_REQUIRED
ACTION_BLOCKED
DATA_INSUFFICIENT

系统不能给：
BUY
SELL
STRONG_BUY
AUTO_BUY
AUTO_SELL
BROKER_ORDER
```

---

# 十一、测试目录

```text
tests/research_db/personal_profile/
  test_behavior_schema.py
  test_trade_behavior_analyzer.py
  test_edge_detector.py
  test_weakness_detector.py
  test_forbidden_pattern_miner.py
  test_setup_library_builder.py
  test_account_style_classifier.py
  test_advisory_boundary.py
  test_operator_profile_builder.py
  test_personal_profile_report.py
  test_no_production_boundary.py
```

必须测试：

```text
1. 优势必须有证据
2. 弱点必须有 case/trade refs
3. 禁止模式不得输出 BUY/SELL
4. account_style 可分类
5. advisory_boundary 阻断交易词
6. production_allowed=false
```

---

# 十二、Verify 脚本

```text
scripts/verify_research_db_phase9_personal_profile.sh
```

必须运行：

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/personal_profile/
```

并扫描交易词与 production flags。

---

# 十三、报告

```text
operator_profile_report.md
edge_map_report.md
weakness_map_report.md
forbidden_patterns_report.md
strategy_fit_report.md
personal_advisory_boundary.md
```

报告必须包含：

```text
优势领域
弱点领域
禁止交易模式
适合持有周期
适合行业/链条
不适合信号
风险预算建议
人工复核要求
```

---

# 十四、Acceptance Matrix

```text
docs/research_db/PHASE9_ACCEPTANCE_MATRIX.md
```

Final Status：

```text
PHASE9_READY_FOR_RESEARCH_COCKPIT
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十五、执行批次

```text
Batch P9-A：目录 + schema
Batch P9-B：行为分析 + edge/weakness detector
Batch P9-C：forbidden patterns + setup library
Batch P9-D：account style + advisory boundary
Batch P9-E：profile builder + reports
Batch P9-F：tests + verify
Batch P9-G：closeout
```

---

# 十六、完成报告格式

```text
## ResearchDB Phase 9 完成报告
commit:
branch:

### Directories
- normalized:
- reports:

### Code
- behavior_schema:
- trade_behavior_analyzer:
- edge_detector:
- weakness_detector:
- forbidden_pattern_miner:
- setup_library_builder:
- account_style_classifier:
- advisory_boundary:
- operator_profile_builder:
- personal_profile_report:

### Tests
- tests/research_db/personal_profile:
- verify_research_db_phase9_personal_profile.sh:

### Final Status
ResearchDB Phase 9: PASS / FAIL
Next Phase: Phase 10 Research Cockpit
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十七、最终裁决

Phase 9 的本质是：

```text
让系统认识你本人。
```

它不是选股系统，而是你的个人操盘镜子。


---

# Phase 9 A+ 额外加固项

## P9-A+ 行为指标公式卡

必须新增：

```text
docs/research_db/PHASE9_BEHAVIOR_METRIC_FORMULAS.md
```

每个行为指标必须包含：

```text
metric_id
metric_name
formula
input_tables
minimum_sample_size
quality_status
```

## P9-A+ 禁止建议输出测试

测试必须证明系统只输出：

```text
RESEARCH_SUPPORT
WATCH_ONLY
PAPER_ONLY
HUMAN_REVIEW_REQUIRED
ACTION_BLOCKED
DATA_INSUFFICIENT
```

不得输出 BUY / SELL / STRONG_BUY / AUTO_EXECUTE。

## P9-A+ 画像结论证据要求

任何 edge / weakness / forbidden_pattern 必须有：

```text
supporting_trades 或 supporting_cases
sample_size
confidence
quality_status
production_allowed=false
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
