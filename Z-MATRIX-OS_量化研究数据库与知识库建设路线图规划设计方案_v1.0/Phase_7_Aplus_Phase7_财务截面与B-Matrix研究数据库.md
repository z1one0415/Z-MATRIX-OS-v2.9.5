# Phase 7：财务截面与 B-Matrix 研究数据库｜A+加固执行版

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

# Phase 7：财务截面与 B-Matrix 研究数据库

> **所属总路线**：Z-MATRIX-OS｜量化研究数据库与知识库建设路线图  
> **阶段编号**：Phase 7  
> **阶段名称**：Financial Snapshot & B-Matrix Research DB｜财务截面与 B-Matrix 研究数据库  
> **前置阶段**：Phase 0–6  
> **执行对象**：OpenClaw 天师 / deepseek-v4-pro  
> **阶段性质**：财务截面 / 估值截面 / 行业分位 / 数据新鲜度 / Parser-Scorer Split / B-Matrix 研究因子  
> **硬边界**：Research Only / Paper Only / No Broker / No Runtime / No Real Trade / No Production

---

## 0. 总裁决

Phase 7 的目标是把 B-Matrix 从“主观基本面判断”升级为：

```text
财务字段可追溯
估值字段可比较
行业分位可计算
数据新鲜度可审计
LLM 只抽事实
Python/YAML 负责确定性评分
```

本阶段优先做：

```text
current financial snapshot
```

不强行伪造历史 PIT 财务库。

如果没有历史 PIT 数据，必须标记：

```text
CURRENT_SNAPSHOT_ONLY
BLOCKED_FOR_BACKTEST
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
data/research_db/finance/
  README.md

  raw/
    financial_imports/
    valuation_imports/
    manual_finance/
    .gitkeep

  staging/
    imported_financial_raw.csv
    imported_valuation_raw.csv
    import_error_rows.csv

  normalized/
    financial_snapshot.csv
    valuation_snapshot.csv
    industry_percentile.csv
    financial_freshness.csv
    b_matrix_current_snapshot.csv
    b_matrix_fact_extraction.jsonl
    b_matrix_score_trace.jsonl
    b_matrix_quality_ledger.csv

  reports/
    financial_snapshot_report.md
    valuation_snapshot_report.md
    b_matrix_current_snapshot_report.md
    financial_freshness_report.md
    b_matrix_data_quality_report.md
```

---

# 二、代码模块

```text
zmatrix/research_db/b_matrix/
  __init__.py
  financial_schema.py
  valuation_schema.py
  freshness_policy.py
  industry_percentile.py
  fact_extraction_contract.py
  deterministic_scorer.py
  b_matrix_snapshot_builder.py
  b_matrix_quality_checker.py
  b_matrix_report.py
```

---

# 三、财务字段

## 3.1 financial_snapshot.csv

```csv
ticker,name,report_date,as_of_date,roe,gross_margin,net_margin,revenue_growth,net_profit_growth,operating_cashflow,debt_ratio,asset_turnover,inventory_turnover,receivables_turnover,capex,rd_expense,source,pit_status,freshness_status,quality_status
```

## 3.2 valuation_snapshot.csv

```csv
ticker,name,date,pe,pb,ps,pcf,ev_ebitda,dividend_yield,market_cap,total_market_cap,float_market_cap,source,pit_status,quality_status
```

## 3.3 industry_percentile.csv

```csv
ticker,name,date,industry_l1,industry_l2,metric,metric_value,percentile,rank,total_count,quality_status
```

## 3.4 financial_freshness.csv

```csv
ticker,name,latest_report_date,days_since_report,freshness_status,stale_reason,quality_status
```

freshness_status：

```text
FRESH
AGING
STALE
MISSING
```

---

# 四、B-Matrix 当前截面

## 4.1 b_matrix_current_snapshot.csv

```csv
ticker,name,date,quality_bucket,growth_bucket,valuation_bucket,cashflow_bucket,balance_sheet_bucket,industry_percentile_bucket,data_status,pit_status,production_allowed,quality_status
```

## 4.2 b_matrix_fact_extraction.jsonl

LLM 只允许抽取：

```text
bool
enum
number
evidence_refs
source_quote_short
```

禁止输出：

```text
连续主观分数
BUY
SELL
STRONG_BUY
```

## 4.3 b_matrix_score_trace.jsonl

确定性评分必须记录：

```json
{
  "ticker": "300763.SZ",
  "score_id": "BM-20260601-001",
  "input_facts": {},
  "rules_applied": [],
  "score_components": {},
  "final_bucket": "WATCH",
  "production_allowed": false
}
```

---

# 五、Parser-Scorer Split

## 5.1 LLM 只做 Parser

允许：

```json
{
  "rd_growth_positive": true,
  "high_client_concentration": false,
  "cashflow_quality": "PARTIAL",
  "evidence_refs": []
}
```

禁止：

```json
{
  "moat_score": 8.5,
  "buy_score": 9.0
}
```

## 5.2 Scorer 由代码/YAML 决定

```python
def calculate_quality_bucket(facts: dict, metrics: dict, config: dict) -> dict:
    ...
```

必须输出 score_trace。

---

# 六、PIT 规则

```text
当前截面数据：CURRENT_SNAPSHOT_ONLY
无 as_of_date：UNKNOWN_PIT_STATUS
as_of_date > trade_date：BLOCKED_FOR_BACKTEST
历史 PIT 数据缺失：不得做历史 B-Matrix 回测
```

---

# 七、第一批 B 因子

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
financial_freshness
```

这些字段将进入 Phase 4 FactorFactory，但如果是 current snapshot，则只可用于当前截面研究。

---

# 八、测试目录

```text
tests/research_db/b_matrix/
  test_financial_schema.py
  test_valuation_schema.py
  test_freshness_policy.py
  test_industry_percentile.py
  test_fact_extraction_contract.py
  test_deterministic_scorer.py
  test_b_matrix_snapshot_builder.py
  test_b_matrix_quality_checker.py
  test_b_matrix_report.py
  test_no_production_boundary.py
```

必须测试：

```text
1. 缺 report_date → quality_status=ERROR
2. current snapshot 不得进入 historical backtest
3. LLM score 字段被阻断
4. bool/enum facts 允许
5. deterministic scorer 输出 score_trace
6. production_allowed=false
```

---

# 九、Verify 脚本

```text
scripts/verify_research_db_phase7_b_matrix.sh
```

必须运行：

```bash
python -m compileall zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/b_matrix/
```

并扫描：

```text
moat_score
buy_score
strong_buy
real_trade_allowed=True
production_allowed=True
```

业务输出不得出现。

---

# 十、报告

```text
financial_snapshot_report.md
valuation_snapshot_report.md
b_matrix_current_snapshot_report.md
financial_freshness_report.md
b_matrix_data_quality_report.md
```

报告必须写明：

```text
当前截面覆盖率
缺失财务字段
行业分位覆盖率
fresh/stale/missing 数量
CURRENT_SNAPSHOT_ONLY 数量
BLOCKED_FOR_BACKTEST 数量
```

---

# 十一、Acceptance Matrix

```text
docs/research_db/PHASE7_ACCEPTANCE_MATRIX.md
```

Final Status：

```text
PHASE7_READY_FOR_INDUSTRY_CHAIN_KNOWLEDGE_BASE
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十二、执行批次

```text
Batch P7-A：目录 + finance/valuation schema
Batch P7-B：freshness + industry percentile
Batch P7-C：fact extraction contract + deterministic scorer
Batch P7-D：B-Matrix snapshot builder + quality checker
Batch P7-E：reports + tests + verify
Batch P7-F：closeout
```

---

# 十三、完成报告格式

```text
## ResearchDB Phase 7 完成报告
commit:
branch:

### Directories
- raw:
- staging:
- normalized:
- reports:

### Code
- financial_schema:
- valuation_schema:
- freshness_policy:
- industry_percentile:
- fact_extraction_contract:
- deterministic_scorer:
- b_matrix_snapshot_builder:
- b_matrix_quality_checker:
- b_matrix_report:

### Tests
- tests/research_db/b_matrix:
- verify_research_db_phase7_b_matrix.sh:

### Final Status
ResearchDB Phase 7: PASS / FAIL
Next Phase: Phase 8 Industry & Chain Knowledge Base
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
```

---

# 十四、最终裁决

Phase 7 的本质是：

```text
把 B-Matrix 从“看基本面”升级为“可审计的财务截面研究系统”。
```


---

# Phase 7 A+ 额外加固项

## P7-A+ Scorer YAML 配置

必须新增：

```text
configs/b_matrix/scoring_rules.yaml
configs/b_matrix/freshness_rules.yaml
configs/b_matrix/parser_contract.schema.json
```

所有分数必须来自 deterministic scorer + YAML。禁止 LLM 直接输出连续评分。

## P7-A+ Parser Contract Fixture

必须新增：

```text
tests/fixtures/b_matrix/parser_valid_bool_enum.json
tests/fixtures/b_matrix/parser_invalid_subjective_score.json
```

测试必须证明：

```text
moat_score / buy_score / growth_score 被阻断。
bool / enum / evidence_refs 通过。
```

## P7-A+ Score Trace 必填字段

每个 deterministic scorer 输出必须包含：

```text
score_id
input_facts
input_metrics
rules_applied
score_components
final_bucket
blocked_reasons
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
