# Phase 8：产业链/行业知识库｜A+加固执行版

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

# Phase 8：产业链/行业知识库

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 8  
> **阶段名称**：Industry & Chain Knowledge Base｜产业链/行业知识库  
> **前置阶段**：Phase 0–7  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：31 行业骨架 / 高频产业链深研 / 公司映射 / 假信号库 / 知识新鲜度 / 与因子/案例互联  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 8 不是写 31 份行业百科。

正确目标是：

```text
建立可被系统引用、可被案例验证、可被因子回测、可持续更新的行业/产业链知识库。
```

执行策略：

```text
31 行业先做骨架卡；
8 条高频主线先做深研；
深研必须连接股票、财务、事件、因子和案例；
知识必须有 freshness_status。
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

# 一、知识库目录

```text
data/research_db/knowledge/
  methodology/
    industry_research_method.md
    chain_mapping_method.md
    false_signal_method.md

  industries/
    industry_card_template.md
    sw_l1_index.md
    cards/
      .gitkeep

  chains/
    chain_card_template.md
    high_frequency_chains.md
    cards/
      .gitkeep

  company_profiles/
    company_profile_template.md
    .gitkeep

  false_signal_library/
    false_signal_taxonomy.md
    sell_on_news_patterns.md
    concept_trap_patterns.md
    financial_mismatch_patterns.md

  reports/
    industry_coverage_report.md
    chain_coverage_report.md
    knowledge_freshness_report.md
    false_signal_report.md
```

---

# 二、代码模块

```text
zmatrix/research_db/knowledge/
  __init__.py
  industry_card_schema.py
  chain_card_schema.py
  company_profile_schema.py
  false_signal_schema.py
  knowledge_loader.py
  knowledge_linker.py
  freshness_checker.py
  chain_company_mapper.py
  false_signal_matcher.py
  knowledge_report.py
```

---

# 三、31 行业骨架卡

每个行业卡：

```yaml
industry_id:
industry_name:
classification_system:
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
case_refs:
factor_refs:
freshness_status:
updated_at:
production_allowed: false
```

cycle_type：

```text
GROWTH
CYCLICAL
DEFENSIVE
FINANCIAL
RESOURCE
CONSUMPTION
TECHNOLOGY
MIXED
```

---

# 四、首批 8 条高频主线深研

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

每条链必须有：

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

---

# 五、产业链卡模板

```yaml
chain_id:
chain_name:
chain_definition:
upstream:
midstream:
downstream:
bottleneck_nodes:
value_capture_nodes:
listed_companies:
benchmark_basket:
key_financial_metrics:
key_catalysts:
common_false_signals:
case_refs:
factor_refs:
event_refs:
freshness_status:
updated_at:
production_allowed: false
```

---

# 六、公司画像模板

```yaml
ticker:
name:
industry_l1:
industry_l2:
chain_id:
chain_position:
value_capture_grade:
business_relevance:
financial_validation:
key_products:
key_customers:
key_risks:
related_cases:
related_factors:
related_events:
freshness_status:
production_allowed: false
```

---

# 七、假信号库

必须维护：

```text
SELL_ON_NEWS
CONCEPT_ONLY
FINANCIAL_MISMATCH
MARGIN_COMPRESSION
CHANNEL_INVENTORY
POLICY_EXPECTATION_OVERPRICED
SCHEDULED_EVENT_TRAP
NARRATIVE_DECAY
CROWDING_REVERSAL
EXECUTION_NOT_FILLABLE
```

每个模式必须定义：

```text
pattern_id
pattern_name
trigger_conditions
evidence_required
related_cases
module_attribution
avoidance_rule_candidate
promotion_allowed=false
```

---

# 八、知识新鲜度

freshness_status：

```text
FRESH
AGING
STALE
MISSING
REVIEW_REQUIRED
```

规则：

```text
行业卡超过 90 天未更新 → AGING
超过 180 天未更新 → STALE
高波动行业超过 30 天未更新 → AGING
事件密集行业必须月度更新
```

---

# 九、知识互联

knowledge_linker 必须支持：

```text
industry → chain
chain → company
company → case
case → factor
factor → event
event → industry
```

输出：

```json
{
  "node_id": "",
  "node_type": "CHAIN",
  "linked_cases": [],
  "linked_factors": [],
  "linked_events": [],
  "production_allowed": false
}
```

---

# 十、测试目录

```text
tests/research_db/knowledge/
  test_industry_card_schema.py
  test_chain_card_schema.py
  test_company_profile_schema.py
  test_false_signal_schema.py
  test_knowledge_loader.py
  test_knowledge_linker.py
  test_freshness_checker.py
  test_chain_company_mapper.py
  test_false_signal_matcher.py
  test_knowledge_report.py
  test_no_production_boundary.py
```

必须测试：

```text
1. 行业卡字段完整
2. 产业链卡字段完整
3. 公司画像必须链接 chain_position
4. 假信号模式必须有 evidence_required
5. freshness 超期变 STALE
6. 链接 case/factor/event 可追溯
7. production_allowed=false
```

---

# 十一、Verify 脚本

```text
scripts/verify_research_db_phase8_knowledge_base.sh
```

必须运行：

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/knowledge/
```

并检查：

```text
industries/cards 目录存在
chains/cards 目录存在
false_signal_library 存在
所有知识卡 production_allowed=false
```

---

# 十二、报告

```text
industry_coverage_report.md
chain_coverage_report.md
knowledge_freshness_report.md
false_signal_report.md
```

报告必须包含：

```text
31 行业骨架完成率
8 高频主线完成率
过期知识卡数量
假信号库覆盖数量
已链接案例数量
已链接因子数量
```

---

# 十三、Acceptance Matrix

```text
docs/research_db/PHASE8_ACCEPTANCE_MATRIX.md
```

Final Status：

```text
PHASE8_READY_FOR_PERSONAL_OPERATOR_PROFILE
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十四、执行批次

```text
Batch P8-A：目录 + 模板
Batch P8-B：行业卡 schema + 31行业骨架索引
Batch P8-C：产业链卡 schema + 8主线模板
Batch P8-D：公司画像 + 假信号库
Batch P8-E：freshness + linker + reports
Batch P8-F：tests + verify
Batch P8-G：closeout
```

---

# 十五、完成报告格式

```text
## ResearchDB Phase 8 完成报告
commit:
branch:

### Knowledge Directories
- methodology:
- industries:
- chains:
- company_profiles:
- false_signal_library:

### Code
- industry_card_schema:
- chain_card_schema:
- company_profile_schema:
- false_signal_schema:
- knowledge_loader:
- knowledge_linker:
- freshness_checker:
- chain_company_mapper:
- false_signal_matcher:
- knowledge_report:

### Tests
- tests/research_db/knowledge:
- verify_research_db_phase8_knowledge_base.sh:

### Final Status
ResearchDB Phase 8: PASS / FAIL
Next Phase: Phase 9 Personal Operator Profile
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十六、最终裁决

Phase 8 的本质是：

```text
把行业知识从静态文章，升级为可被系统引用和验证的研究知识图谱。
```


---

# Phase 8 A+ 额外加固项

## P8-A+ 31 行业骨架最小完成定义

不能只建空目录。每个行业卡至少必须填：

```text
industry_id
industry_name
cycle_type
benchmark_index
representative_stocks
main_drivers
common_traps
freshness_status
production_allowed=false
```

## P8-A+ 8 条主线深研最小完成定义

每条 chain card 至少必须填：

```text
chain_id
chain_name
upstream/midstream/downstream
bottleneck_nodes
listed_companies
benchmark_basket
common_false_signals
case_refs
factor_refs
freshness_status
```

## P8-A+ Knowledge Linker Golden Test

必须用一个虚构链条证明：

```text
chain → company → case → factor → event
```

全链可追溯。


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
