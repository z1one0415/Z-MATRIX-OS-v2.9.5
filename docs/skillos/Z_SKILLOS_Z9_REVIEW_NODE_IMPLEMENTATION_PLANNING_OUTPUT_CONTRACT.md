---
title: "Z9 Review Node Implementation Planning — Output Contract"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Output Contract

## Section 1: Output Contract Overview

The Z9 Review Node produces explanation-only review output. Every invocation returns exactly one review label from the 6-label set, accompanied by structured attribution evidence, a degradation decision trace, and (when applicable) Z2 feedback fields. No trade signal, broker instruction, profit/PNL computation, or state mutation is ever produced.

## Section 2: Review Label Definitions (6 Labels)

### 2.1 EXPLANATION_ACCEPTED_STRUCTURE_ONLY
**Severity**: LOWEST (positive)  
**Meaning**: The Z2 report structure is valid but the explanation lacks substantive analysis depth. The report form is correct but content is minimal.  
**Trigger**: report_structure_score >= 0.7 AND evidence_completeness < 0.4  
**Action**: Accept report structurally, flag for content enrichment.  
**Z2 Feedback**: 3 allowed feedback fields (structure acknowledgment, depth recommendation, enrichment suggestion).

### 2.2 EXPLANATION_ACCEPTED_WITH_MINOR_ISSUES
**Severity**: LOW  
**Meaning**: Review passes with minor issues. Overall quality is good but specific aspects need attention.  
**Trigger**: All scores >= 0.6 with at most 2 scores in [0.6, 0.7]  
**Action**: Accept with minor issue annotations.  
**Z2 Feedback**: 5 allowed feedback fields (minor issue list, severity per issue, recommended fixes).

### 2.3 EXPLANATION_ACCEPTED_SIGNIFICANT_ISSUES
**Severity**: MEDIUM  
**Meaning**: Review passes but with significant issues that impact quality. Multiple scores below threshold.  
**Trigger**: Any score < 0.6 OR at least 3 scores in [0.6, 0.7]  
**Action**: Accept with significant issue annotations. Recommend revision.  
**Z2 Feedback**: 7 allowed feedback fields (significant issue list, impact assessment, revision priority).

### 2.4 EXPLANATION_REJECTED_INSUFFICIENT_EVIDENCE
**Severity**: HIGH  
**Meaning**: The report lacks sufficient evidence to support its conclusions. Evidence completeness critically low.  
**Trigger**: evidence_completeness < 0.3 OR fewer than 10 evidence fields populated  
**Action**: Reject with evidence insufficiency explanation. Show gap analysis.  
**Z2 Feedback**: 10 allowed feedback fields (evidence gap list, required evidence types, collection guidance).

### 2.5 EXPLANATION_REJECTED_CONTRADICTORY
**Severity**: HIGH  
**Meaning**: Evidence within the report contradicts the stated conclusions. Internal inconsistency detected.  
**Trigger**: methodology_soundness < 0.3 OR contradiction_score > 0.7  
**Action**: Reject with contradiction analysis. Show conflicting evidence pairs.  
**Z2 Feedback**: 10 allowed feedback fields (contradiction pairs, reasoning chain break, resolution guidance).

### 2.6 REJECTED_UNSAFE_SOURCE
**Severity**: CRITICAL  
**Meaning**: Input from non-Z2 source detected. Cannot review. Security boundary violation.  
**Trigger**: source_node != "Z2_RESEARCH_REPORT" OR evidence chain tampered  
**Action**: Immediate rejection. No review performed. No attribution. No feedback.  
**Z2 Feedback**: NONE (0 allowed feedback fields — unsafe source cannot inform feedback).

## Section 3: Output Structure

### 3.1 Z9ReviewOutput (Full Structure)
| Field | Type | Description |
|-------|------|------------|
| review_id | str (UUID) | Unique review identifier |
| label | ReviewLabel | One of 6 labels |
| explanation | str | Structured explanation of review result |
| attribution | List[AttributionResult] | Attribution evidence (empty for REJECTED_UNSAFE_SOURCE) |
| evidence_snapshot | EvidenceEnvelope | 19-field evidence pass-through |
| degradation_path | DegradationDecision | Degradation decision applied |
| z2_feedback_allowed | List[str] | Allowed Z2 feedback field names |
| review_timestamp | datetime | When review was completed |
| node_version | str | Z9 node version |

### 3.2 Output Guarantees
1. Exactly ONE label is always assigned
2. Attribution is provided for all non-REJECTED labels
3. Evidence snapshot is always included (readonly pass-through)
4. Degradation path is always documented
5. Z2 feedback fields are always enumerated (even if empty list)
6. Timestamp is always present (tz-aware)
7. Node version is always included

### 3.3 Output Prohibitions
1. NO trade_direction field
2. NO profit_estimate field
3. NO pnl field
4. NO broker_instruction field
5. NO position_recommendation field
6. NO execution_instruction field
7. NO automated_action field
8. NO state_mutation field

## Section 4: Output Validation Rules

### 4.1 Label Assignment Validation
- review_id must be unique UUID
- label must be exactly one of 6 ReviewLabel enum values
- explanation must be non-empty for all labels except REJECTED_UNSAFE_SOURCE
- For REJECTED_UNSAFE_SOURCE: explanation must be exactly "Input rejected: unsafe source detected"
- attribution list must be non-empty for accepted labels, empty for rejected labels

### 4.2 Attribution Validation
- Each AttributionResult must reference a valid AttributionType
- confidence and score must be in [0.0, 1.0]
- evidence_reference must match a field name in EvidenceEnvelope
- No profit-related attribution types may appear

### 4.3 Evidence Validation
- EvidenceEnvelope must contain all 19 fields
- No field may be null (empty string minimum)
- Evidence hash must match input evidence_chain_hash
- Evidence must be immutable (identical to input)

### 4.4 Degradation Validation
- degradation_path must be one of 10 DegradationDecision values
- For REJECTED_UNSAFE_SOURCE: degradation_path must be "BLOCK_Z2_INPUT_MISMATCH" or triggered by source check
- TRADE_RESULT_FORBIDDEN must never appear in a valid output (it blocks output entirely)
- MEMORY_MUTATION_FORBIDDEN must never appear in a valid output (it blocks output entirely)

## Section 5: Output Size Limits

| Field | Maximum Size |
|-------|:---:|
| explanation | 16384 chars |
| attribution list | 20 entries |
| attribution.reasoning | 2048 chars |
| z2_feedback_allowed | 10 entries |
| Total output payload | 256KB |

Outputs exceeding these limits are truncated with a truncation warning flag. Truncation is logged but does not fail the review.

## Section 6: Output Delivery

### 6.1 Delivery Channel
Z9 output is delivered through the SkillOS evidence bus as an immutable evidence envelope. The output is:
- Logged to the audit trail (hash-chained)
- Returned to the calling SkillOS runtime
- Available for Z2 to consume as advisory feedback
- NOT sent to any trade/execution pipeline
- NOT written to any persistent store (readonly)

### 6.2 Idempotency
Reviews are idempotent: submitting the same snapshot_id twice returns the same review result (cached). Cached results carry a cached=True flag. Cache TTL: 1 hour. Cache invalidation: on new snapshot_id only.

### 6.3 Concurrency
Z9 supports concurrent review invocations up to the rate limit (10/sec, 100/min). Each invocation is independent. No shared mutable state between reviews.

## Section 7: Output Contract Testing

### 7.1 Structure Tests
- Valid output contains all required fields
- Output serializes/deserializes correctly
- Label enum values are correct
- Attribution list structure is correct
- Evidence envelope is complete

### 7.2 Boundary Tests
- Maximum explanation length handled
- Maximum attribution entries handled
- Empty attribution for REJECTED_UNSAFE_SOURCE
- Non-empty attribution for all accepted labels
- Missing optional fields handled (none are optional)

### 7.3 Forbidden Field Tests
- Output JSON contains no profit/PNL/trade/broker fields
- Output JSON contains no execution_instruction field
- Output JSON contains no automated_action field
- Output JSON contains no state_mutation field
- Static analysis confirms no forbidden field names in model definitions

### 7.4 Idempotency Tests
- Same snapshot_id twice returns identical output
- Different snapshot_id returns potentially different output
- Cache invalidation works after TTL
- Cached flag set correctly on cached responses

---

**Cross-Reference**: See MODEL_CONTRACT for Pydantic definitions. See INPUT_CONTRACT for input specification. See ATTRIBUTION_PLAN for attribution details.
