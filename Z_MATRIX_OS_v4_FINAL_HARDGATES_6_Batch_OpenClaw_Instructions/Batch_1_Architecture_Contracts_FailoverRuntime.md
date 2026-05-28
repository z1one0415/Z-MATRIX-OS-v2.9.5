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

# Batch 1｜Architecture + Contracts + Parser-Scorer + Failover Runtime

## 1.1 批次目标

本批是 v4.0 的工程地基。  
必须完成：

```text
1. Capability Domain Registry
2. Skill Registry with parser_scorer_policy
3. Pipeline Tier Registry
4. Workflow DAG domain_state_outputs
5. OutputEnvelope
6. Pydantic Structured Output
7. Parser-Scorer Split Foundation
8. Deterministic Scoring Foundation
9. AsyncWorkflowExecutor
10. RateLimiter / TokenBucket / Retry / Timeout / CircuitBreaker
11. ZC35 Catalyst Contracts Foundation
12. ZC45 Proxy Hedge / Beta Budget Contracts Foundation
13. LLMProviderFailoverPolicy
14. OfflineDegradedMode
15. CachedFactExtractionStore
16. CriticalPipelineFallback
```

---

## 2. Capability Domains

必须注册：

```text
ZC00 Parser-Scorer Foundation
ZC10 Research Culture Domain
ZC20 Data Evidence Domain
ZC30 Strategy Validation Domain
ZC35 Catalyst Lifecycle Domain
ZC40 Execution Quality Domain
ZC45 Proxy Hedge & Defensive Allocation Domain
ZC50 Account Governance Domain
ZSC System Cockpit Domain
ZR Runtime Reliability Domain
```

所有 domain 默认：

```text
real_trade_allowed=False
requires_human_review_default=True
```

---

## 3. 必做模块

```text
zmatrix/architecture/capability_domain_registry.py
zmatrix/architecture/pipeline_tier_registry.py
zmatrix/architecture/skill_registry.py
zmatrix/architecture/pipeline_registry.py
zmatrix/architecture/workflow_dag.py
zmatrix/system_cockpit/output_envelope.py

zmatrix/contracts/base_contract.py
zmatrix/contracts/schema_validator.py
zmatrix/contracts/structured_output.py
zmatrix/contracts/validation_error.py
zmatrix/contracts/repair_once.py
zmatrix/contracts/fact_extraction_contract.py
zmatrix/contracts/subjective_score_ban.py
zmatrix/contracts/extraction_validation.py
zmatrix/contracts/catalyst_event_contract.py
zmatrix/contracts/proxy_hedge_contract.py
zmatrix/contracts/beta_budget_contract.py
zmatrix/contracts/failover_contract.py

zmatrix/feature_mapping/feature_schema_registry.py
zmatrix/feature_mapping/enum_normalizer.py
zmatrix/feature_mapping/evidence_span_validator.py
zmatrix/feature_mapping/feature_quality_gate.py

zmatrix/scoring/deterministic_scorer.py
zmatrix/scoring/scoring_config_registry.py
zmatrix/scoring/rule_weight_loader.py
zmatrix/scoring/score_trace.py
zmatrix/scoring/score_versioning.py
zmatrix/scoring/scoring_safety.py

zmatrix/runtime/async_workflow_executor.py
zmatrix/runtime/rate_limiter.py
zmatrix/runtime/token_bucket.py
zmatrix/runtime/retry_policy.py
zmatrix/runtime/timeout_policy.py
zmatrix/runtime/circuit_breaker.py
zmatrix/runtime/llm_call_budget.py
zmatrix/runtime/llm_provider_failover.py
zmatrix/runtime/offline_degraded_mode.py
zmatrix/runtime/cached_fact_extraction_store.py
zmatrix/runtime/critical_pipeline_fallback.py
zmatrix/runtime/stale_data_policy.py
zmatrix/runtime/degraded_closeout_report.py
```

---

## 4. SkillRegistry 必须支持

```text
skill_address
skill_id
primary_domain
secondary_domains
domain_role
input_contract
output_contract
allowed_pipeline_tiers
forbidden_capabilities
requires_human_review
real_trade_allowed
parser_scorer_policy
failover_policy_id
```

`parser_scorer_policy`：

```text
PARSER_ONLY
DETERMINISTIC_SCORER_ONLY
PARSER_THEN_SCORER
NO_LLM
```

---

## 5. Failover Contracts

```python
from typing import Literal
from pydantic import BaseModel

class LLMProviderStatus(BaseModel):
    provider_id: str
    status: Literal["OK", "TIMEOUT", "RATE_LIMITED", "AUTH_FAILED", "UNAVAILABLE", "UNKNOWN"]
    checked_at: str
    error_message: str | None = None

class CachedFactExtractionRecord(BaseModel):
    cache_id: str
    source_task_id: str
    created_at: str
    expires_at: str
    is_stale: bool
    fact_extraction_hash: str
    audit_event_id: str
    allowed_usage: Literal["READ_ONLY_REFERENCE", "DATA_INSUFFICIENT_ONLY", "BLOCKED"]

class DegradedCloseoutReport(BaseModel):
    pipeline_run_id: str
    degraded_reason: str
    failed_provider_status: list[LLMProviderStatus]
    stale_cache_used: bool = False
    new_judgement_generated: bool = False
    final_status: Literal["DEGRADED", "DATA_INSUFFICIENT", "FAILED_CLOSED"]
    real_trade_allowed: bool = False
```

硬规则：

```text
new_judgement_generated 必须为 False。
stale cache 不得驱动新策略结论。
```

---

## 6. LLMProviderFailoverPolicy

必须实现顺序：

```text
primary_provider
secondary_provider
local_cache_read_only
offline_degraded_mode
failed_closed
```

规则：

```text
1. Primary 失败 → 尝试 secondary。
2. Secondary 失败 → 读取已审计缓存。
3. 缓存未过期 → 仅可作为 READ_ONLY_REFERENCE。
4. 缓存过期 → DATA_INSUFFICIENT。
5. 不得使用 stale cache 生成新判断。
6. 必须输出 DegradedCloseoutReport。
```

---

## 7. 必须新增测试

```text
tests/architecture/test_capability_domain_registry.py
tests/architecture/test_skill_registry_parser_scorer_policy.py
tests/architecture/test_pipeline_tier_registry.py
tests/architecture/test_workflow_domain_state_outputs.py
tests/architecture/test_output_envelope.py

tests/contracts/test_fact_extraction_contract.py
tests/contracts/test_catalyst_event_contract.py
tests/contracts/test_proxy_hedge_contract.py
tests/contracts/test_beta_budget_contract.py
tests/contracts/test_failover_contract.py
tests/contracts/test_schema_validator.py
tests/contracts/test_subjective_score_ban.py

tests/feature_mapping/
tests/scoring/

tests/runtime/test_async_workflow_executor.py
tests/runtime/test_rate_limiter.py
tests/runtime/test_token_bucket.py
tests/runtime/test_retry_policy.py
tests/runtime/test_timeout_policy.py
tests/runtime/test_circuit_breaker.py
tests/runtime/test_llm_call_budget.py
tests/runtime/test_llm_provider_failover.py
tests/runtime/test_offline_degraded_mode.py
tests/runtime/test_cached_fact_extraction_store.py
tests/runtime/test_critical_pipeline_fallback.py
tests/runtime/test_stale_data_policy.py
tests/runtime/test_degraded_closeout_report.py
```

---

## 8. 更新验收矩阵

```text
V40-B1-001 Capability Domain Registry
V40-B1-002 Skill Registry Domain Tags
V40-B1-003 Pipeline Tier Registry
V40-B1-004 Workflow Domain State Outputs
V40-B1-005 OutputEnvelope
V40-B1-006 AsyncWorkflowExecutor
V40-B1-007 RateLimiterTokenBucket
V40-B1-008 StructuredOutputContract
V40-B1-009 PydanticSchemaValidation
V40-B1-010 RepairOnceFailClosed
V40-B1-011 FactExtractionContract
V40-B1-012 SubjectiveScoreBanValidator
V40-B1-013 FeatureMappingRegistry
V40-B1-014 ScoringConfigRegistry
V40-B1-015 DeterministicScorer
V40-B1-016 ScoreTrace
V40-B1-017 CatalystEventContract
V40-B1-018 ProxyHedgeContract
V40-B1-019 BetaBudgetContract
V40-B1-020 LLMProviderFailoverPolicy
V40-B1-021 OfflineDegradedMode
V40-B1-022 CachedFactExtractionStore
V40-B1-023 CriticalPipelineFallback
```

---

## 9. 测试命令

```bash
python -m compileall zmatrix tests scripts

pytest -q tests/architecture/
pytest -q tests/contracts/
pytest -q tests/feature_mapping/
pytest -q tests/scoring/
pytest -q tests/runtime/

bash scripts/verify_v40_guardrails.sh
bash scripts/verify_v40_parser_scorer_split.sh
bash scripts/verify_v40_zc35_catalyst_guardrails.sh
bash scripts/verify_v40_zc45_proxy_hedge_guardrails.sh
bash scripts/verify_v40_final_hardgates.sh
```

---

## 10. 提交

```bash
git status --short
git add .
git commit -m "v4.0-batch-1: add architecture contracts parser-scorer and failover runtime"
git push
git rev-parse HEAD
```

---

## 11. 验收标准

```text
1. ZC00-ZSC/ZR capability domains 注册完成。
2. SkillRegistry 支持 parser_scorer_policy 与 failover_policy_id。
3. FactExtraction/Catalyst/ProxyHedge/BetaBudget/Failover contracts 可校验。
4. SubjectiveScoreBanValidator 可阻断 LLM 主观分数。
5. DeterministicScorer 可由 config 生成 score。
6. ScoreTrace 可生成 hash。
7. AsyncWorkflowExecutor 可执行 DAG。
8. LLMProviderFailoverPolicy 可降级。
9. Stale cache 不生成新判断。
10. DegradedCloseoutReport 可生成。
11. pytest 全过。
12. 五条 verify 全过。
13. 云仓 commit 可验证。
```
