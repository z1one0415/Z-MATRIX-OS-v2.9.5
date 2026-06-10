---
title: "Z9 Review Node Implementation Planning — Evidence Plan"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Evidence Plan

## Section 1: Evidence Architecture Overview

Z9 inherits 19 evidence fields from the Z2 `z9_review_snapshot_candidate` snapshot. Z9 does NOT re-generate evidence. The evidence module acts as a strictly readonly pass-through layer that validates evidence integrity, detects tampering, and provides structured access to evidence fields for attribution computation. All evidence is treated as immutable — any modification attempt is detected and blocked.

## Section 2: Evidence Envelope Specification (19 Fields)

### 2.1 Core Identifier Fields (3)
| # | Field | Description | Validation |
|---|-------|------------|-----------|
| E1 | evidence_hash | SHA-256 hash of entire evidence chain | 64 hex chars |
| E2 | evidence_version | Integer version of evidence schema | >= 1 |
| E3 | source_timestamp | When evidence was captured | tz-aware, not future |

### 2.2 Report Quality Fields (5)
| # | Field | Description | Range |
|---|-------|------------|:---:|
| E4 | report_structure_score | Structural quality score | [0.0, 1.0] |
| E5 | evidence_completeness | Evidence completeness score | [0.0, 1.0] |
| E6 | source_quality_rating | Source quality assessment | [0.0, 1.0] |
| E7 | methodology_soundness | Methodology quality score | [0.0, 1.0] |
| E8 | conclusion_confidence | Confidence in conclusions | [0.0, 1.0] |

### 2.3 Chain Integrity Fields (4)
| # | Field | Description | Format |
|---|-------|------------|--------|
| E9 | chain_of_reasoning_hash | Reasoning chain hash | SHA-256 hex |
| E10 | evidence_chain_hash_copy | Duplicate of E1 for verification | SHA-256 hex |
| E11 | snapshot_signature | Ed25519 signature of snapshot | 128 hex chars |
| E12 | z2_node_version | Z2 node version at capture | semver |

### 2.4 Context Fields (7)
| # | Field | Description |
|---|-------|------------|
| E13 | research_subject | Subject of research |
| E14 | report_generation_context | Generation context metadata |
| E15 | data_source_count | Number of data sources used |
| E16 | citation_count | Number of citations |
| E17 | analysis_depth_level | Depth of analysis (shallow/medium/deep) |
| E18 | z2_confidence_interval | Z2 confidence interval |
| E19 | evidence_provenance | Provenance tracking string |

## Section 3: Evidence Pass-Through Contract

### 3.1 Immutability Guarantee
All 19 evidence fields pass through Z9 unchanged. The evidence module:
- Copies fields by value, not by reference
- Validates each field's integrity on receipt
- Computes a pass-through hash for audit trail
- Detects any modification attempt between receipt and output
- Rejects tampered evidence with BLOCK_EVIDENCE_TAMPERED

### 3.2 No Re-Generation Rule
Z9 must NOT:
- Re-compute any evidence field
- Re-evaluate any score
- Re-assess any rating
- Supplement missing evidence
- Infer evidence from external data
- Replace null fields with defaults
- Normalize or transform evidence values

### 3.3 Evidence Access Pattern
Evidence fields are read-only accessible by field name. The evidence module provides:
- `get_evidence(field_name: str) -> Any`: Read single field
- `get_all_evidence() -> EvidenceEnvelope`: Read entire envelope
- `validate_evidence_hash() -> bool`: Verify hash integrity
- `detect_tampering(original: EvidenceEnvelope, current: EvidenceEnvelope) -> List[str]`: Diff detection

## Section 4: Evidence Integrity Validation

### 4.1 Inbound Integrity Check
On receipt of z9_review_snapshot_candidate:
1. Extract evidence_chain_hash from input
2. Compute hash of evidence fields (E1-E19)
3. Compare computed hash with evidence_chain_hash
4. If mismatch: BLOCK_EVIDENCE_TAMPERED
5. If match: Proceed to field-level validation

### 4.2 Field-Level Validation
Each field is validated against its specification:
- E1, E10: Must match SHA-256 format
- E2: Must be integer >= 1
- E3: Must be tz-aware, not in future
- E4-E8: Must be in [0.0, 1.0], not NaN/Inf
- E9, E10: Must match SHA-256 format
- E11: Must match Ed25519 format (128 hex)
- E12: Must parse as semver
- E13-E19: Must be non-empty strings

### 4.3 Outbound Integrity Check
Before returning Z9ReviewOutput:
1. Capture evidence snapshot from input
2. Verify no field has been modified
3. Re-compute evidence hash
4. Compare with original evidence_chain_hash
5. If mismatch: Trigger evidence tampering alert, BLOCK_EVIDENCE_TAMPERED

## Section 5: Evidence Tampering Detection

### 5.1 Detection Mechanisms
| Mechanism | Description | Trigger Condition |
|-----------|------------|------------------|
| Hash Comparison | Compare inbound hash with computed hash | Inbound hash mismatch |
| Field Diff | Compare input fields with output fields | Any field differs |
| Metadata Check | Verify evidence_version, timestamps | Inconsistent metadata |
| Signature Validation | Verify Ed25519 signature | Invalid signature |
| Provenance Check | Verify provenance chain | Broken provenance |

### 5.2 Tampering Response
On detection of evidence tampering:
1. Log tampering event with full diff
2. Set degradation to BLOCK_EVIDENCE_TAMPERED
3. Do NOT proceed with review
4. Return DEGRADE_TO_UNSAFE_DEFAULT
5. Audit trail records tampering attempt

## Section 6: Evidence Module Implementation Plan

### 6.1 Module: evidence.py
```
Class EvidenceManager:
    - receive_evidence(snapshot: Z9ReviewInput) -> EvidenceEnvelope
    - validate_evidence(envelope: EvidenceEnvelope) -> bool
    - detect_tampering(original, current) -> List[str]
    - compute_evidence_hash(envelope: EvidenceEnvelope) -> str
    - get_field(field_name: str) -> Any
    - enumerate_fields() -> List[str]
```

### 6.2 Evidence Field Mapping (Z2 Input → Z9 Evidence)
```
Z9ReviewInput.evidence_chain_hash  → EvidenceEnvelope.evidence_hash (E1)
Z9ReviewInput.report_structure_score → EvidenceEnvelope.report_structure_score (E4)
Z9ReviewInput.evidence_completeness → EvidenceEnvelope.evidence_completeness (E5)
Z9ReviewInput.source_quality_rating → EvidenceEnvelope.source_quality_rating (E6)
Z9ReviewInput.methodology_soundness  → EvidenceEnvelope.methodology_soundness (E7)
Z9ReviewInput.conclusion_confidence → EvidenceEnvelope.conclusion_confidence (E8)
Z9ReviewInput.chain_of_reasoning_hash → EvidenceEnvelope.chain_of_reasoning_hash (E9)
Z9ReviewInput.snapshot_signature → EvidenceEnvelope.snapshot_signature (E11)
Z9ReviewInput.z2_node_version → EvidenceEnvelope.z2_node_version (E12)
Z9ReviewInput.research_subject → EvidenceEnvelope.research_subject (E13)
Z9ReviewInput.data_freshness_timestamp → EvidenceEnvelope.source_timestamp (E3)
```

## Section 7: Evidence Testing Requirements

### 7.1 Pass-Through Tests
- All 19 fields pass through unchanged
- Field values identical before and after evidence extraction
- Evidence hash recomputation matches input hash
- Evidence manager returns correct field by name

### 7.2 Tampering Detection Tests
- Modified score field detected
- Modified hash field detected
- Missing field detected
- Extra field detected
- Null field detected
- Tampered signature detected
- BLOCK_EVIDENCE_TAMPERED triggered on any tampering

### 7.3 Integrity Tests
- Valid evidence passes all checks
- Invalid hash format rejected
- Invalid score range rejected
- NaN score rejected
- Future timestamp rejected
- Out-of-version evidence_version rejected

### 7.4 Immutability Tests
- EvidenceEnvelope is frozen (cannot modify after creation)
- EvidenceManager does not expose mutation methods
- No write operations in evidence module
- Evidence hash is deterministic (same input → same hash)
- Evidence hash changes detectably on any field change

---

**Cross-Reference**: See MODEL_CONTRACT for EvidenceEnvelope definition. See DEGRADATION_PLAN for BLOCK_EVIDENCE_TAMPERED path. See ATTRIBUTION_PLAN for evidence consumption.
