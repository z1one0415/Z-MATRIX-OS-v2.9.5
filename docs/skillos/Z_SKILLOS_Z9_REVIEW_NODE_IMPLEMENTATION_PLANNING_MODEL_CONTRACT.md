---
title: "Z9 Review Node Implementation Planning — Model Contract"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Model Contract

## Section 1: Model Architecture Overview

The Z9 Review Node model layer defines all Pydantic v2 data structures used throughout the review pipeline. All models are immutable by default (frozen=True), enforce strict validation (extra=forbid), and carry explicit type annotations. The model layer is the single source of truth for data shape throughout the Z9 review node implementation.

## Section 2: Core Model Definitions

### 2.1 ReviewLabel (Enum)
```python
class ReviewLabel(str, Enum):
    EXPLANATION_ACCEPTED_STRUCTURE_ONLY = "EXPLANATION_ACCEPTED_STRUCTURE_ONLY"
    EXPLANATION_ACCEPTED_WITH_MINOR_ISSUES = "EXPLANATION_ACCEPTED_WITH_MINOR_ISSUES"
    EXPLANATION_ACCEPTED_SIGNIFICANT_ISSUES = "EXPLANATION_ACCEPTED_SIGNIFICANT_ISSUES"
    EXPLANATION_REJECTED_INSUFFICIENT_EVIDENCE = "EXPLANATION_REJECTED_INSUFFICIENT_EVIDENCE"
    EXPLANATION_REJECTED_CONTRADICTORY = "EXPLANATION_REJECTED_CONTRADICTORY"
    REJECTED_UNSAFE_SOURCE = "REJECTED_UNSAFE_SOURCE"
```
6 review labels. REJECTED_UNSAFE_SOURCE is the catch-all for any input from non-Z2 sources (B1, A1, Factor Library).

### 2.2 DegradationDecision (Enum)
```python
class DegradationDecision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_DEGRADED = "ALLOW_DEGRADED"
    ALLOW_CACHED = "ALLOW_CACHED"
    DEGRADE_TO_EXPLANATION_ONLY = "DEGRADE_TO_EXPLANATION_ONLY"
    DEGRADE_TO_LABEL_ONLY = "DEGRADE_TO_LABEL_ONLY"
    DEGRADE_TO_UNSAFE_DEFAULT = "DEGRADE_TO_UNSAFE_DEFAULT"
    BLOCK_Z2_INPUT_MISMATCH = "BLOCK_Z2_INPUT_MISMATCH"
    BLOCK_EVIDENCE_TAMPERED = "BLOCK_EVIDENCE_TAMPERED"
    TRADE_RESULT_FORBIDDEN = "TRADE_RESULT_FORBIDDEN"
    MEMORY_MUTATION_FORBIDDEN = "MEMORY_MUTATION_FORBIDDEN"
```
10 degradation decisions. TRADE_RESULT_FORBIDDEN and MEMORY_MUTATION_FORBIDDEN are hard blockers.

### 2.3 AttributionType (Enum)
```python
class AttributionType(str, Enum):
    EVIDENCE_STRUCTURE = "EVIDENCE_STRUCTURE"
    EVIDENCE_COMPLETENESS = "EVIDENCE_COMPLETENESS"
    EVIDENCE_CONSISTENCY = "EVIDENCE_CONSISTENCY"
    REPORT_STRUCTURE = "REPORT_STRUCTURE"
    REPORT_CLARITY = "REPORT_CLARITY"
    REPORT_DEPTH = "REPORT_DEPTH"
    SOURCE_CREDIBILITY = "SOURCE_CREDIBILITY"
    METHODOLOGY_SOUNDNESS = "METHODOLOGY_SOUNDNESS"
    CONCLUSION_ALIGNMENT = "CONCLUSION_ALIGNMENT"
```
9 explanation-only attribution types. Profit attribution is NOT in this enum and is blocked.

### 2.4 ForbiddenAction (Enum)
```python
class ForbiddenAction(str, Enum):
    AUTO_PATCH_Z2_OUTPUT = "AUTO_PATCH_Z2_OUTPUT"
    AUTO_UPDATE_Z2_MODEL = "AUTO_UPDATE_Z2_MODEL"
    TRADE_SIGNAL_GENERATION = "TRADE_SIGNAL_GENERATION"
    PROFIT_COMPUTATION = "PROFIT_COMPUTATION"
    MEMORY_MUTATION = "MEMORY_MUTATION"
    BROKER_COMMUNICATION = "BROKER_COMMUNICATION"
    PORTFOLIO_OPTIMIZATION = "PORTFOLIO_OPTIMIZATION"
    PNL_CALCULATION = "PNL_CALCULATION"
```
8 forbidden actions mapped to DENY_Z9_TRADE_RESULT_FORBIDDEN and DENY_Z9_MEMORY_MUTATION_FORBIDDEN.

## Section 3: Data Models (Pydantic)

### 3.1 Z9ReviewInput (15-field contract from Z2)
```python
class Z9ReviewInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    source_node: Literal["Z2_RESEARCH_REPORT"]
    snapshot_id: str
    report_timestamp: datetime
    research_subject: str
    evidence_chain_hash: str
    report_structure_score: float
    evidence_completeness: float
    source_quality_rating: float
    methodology_soundness: float
    conclusion_confidence: float
    chain_of_reasoning_hash: str
    data_freshness_timestamp: datetime
    z2_node_version: str
    snapshot_signature: str
    review_request_id: str
```
15 required fields. source_node MUST be "Z2_RESEARCH_REPORT". Any other value triggers REJECTED_UNSAFE_SOURCE.

### 3.2 EvidenceEnvelope (19-field pass-through)
```python
class EvidenceEnvelope(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    evidence_hash: str
    evidence_version: int
    source_timestamp: datetime
    # 16 additional evidence fields inherited from Z2 snapshot
    field_01 through field_16: str
```
19 total fields. All are readonly pass-through from Z2 input. No re-generation. No modification.

### 3.3 ReviewOutput (6-label output)
```python
class Z9ReviewOutput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    review_id: str
    label: ReviewLabel
    explanation: str
    attribution: List[AttributionResult]
    evidence_snapshot: EvidenceEnvelope
    degradation_path: DegradationDecision
    z2_feedback_allowed: List[str]
    review_timestamp: datetime
    node_version: str
```
Output structure. Always exactly one label. Explanation is mandatory for all non-REJECTED_UNSAFE_SOURCE labels.

### 3.4 AttributionResult
```python
class AttributionResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    attribution_type: AttributionType
    confidence: float  # 0.0 to 1.0
    reasoning: str
    evidence_reference: str  # Field name from EvidenceEnvelope
    score: float  # 0.0 to 1.0
```
Individual attribution result. confidence and score range [0.0, 1.0].

### 3.5 DegradationContext
```python
class DegradationContext(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    decision: DegradationDecision
    reason: str
    input_source_valid: bool
    evidence_chain_intact: bool
    trade_result_attempted: bool
    memory_mutation_attempted: bool
    fallback_decision: Optional[DegradationDecision]
```
Context tracking for degradation decisions. trade_result_attempted and memory_mutation_attempted trigger hard blocks.

## Section 4: Model Invariants

### 4.1 Immutability
- ALL models use frozen=True
- ALL models use extra="forbid"
- No model allows runtime field addition
- Serialization preserves all fields exactly

### 4.2 Validation Rules
- source_node: Must equal "Z2_RESEARCH_REPORT"
- confidence/score: Must be in [0.0, 1.0]
- evidence_hash: Must match SHA-256 pattern
- snapshot_signature: Must match Ed25519 format
- All timestamps: Must be timezone-aware

### 4.3 Forbidden Field Patterns
- NO profit field
- NO pnl field
- NO trade_direction field
- NO position_size field
- NO broker_id field
- NO execution_price field

## Section 5: Model Lifecycle

### 5.1 Creation
Models are created exclusively through Pydantic validators. No raw dict construction is permitted. Factory functions must validate all inputs before model instantiation.

### 5.2 Serialization
- JSON serialization via model_dump_json()
- All enums serialized as string values
- Timestamps serialized as ISO 8601
- No field exclusion during serialization

### 5.3 Deserialization
- Strict validation on deserialization
- Unknown fields rejected (extra="forbid")
- Type coercion only for safe types (str→str, float→float with precision check)
- No implicit None→default coercion

## Section 6: Model Dependencies

### 6.1 Internal Dependencies
- ReviewOutput depends on ReviewLabel, AttributionResult, EvidenceEnvelope, DegradationDecision
- AttributionResult depends on AttributionType
- DegradationContext depends on DegradationDecision

### 6.2 External Dependencies
- All models reference fields defined in Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED
- EvidenceEnvelope inherits shape from Z2 evidence chain specification
- ReviewLabel values match Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED specification

## Section 7: Model Testing Requirements

### 7.1 Validation Tests
- All 6 ReviewLabel values parse correctly
- All 10 DegradationDecision values parse correctly
- All 9 AttributionType values parse correctly
- All 8 ForbiddenAction values parse correctly
- Z9ReviewInput rejects non-"Z2_RESEARCH_REPORT" source_node
- Z9ReviewInput rejects missing fields (15 required)
- Z9ReviewInput rejects extra fields
- EvidenceEnvelope rejects modification attempts
- ReviewOutput validates exactly one label
- All confidence/score fields clamp to [0.0, 1.0]

### 7.2 Serialization Tests
- Round-trip JSON serialization/deserialization for all models
- Enum string serialization correctness
- Timestamp ISO 8601 format
- Extra field rejection on deserialization

### 7.3 Forbidden Field Tests
- Profit field absent from all models
- PNL field absent from all models
- Trade field absent from all models
- Broker field absent from all models
