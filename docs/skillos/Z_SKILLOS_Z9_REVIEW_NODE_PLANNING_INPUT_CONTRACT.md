# Z9 Review Node Planning — INPUT CONTRACT

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Primary Input

The Z9 Review Node accepts exactly ONE input structure: z9_review_snapshot_candidate

```python
@dataclass(frozen=True)
class Z9ReviewSnapshotCandidate:
    report_node_id: str           # UUID of Z2 report
    source_graph_hash: str        # SHA-256 of source graph
    factor_context_summary_hash: str  # SHA-256
    evidence_chain_hash: str      # SHA-256
    research_summary_hash: str    # SHA-256
    risk_warning_hash: str        # SHA-256
    confidence_level: float       # 0.0 - 1.0
    confidence_reason: str        # Human-readable
    missing_evidence: list[str]   # Identified gaps
    degradation_status: str       # Enum value
    blocked_outputs_removed: list[str]  # Removed outputs
    review_required: bool         # Always True when sent
    review_reason: str            # Why review triggered
    readonly_only: bool           # Always True
```

## 2. Input Validation Rules

- report_node_id MUST be valid UUID v4
- All hash fields MUST be 64-char hex strings (SHA-256)
- confidence_level MUST be in [0.0, 1.0] range
- confidence_reason MUST be non-empty string
- readonly_only MUST be True (reject if False)
- review_required MUST be True (reject if False)
- degradation_status MUST be valid enum value

## 3. FORBIDDEN Inputs

| Field | Reason | Gate |
|---|---|---|
| raw factor values | Not explanation review | DENY_Z9_SOURCE_FORBIDDEN |
| real returns | Trade data | DENY_Z9_TRADE_RESULT_FORBIDDEN |
| trade_result | Trade data | DENY_Z9_TRADE_RESULT_FORBIDDEN |
| paper_trade_result | Simulated trade | DENY_Z9_TRADE_RESULT_FORBIDDEN |
| broker_result | Execution data | DENY_Z9_REAL_SOURCE_FORBIDDEN |
| real_pnl | Performance data | DENY_Z9_TRADE_RESULT_FORBIDDEN |
| position_change | Position authority | DENY_Z9_EXECUTION_FORBIDDEN |
| automatic_rebalance | Execution authority | DENY_Z9_EXECUTION_FORBIDDEN |
| execution_feedback | Execution data | DENY_Z9_EXECUTION_FORBIDDEN |
| broker payload | Broker data | DENY_Z9_REAL_SOURCE_FORBIDDEN |

## 4. Input Rejection Behavior

If any forbidden input is detected:
1. Immediately set degradation to DENY_Z9_SOURCE_FORBIDDEN
2. Emit no_trade_result = True
3. Log rejection reason
4. Return empty review with failure_reason_candidate
5. Do NOT process any further

## 5. Hash Verification

All input hashes must be verified for integrity:
- source_graph_hash must match expected format
- evidence_chain_hash must be present and non-empty
- If any hash is missing → DENY_Z9_EVIDENCE_INCOMPLETE
- Z9 does not recompute hashes (readonly consumer)

## 6. Snapshot Immutability

The z9_review_snapshot_candidate is frozen:
- No field may be modified after receipt
- No field may be added post-receipt
- The snapshot is consumed as-is from Z2
- Z9 feedback is advisory and readonly — no mutation back

## 7. Contract Test Requirements

Future tests must verify:
- Valid snapshot accepted correctly
- Missing hash triggers DENY_Z9_EVIDENCE_INCOMPLETE
- trade_result in input triggers DENY_Z9_TRADE_RESULT_FORBIDDEN
- readonly_only=False triggers rejection
- review_required=False triggers rejection
- All forbidden fields trigger appropriate DENY gate
