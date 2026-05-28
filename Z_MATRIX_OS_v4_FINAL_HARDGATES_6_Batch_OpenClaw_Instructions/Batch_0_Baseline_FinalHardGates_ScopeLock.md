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

# Batch 0｜Baseline Freeze + Final Hard Gates Scope Lock

## 0.1 批次定位

本批只做非侵入式基线冻结、范围锁定和最终硬门登记。  
不得修改业务逻辑。不得修策略。不得重构核心代码。

本批必须锁定四组最高优先级协议：

```text
ZC00_PARSER_SCORER_SPLIT_PROTOCOL_V10
ZC35_CATALYST_LIFECYCLE_ENGINE_V10
ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION_V10
V40_FINAL_HARDGATES_PROTOCOL_V10
```

---

## 0.2 必须新增文件

```text
docs/upgrade/V40_BASELINE_AUDIT.md
docs/upgrade/V40_CONTENT_ASSET_INDEX.md
docs/upgrade/V40_UPGRADE_SCOPE_LOCK.md
docs/upgrade/V40_FULL_SCOPE_ACCEPTANCE_MATRIX.md
docs/upgrade/V40_REGIME_CANDIDATE_QUARANTINE.md
docs/upgrade/V40_FINAL_PATCH_NOTES.md
docs/upgrade/V40_ZC35_CATALYST_SCOPE_LOCK.md
docs/upgrade/V40_ZC45_PROXY_HEDGE_SCOPE_LOCK.md
docs/upgrade/V40_FINAL_HARDGATES_SCOPE_LOCK.md

docs/architecture/PARSER_SCORER_SPLIT_PROTOCOL_V10.md
docs/architecture/LLM_SUBJECTIVE_SCORE_BAN_V10.md
docs/architecture/DETERMINISTIC_SCORING_PROTOCOL_V10.md
docs/architecture/SCORE_TRACE_PROTOCOL_V10.md
docs/architecture/ZC35_CATALYST_LIFECYCLE_PROTOCOL_V10.md
docs/architecture/ZC35_EVENT_STUDY_PROTOCOL_V10.md
docs/architecture/ZC35_SELL_ON_NEWS_DEFENSE_PROTOCOL_V10.md
docs/architecture/ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION_PROTOCOL_V10.md
docs/architecture/ZC45_BETA_BUDGET_PROTOCOL_V10.md
docs/architecture/ZC45_TAIL_HEDGE_SIMULATOR_PROTOCOL_V10.md
docs/architecture/ZC40_LIMIT_BOARD_FILLABILITY_PROTOCOL_V10.md
docs/architecture/RUNTIME_LLM_FAILOVER_PROTOCOL_V10.md

scripts/verify_v40_guardrails.sh
scripts/verify_v40_parser_scorer_split.sh
scripts/verify_v40_zc35_catalyst_guardrails.sh
scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
scripts/verify_v40_final_hardgates.sh
```

---

## 0.3 V40_CONTENT_ASSET_INDEX.md 必须包含

```markdown
# V40 Content Asset Index

| Asset ID | Name | Required Batch | Status |
|---|---|---:|---|
| ZC00_PARSER_SCORER_SPLIT_PROTOCOL_V10 | 解析器-评分器分离协议 | Batch 0-5 | PENDING |
| ZC10_RESEARCH_COUNCIL_12_SEATS_SKILL_PACK_V10 | 十二人虚拟研究院 | Batch 2 | PENDING |
| ZREPORT_TEMPLATE_LIBRARY_12_MAIN_8_COMPONENTS_V10 | 12主模板+8组件模板 | Batch 2 | PENDING |
| ZC20_DATAFORGE_PROPRIETARY_ALT_DATA_EVIDENCE_V10 | DataForge 数据证据底座 | Batch 3 | PENDING |
| ZC30_FACTOR_FACTORY_IC_RANKIC_DECILE_PROMOTION_V10 | 因子生产线 | Batch 3 | PENDING |
| ZC35_CATALYST_LIFECYCLE_ENGINE_V10 | 催化生命周期与预期耗尽引擎 | Batch 3/4/5 | PENDING |
| ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION_V10 | 代理对冲与防御配置层 | Batch 3/4/5 | PENDING |
| ZC40_LIMIT_BOARD_FILLABILITY_GATE_V10 | 一字板/涨停可成交性硬门 | Batch 4/5 | PENDING |
| RUNTIME_LLM_PROVIDER_FAILOVER_V10 | LLM/API 失效降级硬门 | Batch 1/5 | PENDING |
| ZC30_MULTI_STRATEGY_SLEEVE_WEIGHT_LIFECYCLE_V10 | 多策略 Sleeve | Batch 3 | PENDING |
| ZC40_EXECUTION_QUALITY_ROUTE_COMPETITION_MICRO_LITE_V10 | 执行质量双件套 | Batch 4 | PENDING |
| ZC50_ACCOUNT_GOVERNANCE_CAPITAL_CURVE_ALPHA_V10 | 账户治理资金曲线 | Batch 4 | PENDING |
| ZSC_AUDIT_EXPORT_PACK_TRACEABILITY_V10 | 审计导出包 | Batch 5 | PENDING |
```

---

## 0.4 V40_FINAL_HARDGATES_SCOPE_LOCK.md 必须写入

```text
本轮新增三大上线前硬门：

1. ZC40 LimitBoardFillabilityGate
   - 一字涨停不可成交时不得输出新入场。
   - 开板接力必须进入 WAIT / PAPER_ONLY_OBSERVE。
   - 涨停连续衰减必须接入 ZC35 residual_power。

2. ZC45 ProxyHedgeStressTest
   - 代理对冲必须经过相关性稳定性与流动性压力测试。
   - 不得声称 Market Neutral。
   - 防御资产只能输出 preview，不得自动配置。

3. Runtime LLMProviderFailoverPolicy
   - LLM/API 失败时不得生成新判断。
   - 缓存事实必须标记 stale。
   - stale 事实只能导致 DATA_INSUFFICIENT / DEGRADED。
   - IRF 必须降级收口，不得崩溃。
```

---

## 0.5 V40_FULL_SCOPE_ACCEPTANCE_MATRIX.md 必须新增

```text
V40-B0-005 Parser-Scorer Split Scope Lock
V40-B0-006 LLM Subjective Score Ban
V40-B0-007 Deterministic Scoring Protocol
V40-B0-008 Score Trace Protocol
V40-B0-009 ZC35 Catalyst Lifecycle Scope Lock
V40-B0-010 ZC35 Sell-on-News Defense Scope Lock
V40-B0-011 ZC45 Proxy Hedge Scope Lock
V40-B0-012 ZC45 Defensive Allocation Guardrails
V40-B0-013 Final Hard Gates Scope Lock
V40-B0-014 LimitBoard Fillability Scope Lock
V40-B0-015 LLM Failover Scope Lock

V40-B1-020 LLMProviderFailoverPolicy
V40-B1-021 OfflineDegradedMode
V40-B1-022 CachedFactExtractionStore
V40-B1-023 CriticalPipelineFallback

V40-B3-030 ProxyHedgeStressTest

V40-B4-017 LimitBoardFillabilityGate
V40-B4-018 BoardContinuationDetector
V40-B4-019 OpenBoardChaseRiskDetector

V40-B5-020 FinalHardGatesPanel
V40-B5-021 LLMFailoverPanel
V40-B5-022 LimitBoardFillabilityPanel
V40-B5-023 ProxyHedgeStressPanel
```

---

## 0.6 verify_v40_final_hardgates.sh 要求

脚本必须检查：

```text
1. LimitBoardFillabilityGate 存在。
2. ProxyHedgeStressTest 存在。
3. LLMProviderFailoverPolicy 存在。
4. OfflineDegradedMode 存在。
5. CachedFactExtractionStore 存在。
6. CriticalPipelineFallback 存在。
7. 不存在 market_neutral_achieved=True。
8. 不存在 real_option_order。
9. 不存在 limit_up_auto_buy。
10. API failure path 不输出 fresh judgement。
```

---

## 0.7 必跑命令

```bash
python -m compileall zmatrix tests scripts
pytest -q
bash scripts/verify_v40_guardrails.sh
bash scripts/verify_v40_parser_scorer_split.sh
bash scripts/verify_v40_zc35_catalyst_guardrails.sh
bash scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
bash scripts/verify_v40_final_hardgates.sh
```

如果当前 pytest 历史遗留失败，只记录，不修业务逻辑。

---

## 0.8 提交

```bash
git status --short
git add .
git commit -m "v4.0-batch-0: freeze baseline and lock final hard gates"
git push
git rev-parse HEAD
```

---

## 0.9 验收标准

```text
1. 不修改业务逻辑。
2. ZC00/ZC35/ZC45/FinalHardGates 范围锁定文档完成。
3. 内容资产索引包含三大最终硬门。
4. Regime candidate 被 quarantine。
5. 五条 verify 脚本可运行。
6. 验收矩阵覆盖全部新增项。
7. 云仓 commit 可验证。
```
