---
title: "Z9 Review Node Implementation Planning — Degradation Plan"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Degradation Plan

## Section 1: Degradation Architecture Overview

The Z9 degradation module implements a 10-decision degradation framework that governs how the review node responds to various error conditions, boundary violations, and system states. Two decisions (TRADE_RESULT_FORBIDDEN and MEMORY_MUTATION_FORBIDDEN) are hard blockers that immediately halt all processing. The remaining 8 decisions form a graduated degradation ladder from full operation to safe default fallback.

## Section 2: Degradation Decision Catalog (10 Decisions)

### 2.1 ALLOW (Decision #1)
**Severity**: NONE (normal operation)  
**Description**: Full review operation with all features enabled. Evidence validation passes, attribution is computed, review label assigned, Z2 feedback prepared.  
**Trigger**: All input validation passes, kill switch OFF, evidence chain intact.  
**Output**: Complete Z9ReviewOutput with all fields populated.  
**Recovery**: N/A (normal state).

### 2.2 ALLOW_DEGRADED (Decision #2)
**Severity**: LOW  
**Description**: Review proceeds but with reduced evidence. Some evidence fields are missing or borderline but review can continue with lower confidence.  
**Trigger**: 1-3 evidence fields below quality threshold but not critically missing.  
**Output**: Z9ReviewOutput with completeness_warning flag, reduced attribution confidence.  
**Recovery**: Self-recovering on next valid input. No manual intervention needed.

### 2.3 ALLOW_CACHED (Decision #3)
**Severity**: LOW  
**Description**: Return the most recent cached review result instead of computing a new one. Used when rate limits are hit or when evidence is unchanged from previous review.  
**Trigger**: Rate limit exceeded (10/sec or 100/min) OR duplicate snapshot_id within TTL.  
**Output**: Previous Z9ReviewOutput with cached=True flag.  
**Recovery**: Self-recovering when rate limit window resets or new snapshot_id received.

### 2.4 DEGRADE_TO_EXPLANATION_ONLY (Decision #4)
**Severity**: MEDIUM  
**Description**: Strip all attribution results and only return the review label with a basic explanation. Used when attribution computation encounters non-fatal errors.  
**Trigger**: Attribution computation partial failure OR 3+ evidence fields suspect.  
**Output**: Z9ReviewOutput with empty attribution list, basic text explanation.  
**Recovery**: Self-recovering on next valid input with complete evidence.

### 2.5 DEGRADE_TO_LABEL_ONLY (Decision #5)
**Severity**: MEDIUM  
**Description**: Return only the review label without explanation or attribution. Used when evidence quality is too poor for meaningful explanation generation.  
**Trigger**: 5+ evidence fields below minimum quality OR evidence_completeness extremely low but not zero.  
**Output**: Z9ReviewOutput with label only, explanation="Degraded: label only", no attribution.  
**Recovery**: Self-recovering on next valid input.

### 2.6 DEGRADE_TO_UNSAFE_DEFAULT (Decision #6)
**Severity**: HIGH  
**Description**: Default to REJECTED_UNSAFE_SOURCE label. Used when input validation fails at stages 2-5 (not source check, which is handled before degradation).  
**Trigger**: BLOCK_Z2_INPUT_MISMATCH OR BLOCK_EVIDENCE_TAMPERED OR any non-source integrity failure.  
**Output**: Z9ReviewOutput with label=REJECTED_UNSAFE_SOURCE, minimal explanation.  
**Recovery**: Requires next valid, untampered input from Z2.

### 2.7 BLOCK_Z2_INPUT_MISMATCH (Decision #7)
**Severity**: HIGH  
**Description**: Reject review due to input contract violation. Missing fields, wrong types, out-of-range values.  
**Trigger**: Stage 2-4 input validation failure (field presence, type, range).  
**Output**: DEGRADE_TO_UNSAFE_DEFAULT (upgraded). Detailed error logged.  
**Recovery**: Requires corrected input from Z2.

### 2.8 BLOCK_EVIDENCE_TAMPERED (Decision #8)
**Severity**: CRITICAL  
**Description**: Evidence integrity check failed. Hash mismatch, signature invalid, or fields modified in transit.  
**Trigger**: Stage 5 integrity validation failure.  
**Output**: DEGRADE_TO_UNSAFE_DEFAULT (upgraded). Security alert logged.  
**Recovery**: Requires clean, signed input from Z2. Security investigation may be warranted.

### 2.9 TRADE_RESULT_FORBIDDEN (Decision #9 — HARD BLOCKER)
**Severity**: BLOCKER (halts all processing)  
**Description**: Attempt to compute trade/profit/PNL result detected. Hard block — no review proceeds.  
**Trigger**: Any profit computation path activated OR trade-related function called OR financial metric computed.  
**Output**: NONE (processing halted). Security alert immediately raised.  
**Recovery**: Manual code audit required. Node must be restarted with corrected configuration.  
**Cannot be overridden**: This is a non-overridable hard block.

### 2.10 MEMORY_MUTATION_FORBIDDEN (Decision #10 — HARD BLOCKER)
**Severity**: BLOCKER (halts all processing)  
**Description**: Attempt to mutate system state (memory, knowledge graph, config, filesystem) detected.  
**Trigger**: Any write operation attempted OR state mutation function called OR DB connection opened.  
**Output**: NONE (processing halted). Security alert immediately raised.  
**Recovery**: Manual code audit required. Node must be restarted.  
**Cannot be overridden**: This is a non-overridable hard block.

## Section 3: Degradation Decision Tree

```
Input Received
    │
    ├── Kill Switch ON? ──→ DISABLED_DEFAULT_NOOP (bypass all, return NOOP)
    │
    ├── Source Check
    │   ├── source != "Z2_RESEARCH_REPORT" → REJECTED_UNSAFE_SOURCE (no degradation)
    │   └── source == "Z2_RESEARCH_REPORT" → Continue
    │
    ├── Trade/Memory Check (HARD BLOCKERS — checked FIRST)
    │   ├── Profit computation attempted → TRADE_RESULT_FORBIDDEN → HALT
    │   └── Memory mutation attempted → MEMORY_MUTATION_FORBIDDEN → HALT
    │
    ├── Input Validation (Stages 2-4)
    │   ├── Field missing/type/range error → BLOCK_Z2_INPUT_MISMATCH → DEGRADE_TO_UNSAFE_DEFAULT
    │   └── All fields valid → Continue
    │
    ├── Evidence Integrity (Stage 5)
    │   ├── Hash mismatch / tampering → BLOCK_EVIDENCE_TAMPERED → DEGRADE_TO_UNSAFE_DEFAULT
    │   └── Evidence clean → Continue
    │
    ├── Rate Limit Check
    │   ├── Rate limit exceeded → ALLOW_CACHED
    │   └── Within limits → Continue
    │
    ├── Evidence Quality Assessment
    │   ├── 5+ fields below minimum → DEGRADE_TO_LABEL_ONLY
    │   ├── 3+ fields suspect → DEGRADE_TO_EXPLANATION_ONLY
    │   ├── 1-3 fields borderline → ALLOW_DEGRADED
    │   └── All fields good → ALLOW
    │
    └── Output → Z9ReviewOutput with degradation_path recorded
```

## Section 4: Degradation Context Tracking

### 4.1 DegradationContext Model
Every degradation decision carries a DegradationContext that records:
- decision: Which decision was taken
- reason: Why this decision was triggered
- input_source_valid: Whether z9_review_snapshot_candidate source check passed
- evidence_chain_intact: Whether evidence hash verified
- trade_result_attempted: Whether profit computation was attempted (blocker)
- memory_mutation_attempted: Whether state mutation was attempted (blocker)
- fallback_decision: What fallback was applied (if any)

### 4.2 Degradation Logging
All degradation decisions are logged to the audit trail with:
- Timestamp (tz-aware)
- Snapshot ID
- Decision taken
- Triggering condition details
- Stack trace (for hard blockers only)
- Recovery recommendation

## Section 5: Degradation Recovery Paths

| Current State | Recovery Condition | Recovery Decision |
|--------------|-------------------|------------------|
| ALLOW_DEGRADED | Next input with complete evidence | ALLOW |
| ALLOW_CACHED | Rate limit window reset OR new snapshot | ALLOW |
| DEGRADE_TO_EXPLANATION_ONLY | Next input with >= 16 valid evidence fields | ALLOW |
| DEGRADE_TO_LABEL_ONLY | Next input with >= 14 valid evidence fields | ALLOW or ALLOW_DEGRADED |
| DEGRADE_TO_UNSAFE_DEFAULT | Next clean, signed input from Z2 | ALLOW |
| TRADE_RESULT_FORBIDDEN | Manual code audit + restart | ALLOW (after audit) |
| MEMORY_MUTATION_FORBIDDEN | Manual code audit + restart | ALLOW (after audit) |

## Section 6: DISABLED_DEFAULT_NOOP Integration

### 6.1 Priority
DISABLED_DEFAULT_NOOP is the highest-priority degradation state. It is checked BEFORE any other decision. When kill_switch is ON:
1. No input validation occurs
2. No evidence extraction occurs
3. No attribution computation occurs
4. No review label is assigned
5. No Z2 feedback is prepared
6. A simple NOOP response is returned

### 6.2 NOOP Response Format
```json
{
  "status": "DISABLED_DEFAULT_NOOP",
  "message": "Z9 Review Node is disabled by default. Set kill_switch=OFF to enable.",
  "timestamp": "2026-06-10T00:00:00+08:00",
  "node_version": "0.0.0-disabled"
}
```

## Section 7: Degradation Testing Requirements

### 7.1 Decision Path Tests
- ALLOW produces complete output with all fields
- ALLOW_DEGRADED produces output with completeness_warning
- ALLOW_CACHED returns previous result with cached=True
- DEGRADE_TO_EXPLANATION_ONLY has empty attribution
- DEGRADE_TO_LABEL_ONLY has no attribution or explanation
- DEGRADE_TO_UNSAFE_DEFAULT marks REJECTED_UNSAFE_SOURCE
- BLOCK_Z2_INPUT_MISMATCH escalates to DEGRADE_TO_UNSAFE_DEFAULT
- BLOCK_EVIDENCE_TAMPERED escalates to DEGRADE_TO_UNSAFE_DEFAULT
- TRADE_RESULT_FORBIDDEN halts ALL processing
- MEMORY_MUTATION_FORBIDDEN halts ALL processing

### 7.2 Blocker Tests
- TRADE_RESULT_FORBIDDEN is NOT overridable
- MEMORY_MUTATION_FORBIDDEN is NOT overridable
- Both blockers produce ZERO output (no partial results)
- Both blockers raise immediate security alerts
- Both blockers require manual intervention for recovery

### 7.3 DISABLED_DEFAULT Tests
- Kill switch ON → NOOP regardless of input validity
- Kill switch ON → NOOP regardless of evidence quality
- Kill switch ON → NOOP regardless of source
- Kill switch OFF → Normal degradation chain
- NOOP response format matches specification

### 7.4 Recovery Tests
- ALLOW_DEGRADED → ALLOW on next valid input
- ALLOW_CACHED → ALLOW after rate window
- DEGRADE_TO_EXPLANATION_ONLY → ALLOW on complete evidence
- DEGRADE_TO_LABEL_ONLY → ALLOW_DEGRADED on better evidence
- DEGRADE_TO_UNSAFE_DEFAULT → ALLOW on clean Z2 input
- TRADE_RESULT_FORBIDDEN persists until manual intervention
- MEMORY_MUTATION_FORBIDDEN persists until manual intervention

---

**Cross-Reference**: See OVERVIEW for degradation architecture context. See ATTRIBUTION_PLAN for how degradation affects attribution. See Z2_FEEDBACK_PLAN for feedback channel degradation.
