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

# Batch 4｜ExecutionQuality + AccountGovernance + LimitBoard + Catalyst/Beta Integration

## 4.1 批次目标

本批落地：

```text
ZC40 Execution Quality
ZC40 LimitBoardFillabilityGate
ZC50 Account Governance
MicroLite Effectiveness Attribution
ZC35 Catalyst Status → Execution / Account Review Bridge
ZC45 Beta Budget / Defensive Allocation → Account Review Bridge
```

最终要求：

```text
ZC35 输出只作为执行降级与持仓审查信号，不得直接买卖。
ZC45 输出只作为风险预算、防御配置预览和账户审查信号，不得自动配置。
ZC40 在一字板/连续涨停/不可成交状态下，不得输出新入场。
```

---

## 2. ZC40 Execution Quality 必做模块

```text
zmatrix/execution_quality/execution_context.py
zmatrix/execution_quality/liquidity_gate.py
zmatrix/execution_quality/price_quality_gate.py
zmatrix/execution_quality/slippage_model.py
zmatrix/execution_quality/downgrade_policy.py
zmatrix/execution_quality/micro_lite.py
zmatrix/execution_quality/route_spec.py
zmatrix/execution_quality/route_competition.py
zmatrix/execution_quality/route_result.py
zmatrix/execution_quality/paper_order_plan.py
zmatrix/execution_quality/execution_fact_extraction.py
zmatrix/execution_quality/execution_deterministic_scoring.py
zmatrix/execution_quality/catalyst_status_execution_gate.py
zmatrix/execution_quality/beta_budget_execution_gate.py
zmatrix/execution_quality/limit_board_fillability_gate.py
zmatrix/execution_quality/board_continuation_detector.py
zmatrix/execution_quality/open_board_chase_risk_detector.py
zmatrix/execution_quality/execution_audit_report.py
zmatrix/execution_quality/microlite_effectiveness.py
zmatrix/execution_quality/gate_false_negative_report.py
zmatrix/execution_quality/execution_quality_attribution.py
zmatrix/execution_quality/user_reading_layer.py
zmatrix/execution_quality/v3_execution_payload.py
```

---

## 3. LimitBoardFillabilityGate

必须识别：

```text
one_word_limit_up
continuous_limit_up
limit_up_open_board
open_board_volume_sufficient
open_board_turnover_sufficient
gap_limit_up_without_fill
queue_unfillable
catalyst_residual_power_after_open_board
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

硬规则：

```text
one_word_limit_up=True → NOT_FILLABLE
continuous_limit_up>=2 且 no_open_board → WAIT_OPEN_BOARD
open_board=True 但 catalyst_residual_power=LOW → CHASE_RISK
open_board=True 但 turnover_insufficient → LIQUIDITY_TRAP
任何 NOT_FILLABLE/CHASE_RISK/LIQUIDITY_TRAP → no_new_entry=True
```

不得输出 buy。

---

## 4. CatalystStatusExecutionGate

读取 ZC35 输出：

```text
CATALYST_ACTIVE
CATALYST_DECAYING
CATALYST_EXHAUSTED
CATALYST_VACUUM
SELL_ON_NEWS_RISK
PROCESS_EVENT_WAIT
ENTITY_MISMATCH
DATA_INSUFFICIENT
```

映射规则：

```text
CATALYST_ACTIVE → no downgrade by catalyst
CATALYST_DECAYING → no_new_entry / route requires confirmation
CATALYST_EXHAUSTED → no_new_entry / holding_review
CATALYST_VACUUM → holding_review / paper_reduce_review
SELL_ON_NEWS_RISK → no_new_entry / wait / paper_reduce_review
PROCESS_EVENT_WAIT → watch_only
ENTITY_MISMATCH → remove_from_thesis / research_recheck
DATA_INSUFFICIENT → wait
```

---

## 5. BetaBudgetExecutionGate

读取 ZC45 输出：

```text
portfolio_beta
account_state
regime_state
defensive_allocation_preview
risk_contribution
correlation_stability
proxy_hedge_stress_status
tail_hedge_simulation_status
```

映射规则：

```text
BEAR_TREND + high_beta_exposure → no_new_growth_entry / beta_reduction_review
LIQUIDITY_CONTRACTION + correlation_breakdown → no_proxy_hedge_claim / cash_review
ORANGE/RED account_state → freeze_attack_sleeves
HIGH concentration risk → reduce_position_size_preview
TAIL_HEDGE_PAPER_ONLY → education_report_only
```

不得输出真实调仓。

---

## 6. ZC50 Account Governance 必做模块

```text
zmatrix/account_governance/daily_account_snapshot.py
zmatrix/account_governance/account_truth_ledger.py
zmatrix/account_governance/position_truth.py
zmatrix/account_governance/daily_pnl.py
zmatrix/account_governance/capital_curve.py
zmatrix/account_governance/paper_signal_ledger.py
zmatrix/account_governance/paper_capital_curve.py
zmatrix/account_governance/watchlist_ledger.py
zmatrix/account_governance/watchlist_opportunity_curve.py
zmatrix/account_governance/missed_opportunity_detection.py
zmatrix/account_governance/holding_alpha.py
zmatrix/account_governance/holding_decision_status.py
zmatrix/account_governance/portfolio_exposure.py
zmatrix/account_governance/risk_budget.py
zmatrix/account_governance/position_size_limit.py
zmatrix/account_governance/drawdown_governor.py
zmatrix/account_governance/action_permission_gate.py
zmatrix/account_governance/catalyst_account_review.py
zmatrix/account_governance/beta_budget_governor.py
zmatrix/account_governance/defensive_allocation_review.py
zmatrix/account_governance/limit_board_account_review.py
zmatrix/account_governance/daily_review_command.py
zmatrix/account_governance/account_audit_report.py
zmatrix/account_governance/user_reading_layer.py
zmatrix/account_governance/v3_account_payload.py
```

---

## 7. BetaBudgetGovernor

必须支持：

```text
account_state
regime_state
portfolio_beta
sleeve_beta
theme_beta
max_allowed_beta
single_stock_max_weight
sleeve_max_weight
theme_max_weight
drawdown_adjusted_weight
regime_adjusted_weight
```

输出：

```text
beta_budget_status
risk_budget_adjustment_preview
frozen_sleeves_preview
human_review_required
real_trade_allowed=False
```

---

## 8. DefensiveAllocationReview

输出：

```text
NO_ACTION
DEFENSIVE_REVIEW
CASH_RESERVE_REVIEW
HIGH_DIVIDEND_WATCH
PROXY_HEDGE_NOT_SUITABLE
TAIL_HEDGE_EDUCATION_ONLY
DATA_INSUFFICIENT
```

不得自动买入任何资产。

---

## 9. HoldingDecisionStatus

```text
HOLD_STRONG
HOLD_WATCH
HOLD_DEGRADED
REDUCE_REVIEW
EXIT_REVIEW
THESIS_BROKEN
CATALYST_EXHAUSTION_REVIEW
BETA_BUDGET_REVIEW
LIMIT_BOARD_FILLABILITY_REVIEW
DATA_INSUFFICIENT
```

禁止输出 SELL，只能输出 REVIEW。

---

## 10. 必须新增测试

```text
tests/execution_quality/test_micro_lite_metrics.py
tests/execution_quality/test_liquidity_gate.py
tests/execution_quality/test_price_quality_gate.py
tests/execution_quality/test_slippage_model.py
tests/execution_quality/test_route_competition.py
tests/execution_quality/test_catalyst_status_execution_gate.py
tests/execution_quality/test_beta_budget_execution_gate.py
tests/execution_quality/test_limit_board_fillability_gate.py
tests/execution_quality/test_board_continuation_detector.py
tests/execution_quality/test_open_board_chase_risk_detector.py
tests/execution_quality/test_limit_board_no_auto_buy.py
tests/execution_quality/test_microlite_effectiveness.py
tests/execution_quality/test_v3_execution_payload.py

tests/account_governance/test_daily_account_snapshot.py
tests/account_governance/test_real_capital_curve.py
tests/account_governance/test_paper_capital_curve.py
tests/account_governance/test_watchlist_opportunity_curve.py
tests/account_governance/test_holding_alpha.py
tests/account_governance/test_holding_decision_status.py
tests/account_governance/test_action_permission_gate.py
tests/account_governance/test_catalyst_account_review.py
tests/account_governance/test_beta_budget_governor.py
tests/account_governance/test_defensive_allocation_review.py
tests/account_governance/test_limit_board_account_review.py
```

---

## 11. 更新验收矩阵

```text
V40-B4-001 Z-MicroLite
V40-B4-002 Route Competition
V40-B4-003 Liquidity/Price/Slippage Gates
V40-B4-004 DailyAccountSnapshot
V40-B4-005 Real/Paper/Watchlist Curves
V40-B4-006 Holding Alpha
V40-B4-007 Action Permission Gate
V40-B4-008 MicroLiteEffectivenessAttribution
V40-B4-009 GateFalseNegativeReport
V40-B4-010 ExecutionQualityAttribution
V40-B4-011 ExecutionFactExtraction
V40-B4-012 ExecutionDeterministicScoring
V40-B4-013 CatalystStatusToExecutionGate
V40-B4-014 CatalystExhaustionToAccountReview
V40-B4-015 Beta Budget Governor
V40-B4-016 DefensiveAllocationToAccountReview
V40-B4-017 LimitBoardFillabilityGate
V40-B4-018 BoardContinuationDetector
V40-B4-019 OpenBoardChaseRiskDetector
```

---

## 12. 测试命令

```bash
python -m compileall zmatrix tests scripts

pytest -q tests/execution_quality/
pytest -q tests/account_governance/

bash scripts/verify_v40_guardrails.sh
bash scripts/verify_v40_parser_scorer_split.sh
bash scripts/verify_v40_zc35_catalyst_guardrails.sh
bash scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
bash scripts/verify_v40_final_hardgates.sh
```

---

## 13. 提交

```bash
git status --short
git add .
git commit -m "v4.0-batch-4: add execution account governance limit board and beta gates"
git push
git rev-parse HEAD
```

---

## 14. 验收标准

```text
1. MicroLite 公式/评分/标签本地计算。
2. LimitBoardFillabilityGate 可识别一字板、连续板、开板接力风险。
3. NOT_FILLABLE/CHASE_RISK/LIQUIDITY_TRAP 不输出新入场。
4. CatalystStatusExecutionGate 可把 ZC35 状态转为 review/wait/downgrade。
5. BetaBudgetExecutionGate 可把 ZC45 状态转为 beta_reduction_review。
6. BetaBudgetGovernor 可限制风险预算但不自动调仓。
7. DefensiveAllocationReview 可输出 paper-only review。
8. RouteCompetition 可输出 winning_route。
9. PaperOrderPlanPreview 不输出真实订单。
10. ActionPermissionGate 不输出真实交易。
11. pytest 全过。
12. 五条 verify 全过。
13. 云仓 commit 可验证。
```
