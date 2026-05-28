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

# Batch 5｜System Cockpit + Audit + IRF + Final Hard Gates + v4.0-RC1

## 5.1 批次目标

本批完成 v4.0-FINAL-HARDGATES 收口：

```text
1. System Cockpit
2. Audit Export Pack
3. Parser-Scorer Health Panels
4. CatalystLifecyclePanel
5. DefensiveAllocationPanel
6. BetaExposurePanel
7. LimitBoardFillabilityPanel
8. ProxyHedgeStressPanel
9. LLMFailoverPanel
10. FinalHardGatesPanel
11. Z-IRF-01~08
12. verify_v40_full_upgrade.sh
13. v4.0-RC1 release
```

本批不得重写前面业务模块，只做聚合、审计、导出、总管线和发布。

---

## 2. System Cockpit 必做模块

```text
zmatrix/system_cockpit/scenario_router.py
zmatrix/system_cockpit/domain_state_matrix.py
zmatrix/system_cockpit/pipeline_health.py
zmatrix/system_cockpit/skill_coverage.py
zmatrix/system_cockpit/data_health_panel.py
zmatrix/system_cockpit/strategy_scoreboard.py
zmatrix/system_cockpit/execution_gate_panel.py
zmatrix/system_cockpit/account_risk_panel.py
zmatrix/system_cockpit/portfolio_alpha_cockpit.py
zmatrix/system_cockpit/daily_review_command_center.py
zmatrix/system_cockpit/research_council_panel.py
zmatrix/system_cockpit/factor_factory_panel.py
zmatrix/system_cockpit/multi_strategy_sleeve_panel.py
zmatrix/system_cockpit/proprietary_data_panel.py
zmatrix/system_cockpit/audit_export_panel.py
zmatrix/system_cockpit/report_center_panel.py
zmatrix/system_cockpit/async_pipeline_health_panel.py
zmatrix/system_cockpit/schema_validation_failure_panel.py
zmatrix/system_cockpit/llm_call_budget_panel.py
zmatrix/system_cockpit/rate_limit_panel.py
zmatrix/system_cockpit/portfolio_risk_overlay_panel.py
zmatrix/system_cockpit/parser_scorer_health_panel.py
zmatrix/system_cockpit/subjective_score_violation_panel.py
zmatrix/system_cockpit/score_drift_panel.py
zmatrix/system_cockpit/catalyst_lifecycle_panel.py
zmatrix/system_cockpit/catalyst_exhaustion_panel.py
zmatrix/system_cockpit/defensive_allocation_panel.py
zmatrix/system_cockpit/beta_exposure_panel.py
zmatrix/system_cockpit/proxy_hedge_suitability_panel.py
zmatrix/system_cockpit/proxy_hedge_stress_panel.py
zmatrix/system_cockpit/limit_board_fillability_panel.py
zmatrix/system_cockpit/llm_failover_panel.py
zmatrix/system_cockpit/final_hardgates_panel.py
```

---

## 3. System Cockpit 硬规则

```text
1. 只聚合状态。
2. 不直接计算业务。
3. 不绕过 Registry。
4. 输出 OutputEnvelope。
5. 每次输出挂 AuditEvent。
6. 展示 Parser-Scorer 状态。
7. 展示 Subjective Score Violation。
8. 展示 CatalystLifecycle 状态。
9. 展示 Sell-on-News Risk 与 Catalyst Vacuum。
10. 展示 Beta Exposure 与 Defensive Allocation Preview。
11. 展示 Proxy Hedge Stress，不得称为 Market Neutral。
12. 展示 LimitBoard Fillability。
13. 展示 LLM Failover / Degraded 状态。
```

---

## 4. Audit Export Pack 必做模块

```text
zmatrix/system_cockpit/audit_event.py
zmatrix/system_cockpit/input_snapshot.py
zmatrix/system_cockpit/data_lineage_record.py
zmatrix/system_cockpit/skill_call_trace.py
zmatrix/system_cockpit/pipeline_run_trace.py
zmatrix/system_cockpit/domain_state_snapshot.py
zmatrix/system_cockpit/gate_trace.py
zmatrix/system_cockpit/decision_snapshot.py
zmatrix/system_cockpit/human_approval_record.py
zmatrix/system_cockpit/report_snapshot.py
zmatrix/system_cockpit/output_envelope_hash.py
zmatrix/system_cockpit/hash_chain.py
zmatrix/system_cockpit/safety_manifest.py
zmatrix/system_cockpit/version_manifest.py
zmatrix/system_cockpit/audit_trail.py
zmatrix/system_cockpit/audit_export_pack.py
zmatrix/system_cockpit/audit_markdown_renderer.py
zmatrix/system_cockpit/audit_csv_exporter.py
zmatrix/system_cockpit/audit_zip_exporter.py
zmatrix/system_cockpit/forbidden_output_scan.py
zmatrix/system_cockpit/parser_scorer_audit_trace.py
zmatrix/system_cockpit/catalyst_audit_trace.py
zmatrix/system_cockpit/proxy_hedge_audit_trace.py
zmatrix/system_cockpit/limit_board_audit_trace.py
zmatrix/system_cockpit/failover_audit_trace.py
zmatrix/system_cockpit/v3_audit_payload.py
```

---

## 5. AuditTrail 必须额外记录

```text
fact_extraction_trace
subjective_score_ban_trace
deterministic_scoring_trace
score_trace_hash
scoring_config_version
feature_schema_version
parser_model_version
prompt_version
schema_validation_trace
structured_output_repair_trace
llm_retry_trace
rate_limit_trace
async_node_trace
portfolio_risk_overlay_trace
regime_candidate_quarantine_trace
catalyst_event_trace
catalyst_score_trace
catalyst_decay_trace
sell_on_news_trace
catalyst_exhaustion_trace
beta_exposure_trace
defensive_allocation_preview_trace
hedge_proxy_suitability_trace
proxy_hedge_stress_trace
tail_hedge_simulation_trace
beta_budget_governor_trace
limit_board_fillability_trace
llm_provider_failover_trace
cached_fact_extraction_trace
stale_data_policy_trace
degraded_closeout_trace
```

---

## 6. ExportBundle ZIP 结构

```text
manifest.json
audit_trail.json
audit_report.md
rendered_report.md
output_envelope.json
csv/
  skill_call_trace.csv
  pipeline_run_trace.csv
  gate_trace.csv
  domain_state_snapshot.csv
  evidence_cards.csv
  data_sources.csv
  fact_extraction_trace.csv
  deterministic_scoring_trace.csv
  subjective_score_ban_trace.csv
  catalyst_event_trace.csv
  catalyst_decay_trace.csv
  sell_on_news_trace.csv
  beta_exposure_trace.csv
  defensive_allocation_preview_trace.csv
  hedge_proxy_suitability_trace.csv
  proxy_hedge_stress_trace.csv
  limit_board_fillability_trace.csv
  llm_provider_failover_trace.csv
  stale_data_policy_trace.csv
  schema_validation_trace.csv
  rate_limit_trace.csv
metadata/
  hash_chain.json
  version_manifest.json
  safety_manifest.json
  parser_scorer_manifest.json
  catalyst_lifecycle_manifest.json
  proxy_hedge_manifest.json
  final_hardgates_manifest.json
```

---

## 7. Z-IRF-01~08

每条 IRF 必须：

```text
1. 声明 pipeline_id。
2. 声明 pipeline_tier=L1。
3. 声明 required_domains。
4. 使用 Skill Registry。
5. 使用 AsyncWorkflowExecutor。
6. 遵守 Parser-Scorer Split。
7. 必要时调用 ZC35 CatalystLifecycle。
8. 必要时调用 ZC45 Proxy Hedge / Defensive Allocation。
9. 必要时调用 ZC40 LimitBoardFillability。
10. 支持 Runtime Failover / Degraded Closeout。
11. 输出 OutputEnvelope。
12. 生成 AuditEvent。
13. 通过 smoke test。
14. 不输出真实交易动作。
```

8 条 IRF 定位：

```text
Z-IRF-01 Single Stock Institutional Research
  ZC10 + ZC20 + ZC30 + ZC35 + ZC40 + ZC45 + ZC50 + Report + Audit

Z-IRF-02 Monthly Full Market Selection
  ZC20 + ZC30 + ZC35 + ZC45 + ZC10 + Report + Audit

Z-IRF-03 Strategy Validation
  ZC20 + ZC30 + ZC35 + ZC45 + V3 + Report + Audit

Z-IRF-04 Paper Execution
  ZC30 + ZC35 + ZC40 + ZC45 + ZC50 + LimitBoard + Report + Audit

Z-IRF-05 Account Review
  ZC50 + ZC35 status + ZC45 beta budget + Report + Audit

Z-IRF-06 Portfolio Alpha Review
  ZC50 + ZC40 feedback + ZC35 catalyst state + ZC45 beta exposure + Report + Audit

Z-IRF-07 Multi-Strategy Portfolio
  ZC30 MultiStrategy + ZC35 + ZC45 + PortfolioRiskOverlay + ZC50 + Report + Audit

Z-IRF-08 Factor & Proprietary Data Factory
  ZC20 + ZC30 Factor + ZC35 event/catalyst factors + ZC45 risk overlay factors + ProprietaryData + Report + Audit
```

---

## 8. verify_v40_full_upgrade.sh

必须新增：

```text
scripts/verify_v40_full_upgrade.sh
```

内容必须覆盖：

```bash
python -m compileall zmatrix tests scripts

pytest -q tests/architecture/
pytest -q tests/contracts/
pytest -q tests/feature_mapping/
pytest -q tests/scoring/
pytest -q tests/runtime/
pytest -q tests/research_council/
pytest -q tests/reports/
pytest -q tests/data_layer/
pytest -q tests/proprietary_data/
pytest -q tests/catalyst_lifecycle/
pytest -q tests/proxy_hedge/
pytest -q tests/factor_factory/
pytest -q tests/multi_strategy/
pytest -q tests/portfolio_risk_overlay/
pytest -q tests/execution_quality/
pytest -q tests/account_governance/
pytest -q tests/system_cockpit/
pytest -q tests/audit/
pytest -q tests/irf_pipelines/

bash scripts/verify_v40_guardrails.sh
bash scripts/verify_v40_parser_scorer_split.sh
bash scripts/verify_v40_zc35_catalyst_guardrails.sh
bash scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
bash scripts/verify_v40_final_hardgates.sh
```

---

## 9. Release 文件

```text
docs/release/V40_CLOSEOUT_REPORT.md
release/v4.0-RC1/README.md
release/v4.0-RC1/V40_FULL_SCOPE_ACCEPTANCE_MATRIX_FINAL.md
release/v4.0-RC1/V40_KNOWN_LIMITATIONS.md
release/v4.0-RC1/V40_REGIME_CANDIDATE_QUARANTINE.md
release/v4.0-RC1/V40_PARSER_SCORER_SPLIT_MANIFEST.md
release/v4.0-RC1/V40_ZC35_CATALYST_LIFECYCLE_MANIFEST.md
release/v4.0-RC1/V40_ZC45_PROXY_HEDGE_MANIFEST.md
release/v4.0-RC1/V40_FINAL_HARDGATES_MANIFEST.md
```

V40_CLOSEOUT_REPORT 必须包含：

```text
起点版本
目标版本
6 批次完成情况
ZC00 Parser-Scorer Split 完成状态
ZC35 CatalystLifecycle 完成状态
ZC45 ProxyHedge 完成状态
LimitBoardFillability 完成状态
RuntimeFailover 完成状态
新增模块清单
新增测试清单
五条 verify 结果
V40_FULL_SCOPE_ACCEPTANCE_MATRIX 摘要
Regime candidate quarantine 状态
安全边界确认
Known Limitations
Commit SHA
Tag
```

---

## 10. 必须新增测试

```text
tests/system_cockpit/test_catalyst_lifecycle_panel.py
tests/system_cockpit/test_defensive_allocation_panel.py
tests/system_cockpit/test_beta_exposure_panel.py
tests/system_cockpit/test_proxy_hedge_stress_panel.py
tests/system_cockpit/test_limit_board_fillability_panel.py
tests/system_cockpit/test_llm_failover_panel.py
tests/system_cockpit/test_final_hardgates_panel.py
tests/system_cockpit/test_output_envelope_integration.py

tests/audit/test_catalyst_audit_trace.py
tests/audit/test_proxy_hedge_audit_trace.py
tests/audit/test_limit_board_audit_trace.py
tests/audit/test_failover_audit_trace.py
tests/audit/test_beta_exposure_trace.py
tests/audit/test_defensive_allocation_preview_trace.py
tests/audit/test_tail_hedge_simulation_trace.py
tests/audit/test_forbidden_output_scan.py

tests/irf_pipelines/test_irf_01_single_stock_research.py
tests/irf_pipelines/test_irf_02_monthly_full_market.py
tests/irf_pipelines/test_irf_03_strategy_validation.py
tests/irf_pipelines/test_irf_04_paper_execution.py
tests/irf_pipelines/test_irf_05_account_review.py
tests/irf_pipelines/test_irf_06_portfolio_alpha_review.py
tests/irf_pipelines/test_irf_07_multi_strategy_portfolio.py
tests/irf_pipelines/test_irf_08_factor_proprietary_data_factory.py
```

---

## 11. 更新验收矩阵

```text
V40-B5-001 System Cockpit Panels
V40-B5-002 AuditTrail
V40-B5-003 Audit Export JSON/MD/CSV/ZIP
V40-B5-004 Forbidden Output Scan
V40-B5-005 Z-IRF-01~08
V40-B5-006 verify_v40_full_upgrade.sh
V40-B5-007 v4.0-RC1 Release
V40-B5-008 AsyncPipelineHealthPanel
V40-B5-009 SchemaValidationFailurePanel
V40-B5-010 LLMCallBudgetPanel
V40-B5-011 PortfolioRiskOverlayPanel
V40-B5-012 ParserScorerHealthPanel
V40-B5-013 SubjectiveScoreViolationPanel
V40-B5-014 DeterministicScoringAuditTrace
V40-B5-015 CatalystLifecyclePanel
V40-B5-016 CatalystAuditTrace
V40-B5-017 DefensiveAllocationPanel
V40-B5-018 BetaExposurePanel
V40-B5-019 ProxyHedgeAuditTrace
V40-B5-020 FinalHardGatesPanel
V40-B5-021 LLMFailoverPanel
V40-B5-022 LimitBoardFillabilityPanel
V40-B5-023 ProxyHedgeStressPanel
```

---

## 12. 测试命令

```bash
python -m compileall zmatrix tests scripts

pytest -q tests/system_cockpit/
pytest -q tests/audit/
pytest -q tests/irf_pipelines/

bash scripts/verify_v40_guardrails.sh
bash scripts/verify_v40_parser_scorer_split.sh
bash scripts/verify_v40_zc35_catalyst_guardrails.sh
bash scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
bash scripts/verify_v40_final_hardgates.sh
bash scripts/verify_v40_full_upgrade.sh
```

---

## 13. 提交与发布

```bash
git status --short
git add .
git commit -m "v4.0-batch-5: add cockpit audit irf and final hard gates rc1"
git push
git rev-parse HEAD

git tag v4.0-RC1
git push origin v4.0-RC1
```

如果任何测试失败，不得打 tag。

---

## 14. 验收标准

```text
1. System Cockpit 可聚合 ZC00-ZC50/ZC35/ZC45/ZR。
2. OutputEnvelope 是唯一最终输出。
3. AuditTrail 可完整生成。
4. Audit 记录 fact extraction / subjective score ban / deterministic scoring trace。
5. Audit 记录 catalyst event / catalyst decay / sell-on-news trace。
6. Audit 记录 beta exposure / defensive allocation / proxy hedge stress trace。
7. Audit 记录 limit board fillability trace。
8. Audit 记录 llm failover / stale cache / degraded closeout trace。
9. Audit Export 支持 JSON/Markdown/CSV/ZIP。
10. ForbiddenOutputScan 可阻断真实交易指令。
11. ParserScorerScan 可阻断 LLM 主观分数。
12. ZC35 guardrails 可阻断催化系统直接交易。
13. ZC45 guardrails 可阻断伪对冲和真实交易。
14. FinalHardGates 可验证三大上线前硬门。
15. 8 条 IRF 全部 smoke run。
16. 每条 IRF 使用 AsyncWorkflowExecutor。
17. 每条 IRF 遵守 Parser-Scorer Split。
18. 每条 IRF 必要时调用 ZC35/ZC45/LimitBoard/Failover。
19. 每条 IRF 输出 OutputEnvelope。
20. 每条 IRF 生成 AuditEvent。
21. verify_v40_full_upgrade.sh 通过。
22. 五条 verify 全部通过。
23. V40_FULL_SCOPE_ACCEPTANCE_MATRIX 全部 PASS。
24. v4.0-RC1 tag 创建并推送。
25. 云仓 commit/tag 可验证。
```
