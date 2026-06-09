# Z9 Review Node Planning — ATTRIBUTION POLICY

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Attribution Purpose

Attribution in Z9 explains WHY a review label was assigned. It traces the reasoning
from evidence gaps to review conclusions. Z9 reviews Z2 explanation quality ONLY.
Attribution NEVER references profit, trades, or performance. no_trade_result applies.

## 2. ALLOWED Attribution Types

| Attribution | Purpose | Example |
|---|---|---|
| evidence_gap_attribution | Why evidence is incomplete | "Missing sector hash" |
| confidence_mismatch_attribution | Why confidence doesn't align | "High confidence, low evidence" |
| degradation_reason_attribution | Why degradation occurred | "Source hash missing" |
| blocked_output_risk_attribution | Why outputs were blocked | "Unsafe field detected" |
| missing_source_attribution | Why source data is absent | "No research_summary_hash" |
| structural_readiness_attribution | Why structure is/isn't ready | "All 12 sections complete" |
| future_validation_requirement_attribution | Why future validation needed | "Pending sector confirmation" |

## 3. FORBIDDEN Attribution Types

| Attribution | Reason | Gate |
|---|---|---|
| pnl_attribution | No profit measurement | DENY_Z9_TRADE_RESULT_FORBIDDEN |
| trade_attribution | No trade evaluation | DENY_Z9_TRADE_RESULT_FORBIDDEN |
| slippage_attribution | No execution quality | DENY_Z9_EXECUTION_FORBIDDEN |
| execution_quality_attribution | No execution review | DENY_Z9_EXECUTION_FORBIDDEN |
| broker_result_attribution | No broker evaluation | DENY_Z9_REAL_SOURCE_FORBIDDEN |
| position_change_attribution | No position authority | DENY_Z9_EXECUTION_FORBIDDEN |
| alpha_decay_from_real_trade | No real trade data | DENY_Z9_TRADE_RESULT_FORBIDDEN |
| paper_trade_performance_attribution | No simulated trade | DENY_Z9_TRADE_RESULT_FORBIDDEN |

## 4. Attribution Structure

```python
@dataclass(frozen=True)
class ReviewAttribution:
    attribution_type: str       # Must be from ALLOWED list
    source_section_id: str      # Which review section
    evidence_refs: list[str]    # Supporting evidence hashes
    reasoning: str              # Why this attribution
    confidence: float           # Attribution confidence
    readonly_only: bool         # Always True
    no_trade_result: bool       # Always True
```

## 5. Attribution Validation

- attribution_type MUST be in ALLOWED list
- If attribution_type is in FORBIDDEN list → kill_switch triggers
- reasoning MUST NOT mention profit, returns, alpha, or trade results
- evidence_refs MUST reference valid hashes from input
- Z9 feedback is advisory and readonly

## 6. Attribution Chain

Attributions form a chain:
1. evidence_gap_attribution → identifies what's missing
2. confidence_mismatch_attribution → explains alignment issues
3. degradation_reason_attribution → explains degradation cause
4. structural_readiness_attribution → assesses overall readiness
5. future_validation_requirement_attribution → identifies next steps

This chain is explanation-only. No execution decisions flow from it.

## 7. Attribution Audit

All attributions are:
- Immutable once produced
- Hashed into z9_review_section_hash
- Part of the z9_review_node_hash
- Available for human reviewer inspection
- Never used to trigger trades or position changes
- z9_review_snapshot_candidate is the sole source
