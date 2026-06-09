# Z9 Review Node Planning — OUTPUT CONTRACT

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Allowed Output Fields

```python
@dataclass(frozen=True)
class Z9ReviewOutput:
    z9_review_node_id: str                    # UUID of this review
    review_mode: str                          # "READONLY_EXPLANATION_REVIEW"
    source_z2_report_node_id: str             # From input
    source_graph_hash: str                    # Inherited
    evidence_chain_hash: str                  # Inherited
    review_scope: str                         # "EXPLANATION_QUALITY_ONLY"
    explanation_quality_label: str            # Primary output
    evidence_completeness_label: str          # Evidence assessment
    confidence_alignment_label: str           # Alignment check
    missing_evidence_summary: str             # Gap summary
    degradation_review: str                   # Degradation assessment
    blocked_output_review: str                # Blocked output assessment
    failure_reason_candidate: str             # If review failed
    parameter_adjustment_suggestion: str      # Advisory only
    next_validation_requirement: str          # Future needs
    review_label: str                         # Final label
    review_required: bool                     # Inherited True
    review_reason: str                        # Inherited
    readonly_only: bool                       # Always True
    no_trade_result: bool                     # Always True
    no_paper_trading: bool                    # Always True
    no_broker_action: bool                    # Always True
    no_position_change: bool                  # Always True
```

## 2. REVIEW_LABEL Allowed Values

| Label | Meaning |
|---|---|
| EXPLANATION_ACCEPTED_STRUCTURE_ONLY | Structure valid, evidence sufficient |
| EXPLANATION_DEGRADED_EVIDENCE_GAP | Structure valid but evidence incomplete |
| EXPLANATION_BLOCKED_OUTPUT_RISK | Some outputs were blocked |
| EXPLANATION_CONFIDENCE_MISMATCH | Confidence doesn't match evidence |
| EXPLANATION_REQUIRES_FUTURE_VALIDATION | Needs more data in future |
| EXPLANATION_REJECTED_UNSAFE_SOURCE | Source data contaminated |

## 3. FORBIDDEN Output Fields

| Field | Category | Enforcement |
|---|---|---|
| trade_instruction | Execution | kill_switch |
| buy_signal | Execution | kill_switch |
| sell_signal | Execution | kill_switch |
| position_weight | Position | kill_switch |
| order_signal | Execution | kill_switch |
| automatic_rebalance | Execution | kill_switch |
| broker_action | Broker | kill_switch |
| paper_trade_order | Simulated trade | kill_switch |
| real_trade_order | Real trade | kill_switch |
| real_pnl | Performance | kill_switch |
| performance_claim | Performance | kill_switch |
| alpha_claim | Performance | kill_switch |
| expected_return_claim | Performance | kill_switch |
| production_decision | Production | kill_switch |

## 4. Output Validation

Every output MUST:
- Include no_trade_result = True
- Include readonly_only = True
- Include review_mode = "READONLY_EXPLANATION_REVIEW"
- NOT include any forbidden field
- Have a valid review_label from the allowed set
- Reference source_z2_report_node_id from input

## 5. Output Immutability

Once produced, the review output:
- Cannot be modified retroactively
- Is hashed (z9_review_node_hash)
- Is appended to audit trail
- Does not trigger any downstream execution
- Z9 feedback is advisory and readonly

## 6. Degradation Output

When review cannot complete normally:
- failure_reason_candidate is populated
- review_label reflects degradation type
- All no_* markers remain True
- degradation_review explains the issue
- DENY_Z9_TRADE_RESULT_FORBIDDEN if trade data leaked

## 7. Contract Enforcement

Output contract is enforced by:
- Static type checking (frozen dataclass)
- Runtime validation in review_builder
- Kill switch for forbidden fields
- Test suite coverage (test_contracts.py)
- Integration test verifying no forbidden output
