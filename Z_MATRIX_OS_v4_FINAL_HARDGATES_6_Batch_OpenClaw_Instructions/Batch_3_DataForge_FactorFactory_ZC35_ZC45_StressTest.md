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

# Batch 3｜DataForge + FactorFactory + ZC35 + ZC45 + ProxyHedgeStressTest + MultiStrategy

## 3.1 批次目标

本批落地：

```text
ZC20 DataForge
ZC30 FactorFactory
ZC35 Catalyst Lifecycle Engine
ZC45 Proxy Hedge & Defensive Allocation
ZC45 ProxyHedgeStressTest
ZC30 MultiStrategy Sleeve
PortfolioRiskOverlay v0
```

ZC35 只输出催化状态与审查信号。  
ZC45 只输出防御配置预览、Beta 降低审查、纸面尾部保护模拟。  
二者均不得输出真实交易动作。

---

## 4. ZC20 DataForge 必做模块

```text
zmatrix/data_layer/source_registry.py
zmatrix/data_layer/data_asset_registry.py
zmatrix/data_layer/tushare_capability_scan.py
zmatrix/data_layer/data_lineage.py
zmatrix/data_layer/pit_snapshot.py
zmatrix/data_layer/data_quality_score.py
zmatrix/data_layer/evidence_card.py
zmatrix/data_layer/evidence_graph.py
zmatrix/data_layer/cross_source_validation.py
zmatrix/data_layer/benchmark_mapper.py
zmatrix/data_layer/alt_data_card.py
zmatrix/data_layer/alt_data_due_diligence.py
zmatrix/data_layer/alt_data_auto_collect.py
zmatrix/data_layer/fact_extraction_store.py
zmatrix/data_layer/parser_output_registry.py
zmatrix/data_layer/event_registry.py
zmatrix/data_layer/v3_data_evidence_payload.py
```

强制：

```text
AltData can_drive_execution=False
ProprietaryData can_drive_execution=False
EvidenceCard can_drive_execution=False
FactExtraction can_drive_execution=False
CatalystEvent can_drive_execution=False
ProxyHedgeSignal can_drive_execution=False
```

---

## 5. ZC35 Catalyst Lifecycle Engine

### 5.1 必做模块

```text
zmatrix/catalyst_lifecycle/event_schema.py
zmatrix/catalyst_lifecycle/event_parser.py
zmatrix/catalyst_lifecycle/event_eligibility_gate.py
zmatrix/catalyst_lifecycle/entity_relevance_gate.py
zmatrix/catalyst_lifecycle/scheduled_event_filter.py
zmatrix/catalyst_lifecycle/process_result_classifier.py
zmatrix/catalyst_lifecycle/novelty_detector.py
zmatrix/catalyst_lifecycle/priced_in_estimator.py
zmatrix/catalyst_lifecycle/event_study_engine.py
zmatrix/catalyst_lifecycle/abnormal_return_calculator.py
zmatrix/catalyst_lifecycle/catalyst_power_scorer.py
zmatrix/catalyst_lifecycle/decay_engine.py
zmatrix/catalyst_lifecycle/exhaustion_detector.py
zmatrix/catalyst_lifecycle/sell_on_news_detector.py
zmatrix/catalyst_lifecycle/catalyst_pool.py
zmatrix/catalyst_lifecycle/catalyst_report.py
zmatrix/catalyst_lifecycle/double_ring_fixture.py
zmatrix/catalyst_lifecycle/v3_catalyst_payload.py
```

### 5.2 ZC35 硬规则

```text
scheduled_event_without_surprise → BLOCK / DOWNGRADE
process_event_without_result → WAIT / DOWNGRADE
cross_sector_low_direct_relation → DOWNGRADE
entity_relevance=LOW/NONE → max_grade=C 或 BLOCK
rumor_without_verification → BLOCK
repeated_old_news → DOWNGRADE
```

### 5.3 Double Ring Fixture

必须建立双环传动教训 fixture：

```text
5/14 宇树 GD01：unscheduled product/industry catalyst，direct/high surprise，启动催化时钟
5/20 英伟达/Google I/O：scheduled/indirect，sell-on-news risk / no direct add score
5/22 发改委政策：policy catalyst，medium-high but needs direct link
5/25 华为 τ 定律：cross-sector low direct relation，entity mismatch
5/27 环动上会：process event without result，WAIT_RESULT
5/28 智博会开幕：scheduled conference without surprise，BLOCK/DOWNGRADE
```

---

## 6. ZC45 Proxy Hedge & Defensive Allocation

### 6.1 必做模块

```text
zmatrix/proxy_hedge/beta_exposure_estimator.py
zmatrix/proxy_hedge/defensive_sleeve_router.py
zmatrix/proxy_hedge/hedge_proxy_suitability.py
zmatrix/proxy_hedge/inverse_volatility_sizer.py
zmatrix/proxy_hedge/tail_hedge_simulator.py
zmatrix/proxy_hedge/proxy_hedge_stress_test.py
zmatrix/proxy_hedge/correlation_breakdown_detector.py
zmatrix/proxy_hedge/liquidity_crash_scenario.py
zmatrix/proxy_hedge/defensive_asset_stress_report.py
zmatrix/proxy_hedge/defensive_allocation_preview.py
zmatrix/proxy_hedge/proxy_hedge_report.py
zmatrix/proxy_hedge/v3_proxy_hedge_payload.py
```

### 6.2 BetaExposureEstimator

必须估算：

```text
portfolio_beta_vs_csi300
portfolio_beta_vs_csi500
portfolio_beta_vs_csi1000
industry_beta
growth_beta
small_cap_beta
liquidity_beta
```

输出必须：

```text
real_trade_allowed=False
```

### 6.3 HedgeProxySuitabilityScorer

评分维度：

```text
correlation_to_portfolio
correlation_stability
max_drawdown_in_bear_regime
liquidity
tracking_error
premium_discount_risk
regime_dependency
```

如果 correlation_stability=LOW：

```text
不得标记为 hedge，只能标记为 defensive_candidate 或 NOT_SUITABLE。
```

### 6.4 ProxyHedgeStressTest

必须构建压力场景：

```text
NORMAL_BEAR_MARKET
LIQUIDITY_CRASH
ALL_ASSET_SELL_OFF
RATE_SPIKE
CROSS_BORDER_ETF_PREMIUM_SHOCK
HIGH_DIVIDEND_CROWDING_UNWIND
BOND_DURATION_SHOCK
GOLD_USD_RATE_SHOCK
```

输出：

```text
PROXY_HEDGE_EFFECTIVE
DEFENSIVE_ONLY
CORRELATION_BREAKDOWN
LIQUIDITY_CRASH_RISK
NOT_A_HEDGE
DATA_INSUFFICIENT
```

硬规则：

```text
任何压力场景下 correlation_breakdown=True → 不得称为 hedge。
只能称为 defensive_candidate 或 NOT_A_HEDGE。
```

### 6.5 TailHedgeSimulator

只做纸面模拟：

```text
put_option_cost
expected_protection
tail_payoff
breakeven_drop
theta_decay
volatility_sensitivity
```

输出：

```text
TAIL_HEDGE_PAPER_ONLY
DO_NOT_EXECUTE
```

不得生成真实期权指令。

---

## 7. ZC30 FactorFactory

保留原有工业级验证：

```text
IC
RankIC
ICIR
Positive IC Ratio
Decile Return
Top-Bottom Spread
Monotonicity Score
Factor Decay T5/T20/T60
Regime Split
Correlation / Redundancy
WalkForwardValidator
SectorHoldoutValidator
MultipleTestingPenalty
FactorOverfitRiskScore
```

新增桥接模块：

```text
zmatrix/factor_factory/catalyst_factor_bridge.py
zmatrix/factor_factory/proxy_hedge_factor_bridge.py
zmatrix/factor_factory/final_hardgate_factor_guard.py
```

硬规则：

```text
如果 factor 来源包含 LLM raw subjective score → BLOCK。
如果 factor 来源是 deterministic score but missing score_trace_hash → BLOCK。
ZC45 输出不得作为 production trading factor，只能作为 risk overlay / defensive preview input。
```

---

## 8. MultiStrategy + PortfolioRiskOverlay

7 个 sleeve：

```text
BRD_ROLE_STRATEGY
SECTOR_ROTATION_STRATEGY
BLACK_HORSE_STRATEGY
BASE_CORE_STRATEGY
EVENT_CATALYST_STRATEGY
HIGH_DIVIDEND_DEFENSIVE_STRATEGY
TAIL_RISK_AVOIDANCE_STRATEGY
```

规则：

```text
EVENT_CATALYST_STRATEGY 必须读取 ZC35 lifecycle_status。
HIGH_DIVIDEND_DEFENSIVE_STRATEGY 必须读取 ZC45 suitability 与 ProxyHedgeStressTest。
CATALYST_EXHAUSTED / SELL_ON_NEWS_RISK 不得提升 sleeve weight。
ProxyHedgeStressTest=CORRELATION_BREAKDOWN 时不得提升 defensive sleeve 到 hedge 级别。
ZC45 defensive preview 不得自动调整真实 sleeve weight。
```

---

## 9. 必须新增测试

```text
tests/catalyst_lifecycle/test_event_schema.py
tests/catalyst_lifecycle/test_event_eligibility_gate.py
tests/catalyst_lifecycle/test_entity_relevance_gate.py
tests/catalyst_lifecycle/test_scheduled_event_filter.py
tests/catalyst_lifecycle/test_process_result_classifier.py
tests/catalyst_lifecycle/test_event_study_engine.py
tests/catalyst_lifecycle/test_catalyst_power_scorer.py
tests/catalyst_lifecycle/test_decay_engine.py
tests/catalyst_lifecycle/test_exhaustion_detector.py
tests/catalyst_lifecycle/test_sell_on_news_detector.py
tests/catalyst_lifecycle/test_double_ring_case_fixture.py
tests/catalyst_lifecycle/test_no_llm_catalyst_score.py

tests/proxy_hedge/test_beta_exposure_estimator.py
tests/proxy_hedge/test_defensive_sleeve_router.py
tests/proxy_hedge/test_hedge_proxy_suitability.py
tests/proxy_hedge/test_inverse_volatility_sizer.py
tests/proxy_hedge/test_tail_hedge_simulator.py
tests/proxy_hedge/test_proxy_hedge_stress_test.py
tests/proxy_hedge/test_correlation_breakdown_detector.py
tests/proxy_hedge/test_liquidity_crash_scenario.py
tests/proxy_hedge/test_defensive_asset_stress_report.py
tests/proxy_hedge/test_no_real_hedge_order.py
tests/proxy_hedge/test_no_market_neutral_claim.py

tests/factor_factory/test_catalyst_factor_bridge.py
tests/factor_factory/test_proxy_hedge_factor_bridge.py
tests/factor_factory/test_final_hardgate_factor_guard.py
tests/multi_strategy/
tests/portfolio_risk_overlay/
```

---

## 10. 更新验收矩阵

```text
V40-B3-001 DataForge
V40-B3-006 Factor IC
V40-B3-007 Factor RankIC
V40-B3-008 Factor Decile Return
V40-B3-011 FactorWalkForwardValidation
V40-B3-012 SectorHoldoutValidation
V40-B3-013 FactorOverfitRiskScore
V40-B3-014 PortfolioRiskOverlay
V40-B3-020 CatalystLifecycleEngine
V40-B3-021 EventStudyEngine
V40-B3-022 CatalystDecayEngine
V40-B3-023 SellOnNewsDetector
V40-B3-024 EntityRelevanceGate
V40-B3-025 CatalystDoubleRingFixture
V40-B3-026 ZC45 Proxy Hedge Layer
V40-B3-027 Defensive Sleeve Router
V40-B3-028 Hedge Proxy Suitability Scorer
V40-B3-029 Tail Hedge Simulator
V40-B3-030 ProxyHedgeStressTest
```

---

## 11. 测试命令

```bash
python -m compileall zmatrix tests scripts

pytest -q tests/data_layer/
pytest -q tests/proprietary_data/
pytest -q tests/catalyst_lifecycle/
pytest -q tests/proxy_hedge/
pytest -q tests/factor_factory/
pytest -q tests/multi_strategy/
pytest -q tests/portfolio_risk_overlay/

bash scripts/verify_v40_guardrails.sh
bash scripts/verify_v40_parser_scorer_split.sh
bash scripts/verify_v40_zc35_catalyst_guardrails.sh
bash scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
bash scripts/verify_v40_final_hardgates.sh
```

---

## 12. 提交

允许拆分：

```bash
git commit -m "v4.0-batch-3a: add dataforge evidence event and fact extraction store"
git commit -m "v4.0-batch-3b: add zc35 catalyst lifecycle engine"
git commit -m "v4.0-batch-3c: add zc45 proxy hedge stress test and defensive allocation"
git commit -m "v4.0-batch-3d: add factor factory hardgate bridges and multi strategy"
```

最终：

```bash
git push
git rev-parse HEAD
```

---

## 13. 验收标准

```text
1. DataForge 可运行。
2. EventRegistry 可存事件。
3. ZC35 可解析事件事实。
4. ZC35 不允许 LLM 输出 catalyst_score。
5. EventEligibilityGate 可阻断已计划无超预期事件。
6. EntityRelevanceGate 可阻断弱相关跨板块利好。
7. SellOnNewsDetector 可识别高风险兑现窗口。
8. 双环 fixture 通过。
9. ZC45 可估算 beta exposure。
10. ZC45 可输出 defensive allocation preview。
11. HedgeProxySuitability 可检查相关性稳定性。
12. ProxyHedgeStressTest 可识别相关性崩塌与流动性冲击。
13. TailHedgeSimulator 只输出 paper-only。
14. ZC45 不声称 market neutral。
15. FactorFactory 不接收 LLM 主观分数。
16. MultiStrategy 读取 ZC35/ZC45 状态但不自动调仓。
17. pytest 全过。
18. 五条 verify 全过。
19. 云仓 commit 可验证。
```
