---
title: "Z9 Review Node Implementation Planning — Input Contract"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Input Contract

## Section 1: Input Contract Overview

The Z9 Review Node accepts input exclusively through the `z9_review_snapshot_candidate` contract from Z2 Research Report Node. This document defines the complete input contract: accepted sources, required fields, validation rules, rejection criteria, and security boundaries. Z9 does NOT accept input from B1 Composition Graph, A1 Factor Library Bridge, FactorInvocationResponse, or research/factor_library paths.

## Section 2: Accepted Input Sources

### 2.1 Primary Source (ONLY accepted source)
```
Source Node: Z2_RESEARCH_REPORT_NODE
Contract Name: z9_review_snapshot_candidate
Transmission: Internal skill invocation (not network)
source_node value: "Z2_RESEARCH_REPORT" (literal string, validated)
```

### 2.2 Rejected Sources (all result in REJECTED_UNSAFE_SOURCE)
| # | Rejected Source | Reason | Detection Method |
|---|----------------|--------|-----------------|
| R1 | B1 Composition Graph | B1 provides graph composition, not research reports | source_node != "Z2_RESEARCH_REPORT" |
| R2 | A1 Factor Library Bridge | A1 provides factor data, not research reports | source_node != "Z2_RESEARCH_REPORT" |
| R3 | FactorInvocationResponse | Wrong data shape; factor results are not reviewable | Input contract validation failure |
| R4 | research/factor_library | Direct research data bypasses Z2 pipeline | Path isolation check |
| R5 | Any external source | External data lacks evidence chain integrity | Evidence chain hash validation failure |
| R6 | Any null/empty source | Undefined input cannot be reviewed | Required field validation failure |

## Section 3: Required Fields (15 total)

### 3.1 Field Specification Table
| # | Field Name | Type | Required | Description | Z9 Usage |
|---|-----------|------|:---:|------------|---------|
| 1 | source_node | Literal["Z2_RESEARCH_REPORT"] | REQUIRED | Must equal "Z2_RESEARCH_REPORT" | Source validation |
| 2 | snapshot_id | str (UUID v4) | REQUIRED | Unique snapshot identifier | Review tracking |
| 3 | report_timestamp | datetime (tz-aware) | REQUIRED | When report was generated | Temporal context |
| 4 | research_subject | str | REQUIRED | Subject of research (ticker/theme) | Review scope |
| 5 | evidence_chain_hash | str (SHA-256 hex) | REQUIRED | Hash of Z2 evidence chain | Evidence integrity |
| 6 | report_structure_score | float [0.0, 1.0] | REQUIRED | Z2 structural quality score | Review input |
| 7 | evidence_completeness | float [0.0, 1.0] | REQUIRED | Z2 evidence completeness score | Review input |
| 8 | source_quality_rating | float [0.0, 1.0] | REQUIRED | Z2 source quality assessment | Review input |
| 9 | methodology_soundness | float [0.0, 1.0] | REQUIRED | Z2 methodology evaluation | Review input |
| 10 | conclusion_confidence | float [0.0, 1.0] | REQUIRED | Z2 confidence in conclusion | Review input |
| 11 | chain_of_reasoning_hash | str (SHA-256 hex) | REQUIRED | Hash of reasoning chain | Reasoning integrity |
| 12 | data_freshness_timestamp | datetime (tz-aware) | REQUIRED | Data freshness stamp | Temporal validation |
| 13 | z2_node_version | str (semver) | REQUIRED | Z2 node version | Compatibility check |
| 14 | snapshot_signature | str (Ed25519 format) | REQUIRED | Cryptographic signature | Authenticity |
| 15 | review_request_id | str | REQUIRED | Review request identifier | Request tracking |

### 3.2 Field Validation Rules
- source_node: Exact string match "Z2_RESEARCH_REPORT". Case-sensitive.
- snapshot_id: Must parse as UUID v4. RFC 4122 compliant.
- report_timestamp: Must be timezone-aware datetime. Not in the future (tolerance: +5min).
- evidence_chain_hash: Must be 64 hex characters (SHA-256).
- All float fields: Must be in range [0.0, 1.0]. No NaN, no Inf.
- chain_of_reasoning_hash: Must be 64 hex characters (SHA-256).
- z2_node_version: Must parse as semver (MAJOR.MINOR.PATCH).
- snapshot_signature: Must be 128 hex characters (Ed25519).
- review_request_id: Must be non-empty string.

### 3.3 Field Presence Requirements
ALL 15 fields are REQUIRED. Missing any single field triggers BLOCK_Z2_INPUT_MISMATCH degradation decision. No default values are provided. No optional fields exist. The input contract is strict — partial input is never accepted.

## Section 4: Input Validation Pipeline

### 4.1 Validation Stages (sequential, fail-fast)
```
Stage 1: Source Check
  → Validate source_node == "Z2_RESEARCH_REPORT"
  → If FAIL: REJECTED_UNSAFE_SOURCE, stop processing

Stage 2: Field Presence Check
  → Validate all 15 fields present
  → If FAIL: BLOCK_Z2_INPUT_MISMATCH, stop processing

Stage 3: Type Validation
  → Validate each field type matches specification
  → If FAIL: BLOCK_Z2_INPUT_MISMATCH, stop processing

Stage 4: Range Validation
  → Validate float fields in [0.0, 1.0]
  → Validate timestamps sane
  → If FAIL: BLOCK_Z2_INPUT_MISMATCH, stop processing

Stage 5: Integrity Check
  → Validate evidence_chain_hash format
  → Validate snapshot_signature format
  → If FAIL: BLOCK_EVIDENCE_TAMPERED, stop processing

Stage 6: Evidence Extraction
  → Extract 19-field evidence envelope from snapshot
  → Build EvidenceEnvelope for downstream processing
```

### 4.2 Degradation Path on Input Failure
| Failure Stage | Degradation Decision | Output |
|--------------|---------------------|--------|
| Stage 1 (Source) | N/A (hard reject) | REJECTED_UNSAFE_SOURCE |
| Stage 2-4 (Field/Type/Range) | BLOCK_Z2_INPUT_MISMATCH | DEGRADE_TO_UNSAFE_DEFAULT |
| Stage 5 (Integrity) | BLOCK_EVIDENCE_TAMPERED | DEGRADE_TO_UNSAFE_DEFAULT |

## Section 5: Input Contract Boundaries

### 5.1 Explicitly Rejected Input Patterns
- B1 Composition Graph output (any shape)
- FactorInvocationResponse (any shape)
- research/factor_library raw data
- Market data feeds
- Any network-originated data
- Any user-provided raw input
- Any partially-formed Z2 snapshot
- Any tampered or re-signed evidence chain

### 5.2 Input Size Limits
- Maximum input payload: 64KB
- Maximum string field length: 4096 characters
- Maximum explanation text: 16384 characters
- Exceeding limits triggers BLOCK_Z2_INPUT_MISMATCH

### 5.3 Rate Limiting
- Maximum review invocations per second: 10
- Maximum review invocations per minute: 100
- Burst allowance: 5 invocations
- Exceeding limits triggers ALLOW_CACHED (return last cached review)

## Section 6: Input Contract Versioning

### 6.1 Current Version
Input Contract Version: 1.0.0
Matched Z2 Node Version Range: >= 2.0.0
Validated Against: Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED

### 6.2 Version Compatibility
- MAJOR version change: Full contract re-validation required
- MINOR version change: New fields may be added (must be backward-compatible)
- PATCH version change: No field changes, validation rules may tighten

### 6.3 Contract Drift Detection
If z2_node_version reports a version outside the compatible range:
1. Log compatibility warning
2. Attempt review with known contract shape
3. If field mismatch: BLOCK_Z2_INPUT_MISMATCH
4. If field compatible: ALLOW with compatibility flag

## Section 7: Input Contract Testing

### 7.1 Positive Tests
- Valid Z2 input with all 15 fields passes validation
- All 6 review labels assignable from valid input
- Evidence envelope correctly extracted
- Hash formats validated correctly

### 7.2 Negative Tests
- Non-Z2 source_node → REJECTED_UNSAFE_SOURCE
- Missing field → BLOCK_Z2_INPUT_MISMATCH
- Wrong field type → BLOCK_Z2_INPUT_MISMATCH
- Float out of range → BLOCK_Z2_INPUT_MISMATCH
- Tampered evidence hash → BLOCK_EVIDENCE_TAMPERED
- Invalid signature → BLOCK_EVIDENCE_TAMPERED
- B1 input (any shape) → REJECTED_UNSAFE_SOURCE
- FactorInvocationResponse → REJECTED_UNSAFE_SOURCE
- Empty input → BLOCK_Z2_INPUT_MISMATCH
- Exceeds size limit → BLOCK_Z2_INPUT_MISMATCH

### 7.3 Edge Case Tests
- Duplicate snapshot_id (idempotency)
- Future timestamp (tolerance check)
- Unicode in research_subject
- Maximum field length strings
- Minimum boundary float values (0.0, 1.0)

---

**Cross-Reference**: See MODEL_CONTRACT for Pydantic definitions. See OUTPUT_CONTRACT for review output specification. See DEGRADATION_PLAN for degradation paths.
