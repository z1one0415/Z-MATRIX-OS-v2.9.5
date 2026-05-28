# Z-MATRIX-OS v3.5 → v4.0-FINAL-HARDGATES｜OpenClaw 天师执行指令

> **执行对象**：OpenClaw Z2-天师（DeepSeek-V4-Pro）  
> **起点版本**：Z-MATRIX-OS v3.5 Closeout / 当前云仓最新提交  
> **目标版本**：Z-MATRIX-OS v4.0-FINAL-HARDGATES / RC1  
> **执行原则**：代码实现 + 测试 + 文档 + 验证脚本 + 云仓提交 + 可回滚  
> **硬安全边界**：Paper-only / Human Review Required / No Real Trade / No Broker Order / No Auto Buy / No Auto Sell  
> **强制云仓要求**：每批必须 `git add`、`git commit`、`git push`，并回报 `git rev-parse HEAD`。  
> **强制验证要求**：必须以仓库代码、测试结果、验证脚本和云端 commit 为准，不得只依据日志或口头回报判断完成。  

---

## A. v4.0-FINAL-HARDGATES 三条最高硬门

本版必须吸收并落地以下三个阿喀琉斯之踵治理模块。  
它们是 v4.0 上线前硬门，不是可选增强。

### A1. ZC40 LimitBoardFillabilityGate｜一字板/涨停可成交性硬门

解决问题：

```text
系统判断突发利好正确，但 A 股次日一字涨停，真实买不到。
等能买到时，ZC35 催化已进入衰减后段，继续追入变成接力风险。
```

必须实现：

```text
LimitBoardFillabilityGate
BoardContinuationDetector
OpenBoardChaseRiskDetector
FillabilityStatus
```

输出只允许：

```text
NOT_FILLABLE
WAIT_OPEN_BOARD
OPEN_BOARD_CONFIRMATION_REQUIRED
CHASE_RISK
LIQUIDITY_TRAP
PAPER_ONLY_OBSERVE
DATA_INSUFFICIENT
```

禁止输出：

```text
BUY
AUTO_BUY
REAL_ORDER
```

---

### A2. ZC45 ProxyHedgeStressTest｜代理对冲压力测试硬门

解决问题：

```text
ZC45 代理对冲不是 Market Neutral。
红利、黄金、债券、跨境 ETF 在极端流动性危机中可能同跌。
```

必须实现：

```text
ProxyHedgeStressTest
CorrelationBreakdownDetector
LiquidityCrashScenario
DefensiveAssetStressReport
```

输出只允许：

```text
PROXY_HEDGE_EFFECTIVE
DEFENSIVE_ONLY
CORRELATION_BREAKDOWN
LIQUIDITY_CRASH_RISK
NOT_A_HEDGE
DATA_INSUFFICIENT
```

禁止输出：

```text
MARKET_NEUTRAL
ABSOLUTE_RETURN
REAL_HEDGE_ORDER
AUTO_ALLOCATE
```

---

### A3. Runtime Failover｜LLM/API 失效降级硬门

解决问题：

```text
系统高度依赖 LLM API 和外部供应商。
API 宕机、网络波动、限流、风控拦截时，IRF 管线不得胡编，不得崩溃，不得输出新判断。
```

必须实现：

```text
LLMProviderFailoverPolicy
OfflineDegradedMode
CachedFactExtractionStore
CriticalPipelineFallback
StaleDataPolicy
DegradedCloseoutReport
```

核心规则：

```text
1. LLM API 失败时，不允许生成新事实判断。
2. 允许读取最近一次已审计 FactExtraction，但必须标记 stale。
3. stale 数据不得驱动新策略结论，只能输出 DATA_INSUFFICIENT / DEGRADED。
4. IRF pipeline 不崩溃，必须生成 degraded closeout。
5. AuditTrail 必须记录 failover_trace / cache_trace / stale_data_trace。
```

---

## B. Parser-Scorer Split 最高军规

```text
LLM 负责读懂世界，Z-MATRIX 负责计算世界。
```

黑盒 LLM 不得直接输出任何主观连续型分数，包括但不限于：

```text
moat_score
risk_score
support_score
growth_score
buy_score
sell_score
conviction_score
recommendation_score
catalyst_score
event_power_score
hedge_score
defensive_score
fillability_score
expected_return
position_size
target_weight
probability_of_success
```

LLM 只允许输出：

```text
BOOL
ENUM
FACTUAL_NUMBER
DATE
TEXT_SPAN
EVIDENCE_REF
AMBIGUITY_FLAG
MISSING_EVIDENCE
CONTRADICTION_FLAG
```

所有分数必须由本地确定性代码生成：

```text
FactExtractionModel
→ FeatureNormalizer
→ DeterministicScorer
→ ScoreTrace
→ Review / Factor / Catalyst / Defensive Allocation / Execution / Report / Audit
```

---

## C. ZC35 Catalyst Lifecycle 定位

ZC35 不是追热点系统，而是 **催化生命周期与预期耗尽识别系统**。

ZC35 只输出：

```text
catalyst_status
lifecycle_state
sell_on_news_risk
residual_power
review_signal
```

不得输出买卖指令。

---

## D. ZC45 Proxy Hedge 定位

ZC45 不是做空系统，不是 Market Neutral，不是自动配置系统。

ZC45 只输出：

```text
beta_exposure
defensive_allocation_preview
hedge_proxy_suitability
tail_hedge_simulation
beta_reduction_review
human_review_required
```

不得输出真实交易或自动配置指令。

---

## E. 全局禁止项

所有批次禁止：

```text
1. 输出真实交易指令。
2. 接券商下单接口。
3. 生成 broker_order / market_order / auto_buy / auto_sell。
4. 把 paper order preview 变成真实订单。
5. 绕过 Skill Registry 直接调用新模块。
6. 把 ZC10-ZC50 / ZC35 / ZC45 做成 pipeline。
7. 删除或重写 Z-G01~G18。
8. System Cockpit 直接计算业务逻辑。
9. 只建空文件，不实现 schema、fixture、测试。
10. 把历史归因候选直接写入 production strategy。
11. 让 LLM 输出主观连续分数。
12. 让 ZC35 把已计划会议/流程事件/跨板块弱相关误当强催化。
13. 让 ZC45 自动配置 ETF、期货、期权或声称中性化。
14. 让 ZC40 在一字板不可成交状态下输出新入场。
15. LLM/API 失败时生成新判断。
```

---

## F. 每批统一完成报告格式

每批完成后必须输出：

```text
# Batch N 完成报告

## 1. 批次目标
...

## 2. 已完成内容
...

## 3. 新增/修改文件
...

## 4. 测试命令与结果
...

## 5. Verify 脚本结果
...

## 6. V40_FULL_SCOPE_ACCEPTANCE_MATRIX 更新项
...

## 7. Parser-Scorer Split 确认
- LLM_subjective_float_score_allowed=False
- deterministic_scorer_required=True
- score_trace_required=True

## 8. ZC35 确认
- catalyst_direct_trade_allowed=False
- scheduled_event_without_surprise_blocked=True
- process_event_without_result_downgraded=True
- entity_relevance_gate_enabled=True
- sell_on_news_detector_enabled=True

## 9. ZC45 确认
- market_neutral_claim_allowed=False
- defensive_allocation_auto_execute=False
- tail_hedge_real_order_allowed=False
- hedge_proxy_suitability_checked=True
- proxy_hedge_stress_test_enabled=True
- beta_budget_governor_enabled=True

## 10. ZC40 LimitBoard 确认
- one_word_limit_up_detected=True
- not_fillable_blocks_new_entry=True
- open_board_chase_risk_detected=True

## 11. Runtime Failover 确认
- llm_api_failure_no_new_judgement=True
- stale_cache_marked=True
- degraded_closeout_report_generated=True

## 12. 安全边界确认
- real_trade_allowed=False
- broker_order_allowed=False
- auto_buy_allowed=False
- auto_sell_allowed=False
- human_review_required=True

## 13. Commit SHA
...

## 14. Known Limitations
...

## 15. 下一批建议
...
```

---

# Batch 2｜Research Council + Report Library｜Parser-Scorer + Hard Gates Report Blocks

## 2.1 批次目标

本批落地：

```text
ZC10_RESEARCH_COUNCIL_12_SEATS_SKILL_PACK_V10
ZREPORT_TEMPLATE_LIBRARY_12_MAIN_8_COMPONENTS_V10
```

强制要求：

```text
Reviewer LLM 不得直接打 support_score / risk_score。
Reviewer LLM 只能输出 FactExtractionModel。
ExpertReviewModel 中的 support_score / risk_score 必须由 DeterministicScorer 生成。
报告必须展示 Fact Extraction、ScoreTrace、Scoring Config Version。
报告必须预留 ZC35 / ZC45 / LimitBoard / RuntimeFailover 区块。
```

---

## 3. Research Council 必做目录

```text
zmatrix/research_culture/research_council/
  base_models.py
  base_fact_extractor.py
  base_expert_scorer.py
  base_reviewer.py
  council_chair.py
  council_aggregator.py
  v3_payload_builder.py
  audit_report_builder.py
  user_reading_layer.py

  inversion_mental_models.py
  margin_of_safety.py
  moat_owner_earnings.py
  quality_growth_lifecycle.py
  short_seller_forensic_attack.py
  reflexivity_narrative.py
  chain_value_capture.py
  macro_liquidity_cycle.py
  factor_validity.py
  strategy_validation_overfit.py
  execution_microstructure.py
  account_survival_risk_budget.py

  scoring_configs/
    inversion_mental_models_v1.yaml
    margin_of_safety_v1.yaml
    moat_owner_earnings_v1.yaml
    quality_growth_lifecycle_v1.yaml
    short_seller_forensic_attack_v1.yaml
    reflexivity_narrative_v1.yaml
    chain_value_capture_v1.yaml
    macro_liquidity_cycle_v1.yaml
    factor_validity_v1.yaml
    strategy_validation_overfit_v1.yaml
    execution_microstructure_v1.yaml
    account_survival_risk_budget_v1.yaml
```

---

## 4. Reviewer 固定流程

每个 reviewer 必须执行：

```text
input context
→ fact extraction prompt / parser
→ FactExtractionModel
→ SubjectiveScoreBanValidator
→ FeatureNormalizer
→ DeterministicExpertScorer
→ ExpertReviewModel
→ ScoreTrace
→ AuditTrace
```

不得直接：

```text
LLM → ExpertReviewModel.support_score
LLM → ExpertReviewModel.risk_score
```

---

## 5. 12 个 Reviewer 必须完整实现

```text
01 ZC10.research_style.inversion_mental_models
02 ZC10.research_style.margin_of_safety
03 ZC10.research_style.moat_owner_earnings
04 ZC10.research_style.quality_growth_lifecycle
05 ZC10.research_style.short_seller_forensic_attack
06 ZC10.research_style.reflexivity_narrative
07 ZC10.research_style.chain_value_capture
08 ZC10.research_style.macro_liquidity_cycle
09 ZC10.research_style.factor_validity
10 ZC10.research_style.strategy_validation_overfit
11 ZC10.research_style.execution_microstructure
12 ZC10.research_style.account_survival_risk_budget
```

每个 reviewer 必须包含：

```text
METHODOLOGY_KERNEL
FACT_FIELDS
ALLOWED_ENUMS
REQUIRED_EVIDENCE
AMBIGUITY_POLICY
SCORING_CONFIG
FIXTURE_INPUT
EXPECTED_FACTS
EXPECTED_REVIEW_STATUS
```

---

## 6. Report Library 必做模块

```text
zmatrix/reports/base_models.py
zmatrix/reports/template_registry.py
zmatrix/reports/render_context.py
zmatrix/reports/report_generator.py
zmatrix/reports/missing_field_policy.py
zmatrix/reports/safety_disclaimer.py
zmatrix/reports/snapshot_tester.py
zmatrix/reports/parser_scorer_blocks.py
zmatrix/reports/catalyst_blocks.py
zmatrix/reports/defensive_allocation_blocks.py
zmatrix/reports/limit_board_blocks.py
zmatrix/reports/failover_blocks.py
```

---

## 7. 12 主模板

```text
single_stock_research_report.md
research_council_review_report.md
evidence_data_quality_report.md
strategy_validation_report.md
factor_validation_report.md
multi_strategy_portfolio_report.md
paper_execution_plan_report.md
execution_route_competition_report.md
portfolio_alpha_daily_report.md
account_risk_weekly_report.md
missed_opportunity_postmortem_report.md
audit_trail_report.md
```

每个模板必须增加区块：

```text
Fact Extraction Table
Scoring Trace Table
Scoring Config Version
Parser Model Version
Prompt Version
Subjective Score Ban Status
Catalyst Lifecycle Section
Defensive Allocation Section
Beta Exposure Section
LimitBoard Fillability Section
Runtime Failover / Data Freshness Section
Risk Disclosure
Audit Metadata
```

---

## 8. 组件模板

```text
component_domain_state_matrix.md
component_research_council_summary.md
component_evidence_cards.md
component_risk_disclosure.md
component_action_downgrade.md
component_account_constraints.md
component_alpha_attribution.md
component_audit_metadata.md
component_fact_extraction_table.md
component_score_trace_table.md
component_parser_scorer_disclosure.md
component_catalyst_lifecycle_summary.md
component_defensive_allocation_summary.md
component_beta_exposure_summary.md
component_limit_board_fillability_summary.md
component_runtime_failover_summary.md
```

---

## 9. 必须新增测试

```text
tests/research_council/test_all_reviewers_fact_extraction.py
tests/research_council/test_reviewer_subjective_score_ban.py
tests/research_council/test_reviewer_deterministic_scoring.py
tests/research_council/test_reviewer_score_trace.py
tests/research_council/test_research_council_aggregator.py
tests/research_council/test_research_council_v3_payload.py

tests/reports/test_template_registry.py
tests/reports/test_report_generator.py
tests/reports/test_report_parser_scorer_blocks.py
tests/reports/test_report_catalyst_blocks.py
tests/reports/test_report_defensive_allocation_blocks.py
tests/reports/test_report_limit_board_blocks.py
tests/reports/test_report_failover_blocks.py
tests/reports/test_report_missing_field_policy.py
tests/reports/test_report_safety_disclosure.py
tests/reports/test_report_snapshot_all_templates.py
```

---

## 10. 测试命令

```bash
python -m compileall zmatrix tests scripts

pytest -q tests/research_council/
pytest -q tests/reports/

bash scripts/verify_v40_guardrails.sh
bash scripts/verify_v40_parser_scorer_split.sh
bash scripts/verify_v40_zc35_catalyst_guardrails.sh
bash scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
bash scripts/verify_v40_final_hardgates.sh
```

---

## 11. 提交

```bash
git status --short
git add .
git commit -m "v4.0-batch-2: add research council reports and final hard gate blocks"
git push
git rev-parse HEAD
```

---

## 12. 验收标准

```text
1. 12 个 reviewer 全部实现。
2. 12 个 reviewer 不让 LLM 输出主观连续分数。
3. 每个 reviewer 先提取事实，再本地评分。
4. 每个 reviewer 产生 ScoreTrace。
5. CouncilAggregator 本地聚合。
6. 报告模板展示 fact extraction 与 score trace。
7. 报告模板支持 ZC35/ZC45/LimitBoard/Failover 区块。
8. Missing field 显性 degraded。
9. 风险声明强制出现。
10. pytest 全过。
11. 五条 verify 全过。
12. 云仓 commit 可验证。
```
