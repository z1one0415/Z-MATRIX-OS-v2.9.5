# Phase 10：Research Cockpit 与月度内化机制｜A+加固执行版

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

# Phase 10：Research Cockpit 与月度内化机制

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 10  
> **阶段名称**：Research Cockpit & Monthly Internalization Loop｜研究驾驶舱与月度内化机制  
> **前置阶段**：Phase 0–9  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：日/周/月运行机制 / 研究驾驶舱 / 系统学习报告 / 规则候选治理 / 个人操盘建议闭环  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 10 的目标是把前 9 个阶段从“数据库工程”变成“持续运行的研究操作系统”。

核心不是新模块，而是机制：

```text
每日自动收集
每周自动复盘
每月自动内化
季度人工裁决
```

系统输出：

```text
Research Cockpit
Monthly Memory Report
System Learning Report
Rule Candidate Governance
Operator Profile Update
```

禁止输出：

```text
自动交易指令
broker order
production signal
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
data/research_db/cockpit/
  README.md

  daily/
    daily_run_log.jsonl
    daily_review_queue.md
    daily_system_status.json

  weekly/
    weekly_case_report.md
    weekly_error_heatmap.md
    weekly_outcome_report.md
    weekly_factor_watch.md

  monthly/
    monthly_memory_report.md
    monthly_system_learning_report.md
    monthly_operator_profile_update.md
    monthly_rule_candidate_governance.md
    monthly_research_priority.md

  quarterly/
    quarterly_strategy_review.md
    quarterly_factor_review.md
    quarterly_knowledge_freshness_review.md

  dashboard/
    cockpit_snapshot.json
    cockpit_summary.md
```

---

# 二、代码模块

```text
zmatrix/research_db/cockpit/
  __init__.py
  daily_runner.py
  weekly_closeout.py
  monthly_internalizer.py
  quarterly_reviewer.py
  cockpit_snapshot_builder.py
  rule_candidate_governor.py
  memory_report_builder.py
  system_learning_report.py
  research_priority_engine.py
  cockpit_report.py
```

---

# 三、每日流程

`daily_runner.py` 必须执行：

```text
1. 检查输入数据 freshness
2. 更新 watchlist/holdings/prices
3. 运行 AutoCaseForge daily
4. 更新 outcome 到期项
5. 生成 daily_review_queue.md
6. 生成 cockpit_snapshot.json
```

每日输出：

```text
新增事件数
新增 case draft
待人工确认 case
到期 outcome
数据缺失清单
系统冲突清单
```

---

# 四、每周流程

`weekly_closeout.py` 必须执行：

```text
1. 关闭到期 case
2. 更新 T5/T20/T60
3. 生成 weekly_case_report
4. 生成 weekly_error_heatmap
5. 生成 weekly_outcome_report
6. 更新 factor_watch
```

每周报告必须包含：

```text
新增案例
关闭案例
错判案例
命中案例
错过机会
执行失败
账户 alpha
错误模块分布
```

---

# 五、每月流程

`monthly_internalizer.py` 必须执行：

```text
1. 读取 CaseForge 月度案例
2. 读取 FactorFactory 验证结果
3. 读取 ZC35 催化结果
4. 读取账户 alpha
5. 更新个人操盘画像
6. 生成 monthly_memory_report
7. 生成 rule_candidate_governance
8. 输出下月研究优先级
```

---

# 六、月度内化报告

`monthly_memory_report.md` 必须包含：

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
本月系统记忆候选
下月研究优先级
```

---

# 七、规则候选治理

`rule_candidate_governor.py` 必须坚持：

```text
单案例 → LESSON_ONLY
3 同类案例 → RULE_CANDIDATE
10 跨标的 → RESEARCH_RULE_CANDIDATE
20 跨标的 + 2 regime → PAPER_RULE_CANDIDATE
任何情况 production_allowed=false
```

输出：

```text
PROMOTE_TO_RESEARCH_CANDIDATE
KEEP_WATCHING
REJECT
RETIRE
INSUFFICIENT_CASES
```

禁止：

```text
AUTO_PROMOTE_TO_PRODUCTION
```

---

# 八、Research Cockpit Snapshot

`cockpit_snapshot.json` 必须包含：

```json
{
  "date": "",
  "system_status": "RESEARCH_ONLY",
  "data_freshness": {},
  "account_status": {},
  "caseforge_status": {},
  "factor_status": {},
  "zc35_status": {},
  "knowledge_status": {},
  "operator_profile_status": {},
  "pending_human_reviews": [],
  "production_allowed": false
}
```

---

# 九、研究优先级引擎

`research_priority_engine.py` 必须根据：

```text
亏损贡献
错过机会金额
案例重复频率
因子不确定性
知识过期程度
当前持仓风险
```

输出下月优先级：

```text
P0 必须修
P1 应研究
P2 可观察
P3 暂缓
```

---

# 十、测试目录

```text
tests/research_db/cockpit/
  test_daily_runner.py
  test_weekly_closeout.py
  test_monthly_internalizer.py
  test_quarterly_reviewer.py
  test_cockpit_snapshot_builder.py
  test_rule_candidate_governor.py
  test_memory_report_builder.py
  test_system_learning_report.py
  test_research_priority_engine.py
  test_cockpit_report.py
  test_no_production_boundary.py
```

必须测试：

```text
1. daily 生成 review queue
2. weekly 生成 error heatmap
3. monthly 生成 memory report
4. rule candidate 不自动 production
5. cockpit_snapshot production_allowed=false
6. priority engine 输出 P0/P1/P2/P3
7. 无 BUY/SELL/AUTO_EXECUTE
```

---

# 十一、调度脚本

```text
scripts/researchdb_daily_run.sh
scripts/researchdb_weekly_closeout.sh
scripts/researchdb_monthly_internalization.sh
scripts/researchdb_quarterly_review.sh
scripts/verify_research_db_phase10_cockpit.sh
```

注意：

```text
scheduler 只作为命令编排，不做后台常驻服务。
不得创建 daemon。
不得开启 runtime_enabled。
```

---

# 十二、Verify 脚本

必须运行：

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/cockpit/
bash scripts/researchdb_daily_run.sh
bash scripts/researchdb_weekly_closeout.sh
bash scripts/researchdb_monthly_internalization.sh
```

并扫描 forbidden flags。

---

# 十三、报告要求

```text
cockpit_summary.md
monthly_system_learning_report.md
monthly_rule_candidate_governance.md
monthly_research_priority.md
quarterly_strategy_review.md
```

必须标明：

```text
Research Only
Paper Only
Production BLOCKED
Broker/runtime BLOCKED
Real trade BLOCKED
Human review required
```

---

# 十四、Acceptance Matrix

```text
docs/research_db/PHASE10_ACCEPTANCE_MATRIX.md
```

Final Status：

```text
RESEARCH_DB_OPERATING_SYSTEM_READY
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十五、执行批次

```text
Batch P10-A：目录 + cockpit schema
Batch P10-B：daily runner + snapshot
Batch P10-C：weekly closeout
Batch P10-D：monthly internalizer + memory report
Batch P10-E：rule candidate governor + priority engine
Batch P10-F：scripts + tests + verify
Batch P10-G：closeout
```

---

# 十六、完成报告格式

```text
## ResearchDB Phase 10 完成报告
commit:
branch:

### Directories
- daily:
- weekly:
- monthly:
- quarterly:
- dashboard:

### Code
- daily_runner:
- weekly_closeout:
- monthly_internalizer:
- quarterly_reviewer:
- cockpit_snapshot_builder:
- rule_candidate_governor:
- memory_report_builder:
- system_learning_report:
- research_priority_engine:
- cockpit_report:

### Tests
- tests/research_db/cockpit:
- verify_research_db_phase10_cockpit.sh:

### Final Status
ResearchDB Phase 10: PASS / FAIL
ResearchDB Operating System: READY / BLOCKED
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十七、最终成功标准

Phase 10 完成后，系统必须能：

```text
1. 每日生成 review_queue
2. 每周生成 case/outcome/error 报告
3. 每月生成 memory report
4. 每月更新 operator profile
5. 每月输出 research priority
6. 持续维护 rule candidate queue
7. 保持 production/broker/runtime 全部 BLOCKED
```

---

# 十八、最终裁决

Phase 10 的本质是：

```text
把 Z-MATRIX-OS 从“研究数据库”升级为“持续学习的个人研究操作系统”。
```

完成 Phase 10 后，系统进入长期运行模式：

```text
每日留痕
每周复盘
每月内化
季度裁决
长期进化
```

但仍然坚持：

```text
系统给研究建议；
人做最终裁决；
broker/runtime/production 永远由硬门控制。
```


---

# Phase 10 A+ 额外加固项

## P10-A+ CLI 固定契约

每日脚本必须支持：

```bash
bash scripts/researchdb_daily_run.sh --date YYYY-MM-DD --mode paper
```

每周脚本：

```bash
bash scripts/researchdb_weekly_closeout.sh --week YYYY-WW --mode paper
```

每月脚本：

```bash
bash scripts/researchdb_monthly_internalization.sh --month YYYY-MM --mode paper
```

任何 `--mode production` 必须直接失败。

## P10-A+ Cockpit Snapshot Schema

必须新增：

```text
configs/cockpit/cockpit_snapshot.schema.json
```

字段必须包含：

```text
date
system_status
data_freshness
pending_human_reviews
caseforge_status
factor_status
zc35_status
knowledge_status
operator_profile_status
production_allowed=false
```

## P10-A+ Monthly Internalization Gate

月度内化不得自动修改规则状态。只能输出：

```text
PROMOTE_RECOMMENDED
KEEP_WATCHING
REJECT_RECOMMENDED
INSUFFICIENT_EVIDENCE
```

最终裁决必须人工确认。


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
