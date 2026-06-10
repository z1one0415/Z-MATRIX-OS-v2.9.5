---
title: "Z9 Review Node Implementation Planning — Z2 Feedback Plan"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Z2 Feedback Plan

## Section 1: Z2 Feedback Architecture Overview

The Z2 feedback channel provides advisory/readonly feedback from Z9 back to Z2. Feedback is strictly advisory — it cannot auto-patch Z2 output, cannot auto-update Z2 models, and cannot trigger any automatic action in Z2. The channel defines exactly 10 allowed feedback fields and 8 forbidden fields. All feedback is read by Z2 at its discretion; Z9 never pushes feedback proactively.

## Section 2: Allowed Feedback Fields (10 Fields)

### 2.1 Field Catalog

| # | Field Name | Type | Description | Available On Labels |
|---|-----------|------|------------|-------------------|
| F1 | structure_acknowledgment | str | Acknowledgment of report structure quality | STRUCTURE_ONLY, MINOR_ISSUES, SIGNIFICANT_ISSUES |
| F2 | depth_recommendation | str | Recommendation to improve analytical depth | STRUCTURE_ONLY, SIGNIFICANT_ISSUES |
| F3 | enrichment_suggestion | str | Suggestion for content enrichment | STRUCTURE_ONLY |
| F4 | minor_issue_list | List[str] | List of minor issues found | MINOR_ISSUES |
| F5 | issue_severity_map | Dict[str, str] | Severity per issue (LOW/MEDIUM) | MINOR_ISSUES |
| F6 | recommended_fixes | List[str] | Recommended fix actions | MINOR_ISSUES, SIGNIFICANT_ISSUES |
| F7 | significant_issue_list | List[str] | List of significant issues | SIGNIFICANT_ISSUES |
| F8 | impact_assessment | str | Assessment of issue impact on report quality | SIGNIFICANT_ISSUES |
| F9 | revision_priority | str | Priority order for revisions (HIGH/MEDIUM/LOW) | SIGNIFICANT_ISSUES |
| F10 | evidence_gap_list | List[str] | List of evidence gaps | INSUFFICIENT_EVIDENCE, CONTRADICTORY |

### 2.2 Field Availability by Label

| Label | Available Fields | Count |
|-------|-----------------|:---:|
| EXPLANATION_ACCEPTED_STRUCTURE_ONLY | F1, F2, F3 | 3 |
| EXPLANATION_ACCEPTED_WITH_MINOR_ISSUES | F1, F4, F5, F6 | 5 (F1 always available) |
| EXPLANATION_ACCEPTED_SIGNIFICANT_ISSUES | F1, F6, F7, F8, F9 | 7 (F1, F6 shared) |
| EXPLANATION_REJECTED_INSUFFICIENT_EVIDENCE | F10 (all 10) | 10 (full feedback) |
| EXPLANATION_REJECTED_CONTRADICTORY | F10 (all 10) | 10 (full feedback) |
| REJECTED_UNSAFE_SOURCE | None | 0 (no feedback) |

### 2.3 Field Size Limits
- String fields: Maximum 4096 characters (F1-F3, F8-F9)
- List fields: Maximum 20 items (F4, F6, F7, F10)
- Dict fields: Maximum 20 key-value pairs (F5)
- Key length in dict: Maximum 128 characters
- Value length in dict: Maximum 256 characters

## Section 3: Forbidden Feedback Fields (8 Fields)

### 3.1 Forbidden Field Catalog

| # | Forbidden Field | Reason | Enforcement |
|---|----------------|--------|------------|
| X1 | auto_patch_z2_output | Would modify Z2 output | Runtime guard rejects |
| X2 | auto_update_z2_model | Would mutate Z2 model state | Runtime guard rejects |
| X3 | trade_recommendation | DENY_Z9_TRADE_RESULT_FORBIDDEN | Hard block |
| X4 | position_suggestion | Trade-related field | Hard block |
| X5 | profit_projection | Profit attribution blocked | Hard block |
| X6 | execution_instruction | Would drive execution pipeline | Hard block |
| X7 | model_parameter_override | Would auto-tune Z2 | Runtime guard rejects |
| X8 | forced_report_regeneration | Would trigger Z2 re-processing | Runtime guard rejects |

### 3.2 Forbidden Field Enforcement
The Z2 feedback channel MUST:
1. Validate all outgoing fields against the allowed list (10 fields)
2. Reject any field not in the allowed list
3. Log any attempt to add a forbidden field
4. Strip forbidden fields from output if they somehow appear
5. Raise an alert if blocked fields (X3-X6) are attempted

### 3.3 What Z2 Feedback CANNOT Do
- Auto-patch Z2 research report output
- Auto-update Z2 model parameters or weights
- Trigger automatic report re-generation
- Influence trade/execution decisions
- Override Z2 confidence scores
- Modify Z2 evidence chain
- Force Z2 to re-evaluate a subject
- Change Z2's methodology or approach

## Section 4: Feedback Channel Protocol

### 4.1 Delivery Model
Z9 feedback is delivered as part of the Z9ReviewOutput. The `z2_feedback_allowed` field in the output lists the names of feedback fields that are populated. Z2 reads this list and pulls the corresponding feedback values through the SkillOS evidence bus.

### 4.2 Pull Model (NOT Push)
Z2 feedback operates on a PULL model:
1. Z9 completes review and produces Z9ReviewOutput
2. Output is stored in the SkillOS evidence bus
3. Z2 polls or is notified of available feedback
4. Z2 pulls the feedback fields it wants to consume
5. Z2 decides whether and how to act on feedback

Z9 never PUSHES feedback to Z2 proactively. Z2 is always in control.

### 4.3 Idempotency
Feedback for a given review_id is idempotent — pulling the same review_id's feedback always returns the same fields. Feedback is not updated after initial delivery. If Z2 wants re-review, it must submit a new z9_review_snapshot_candidate with a new snapshot_id.

### 4.4 Feedback Expiry
Feedback expires after 24 hours. Expired feedback is still readable but carries an `expired=True` flag. Z2 should prefer fresh feedback (< 1 hour old).

## Section 5: Feedback Module Implementation

### 5.1 Module: z2_feedback.py
```
Class Z2FeedbackChannel:
    - available_fields_for_label(label: ReviewLabel) -> List[str]
    - prepare_feedback(label: ReviewLabel, attribution: List[AttributionResult]) -> Dict[str, Any]
    - validate_allowed_fields(feedback: Dict[str, Any]) -> bool
    - detect_forbidden_fields(feedback: Dict[str, Any]) -> List[str]
    - strip_forbidden(feedback: Dict[str, Any]) -> Dict[str, Any]
    - enforce_field_limits(feedback: Dict[str, Any]) -> Dict[str, Any]
```

### 5.2 Feedback Preparation by Label
```
STRUCTURE_ONLY:
    structure_acknowledgment: "Report structure meets minimum requirements."
    depth_recommendation: "Consider expanding analysis depth beyond surface-level findings."
    enrichment_suggestion: "Add supporting data and citations to strengthen conclusions."

MINOR_ISSUES:
    structure_acknowledgment: "Report structure is generally sound."
    minor_issue_list: [issues identified from attribution]
    issue_severity_map: {issue: severity for each minor issue}
    recommended_fixes: [fix actions for each minor issue]

SIGNIFICANT_ISSUES:
    structure_acknowledgment: "Report requires attention to significant quality issues."
    recommended_fixes: [fix actions for significant issues]
    significant_issue_list: [issues identified from attribution]
    impact_assessment: "These issues reduce report reliability by approximately X%."
    revision_priority: "Address methodology issues first, then evidence gaps."

INSUFFICIENT_EVIDENCE / CONTRADICTORY:
    evidence_gap_list: [gaps identified from evidence analysis]
    ... (full set of 10 feedback fields)
```

## Section 6: Feedback Advisory Guarantees

### 6.1 Readonly Guarantee
Z2 feedback is advisory and readonly. Z9 makes no guarantees that Z2 will:
- Read the feedback at all
- Act on any recommendation
- Apply any suggested fix
- Re-generate any report

### 6.2 No Obligation
Z2 has ZERO obligation to act on Z9 feedback. Feedback is provided as a service; consumption is entirely at Z2's discretion. Z9 does not track whether feedback was consumed or acted upon.

### 6.3 No Feedback Loop
Z9 feedback does not create a feedback loop. Each review is independent. Z9 does not maintain state about previous feedback. Z9 does not "remember" what it told Z2 before. Each review starts fresh from the provided evidence snapshot.

## Section 7: Feedback Testing Requirements

### 7.1 Allowed Field Tests
- All 10 allowed fields are producible
- Field counts match label expectations (3/5/7/10/10/0)
- Field values are within size limits
- Field types match specification

### 7.2 Forbidden Field Tests
- No forbidden field reaches Z2 feedback output
- Forbidden fields are detected and stripped
- Attempted forbidden field is logged
- Hard-block fields (X3-X6) trigger alerts

### 7.3 Label-Specific Tests
- STRUCTURE_ONLY produces exactly 3 fields
- MINOR_ISSUES produces exactly 5 fields (with F1)
- SIGNIFICANT_ISSUES produces exactly 7 fields
- INSUFFICIENT_EVIDENCE produces all 10 fields
- CONTRADICTORY produces all 10 fields
- UNSAFE_SOURCE produces 0 fields

### 7.4 Advisory Enforcement Tests
- Feedback is never pushed proactively
- Feedback does not auto-patch Z2 output
- Feedback does not auto-update Z2 models
- No feedback loop state maintained
- Feedback idempotent for same review_id

### 7.5 Size Limit Tests
- String fields truncated at 4096 chars
- List fields truncated at 20 items
- Dict fields truncated at 20 entries
- Oversized feedback logged with truncation warning

---

**Cross-Reference**: See OUTPUT_CONTRACT for Z9ReviewOutput structure. See DEGRADATION_PLAN for how degradation affects feedback availability. See MODEL_CONTRACT for feedback-related enums.
