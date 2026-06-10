---
title: "Z9 Review Node Implementation Planning — Attribution Plan"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Attribution Plan

## Section 1: Attribution Architecture Overview

The Z9 attribution module computes explanation-only attribution results based on evidence fields from the Z2 snapshot. Attribution explains WHY a particular review label was assigned by analyzing evidence quality dimensions. The attribution module supports exactly 9 attribution types, all focused on explanation quality. Profit attribution is explicitly blocked — the module contains no profit/PNL/trade computation paths.

## Section 2: Attribution Type Catalog (9 Types)

### 2.1 EVIDENCE_STRUCTURE
**Category**: Evidence Quality  
**Analyzes**: How well the evidence fields are structured and organized  
**Consumes**: E1 (evidence_hash), E2 (evidence_version), E10 (chain_hash_copy)  
**Scoring**: Based on hash integrity, version consistency, structural field presence  
**Weight in review**: 15%

### 2.2 EVIDENCE_COMPLETENESS
**Category**: Evidence Quality  
**Analyzes**: How complete the 19-field evidence envelope is  
**Consumes**: E5 (evidence_completeness), E16 (citation_count), E15 (data_source_count)  
**Scoring**: Direct from evidence_completeness score, supplemented by citation/data source counts  
**Weight in review**: 20%

### 2.3 EVIDENCE_CONSISTENCY
**Category**: Evidence Quality  
**Analyzes**: Internal consistency of evidence fields  
**Consumes**: All E4-E8 scores, E9 (reasoning_hash), E11 (signature)  
**Scoring**: Cross-field correlation analysis; detects contradictory score patterns  
**Weight in review**: 15%

### 2.4 REPORT_STRUCTURE
**Category**: Report Quality  
**Analyzes**: Structural organization of the Z2 report  
**Consumes**: E4 (report_structure_score), E17 (analysis_depth_level)  
**Scoring**: Direct from report_structure_score, depth bonus/penalty from analysis_depth_level  
**Weight in review**: 15%

### 2.5 REPORT_CLARITY
**Category**: Report Quality  
**Analyzes**: Clarity and readability of the report explanation  
**Consumes**: E4 (report_structure_score), E14 (report_generation_context), E19 (evidence_provenance)  
**Scoring**: Composite from structure and context clarity indicators  
**Weight in review**: 10%

### 2.6 REPORT_DEPTH
**Category**: Report Quality  
**Analyzes**: Analytical depth of the report  
**Consumes**: E17 (analysis_depth_level), E16 (citation_count), E15 (data_source_count)  
**Scoring**: Depth level mapped to score, adjusted by citation and data source breadth  
**Weight in review**: 10%

### 2.7 SOURCE_CREDIBILITY
**Category**: Source Quality  
**Analyzes**: Credibility of data sources used in the report  
**Consumes**: E6 (source_quality_rating), E19 (evidence_provenance)  
**Scoring**: Direct from source_quality_rating, provenance check for source traceability  
**Weight in review**: 5%

### 2.8 METHODOLOGY_SOUNDNESS
**Category**: Methodology Quality  
**Analyzes**: Soundness of the research methodology  
**Consumes**: E7 (methodology_soundness), E9 (chain_of_reasoning_hash), E14 (report_generation_context)  
**Scoring**: Direct from methodology_soundness, reasoning chain integrity check  
**Weight in review**: 5%

### 2.9 CONCLUSION_ALIGNMENT
**Category**: Coherence  
**Analyzes**: How well conclusions align with presented evidence  
**Consumes**: E8 (conclusion_confidence), E18 (z2_confidence_interval), All E4-E8 scores  
**Scoring**: Evidence-to-conclusion mapping analysis; detects misalignment between scores and confidence  
**Weight in review**: 5%

## Section 3: Attribution Computation Pipeline

### 3.1 Pipeline Stages
```
Stage 1: Evidence Extraction
  → Receive EvidenceEnvelope (19 fields)
  → Validate all fields present

Stage 2: Per-Type Computation
  → For each of 9 AttributionType:
    → Extract relevant evidence fields
    → Compute confidence (0.0-1.0)
    → Compute score (0.0-1.0)
    → Generate reasoning text
    → Reference primary evidence field

Stage 3: Aggregation
  → Collect all 9 AttributionResult objects
  → Sort by confidence descending
  → Cap list at 20 entries (9 types + optional sub-attributions)

Stage 4: Profit Block Check
  → Scan all results for profit-related attribution
  → If detected: TRADE_RESULT_FORBIDDEN, halt processing
  → If clean: Proceed

Stage 5: Label Mapping
  → Map attribution results to ReviewLabel
  → Apply label assignment thresholds
  → Output labeled AttributionResult list
```

### 3.2 Confidence and Score Computation

**Confidence**: How confident the attribution engine is in this specific assessment
- 0.0-0.3: Low confidence (sparse evidence, borderline values)
- 0.3-0.7: Medium confidence (moderate evidence, clear patterns)
- 0.7-1.0: High confidence (rich evidence, strong signal)

**Score**: The actual quality score for this attribution dimension
- 0.0-0.3: Poor quality
- 0.3-0.7: Moderate quality
- 0.7-1.0: Good quality

## Section 4: Attribution → Label Mapping

### 4.1 Mapping Thresholds
| Condition | Label |
|-----------|-------|
| All scores >= 0.7, report_structure_score >= 0.7, evidence_completeness < 0.4 | EXPLANATION_ACCEPTED_STRUCTURE_ONLY |
| All scores >= 0.6, at most 2 in [0.6, 0.7] | EXPLANATION_ACCEPTED_WITH_MINOR_ISSUES |
| Any score < 0.6 OR >= 3 scores in [0.6, 0.7] | EXPLANATION_ACCEPTED_SIGNIFICANT_ISSUES |
| evidence_completeness < 0.3 | EXPLANATION_REJECTED_INSUFFICIENT_EVIDENCE |
| methodology_soundness < 0.3 | EXPLANATION_REJECTED_CONTRADICTORY |
| source_node != "Z2_RESEARCH_REPORT" | REJECTED_UNSAFE_SOURCE |

### 4.2 Label Selection Priority
Labels are evaluated in order of severity (lowest → highest):
1. REJECTED_UNSAFE_SOURCE (source check — highest priority)
2. EXPLANATION_REJECTED_CONTRADICTORY
3. EXPLANATION_REJECTED_INSUFFICIENT_EVIDENCE
4. EXPLANATION_ACCEPTED_SIGNIFICANT_ISSUES
5. EXPLANATION_ACCEPTED_WITH_MINOR_ISSUES
6. EXPLANATION_ACCEPTED_STRUCTURE_ONLY (default fallback)

The most severe matching label wins.

## Section 5: Profit Attribution Block (Hard Constraint)

### 5.1 Blocked Computation Types
The following are FORBIDDEN in the attribution module:
- Profit estimation
- PNL calculation
- Trade direction inference
- Position sizing recommendation
- Risk/reward ratio computation
- Sharpe ratio or any financial metric
- Market impact analysis
- Price target estimation
- Any computation involving monetary values
- Any computation referencing market prices

### 5.2 Block Enforcement
1. Static analysis: No import of trade/broker/profit/PNL modules
2. Runtime guard: AttributionEngine validates all computation types before execution
3. Output filter: AttributionResult scanned for profit-related keywords before return
4. Degradation trigger: Any attempt to compute profit → TRADE_RESULT_FORBIDDEN

### 5.3 Block Testing
- Verify no profit-related function exists in attribution.py
- Verify no financial metric computation paths
- Verify AttributionResult contains no profit-adjacent fields
- Verify TRADE_RESULT_FORBIDDEN triggered on block attempt

## Section 6: Attribution Module Implementation

### 6.1 Module: attribution.py
```
Class AttributionEngine:
    - compute_all(envelope: EvidenceEnvelope) -> List[AttributionResult]
    - compute_single(attr_type: AttributionType, envelope: EvidenceEnvelope) -> AttributionResult
    - map_to_label(results: List[AttributionResult]) -> ReviewLabel
    - validate_no_profit(results: List[AttributionResult]) -> bool
    - aggregate_confidence(results: List[AttributionResult]) -> float
    - sort_by_confidence(results: List[AttributionResult]) -> List[AttributionResult]
```

### 6.2 Attribution Type Registry
```
ATTRIBUTION_TYPE_MAP = {
    AttributionType.EVIDENCE_STRUCTURE: EvidenceStructureAnalyzer,
    AttributionType.EVIDENCE_COMPLETENESS: EvidenceCompletenessAnalyzer,
    AttributionType.EVIDENCE_CONSISTENCY: EvidenceConsistencyAnalyzer,
    AttributionType.REPORT_STRUCTURE: ReportStructureAnalyzer,
    AttributionType.REPORT_CLARITY: ReportClarityAnalyzer,
    AttributionType.REPORT_DEPTH: ReportDepthAnalyzer,
    AttributionType.SOURCE_CREDIBILITY: SourceCredibilityAnalyzer,
    AttributionType.METHODOLOGY_SOUNDNESS: MethodologySoundnessAnalyzer,
    AttributionType.CONCLUSION_ALIGNMENT: ConclusionAlignmentAnalyzer,
}
```

## Section 7: Attribution Testing Requirements

### 7.1 Coverage Tests
- All 9 attribution types produce valid AttributionResult
- Each type references valid EvidenceEnvelope fields
- Each type produces confidence in [0.0, 1.0]
- Each type produces score in [0.0, 1.0]
- Each type produces non-empty reasoning text
- Each type references a valid evidence_reference field name

### 7.2 Label Mapping Tests
- High scores (all >= 0.9) → EXPLANATION_ACCEPTED_WITH_MINOR_ISSUES
- evidence_completeness = 0.2 → EXPLANATION_REJECTED_INSUFFICIENT_EVIDENCE
- methodology_soundness = 0.2 → EXPLANATION_REJECTED_CONTRADICTORY
- Mixed moderate scores → EXPLANATION_ACCEPTED_SIGNIFICANT_ISSUES
- REJECTED_UNSAFE_SOURCE takes priority over all others

### 7.3 Profit Block Tests
- AttributionEngine.validate_no_profit detects profit computation
- TRADE_RESULT_FORBIDDEN triggered on profit attempt
- AttributionResult output contains no profit fields
- Static code analysis confirms no profit imports

### 7.4 Edge Case Tests
- Empty evidence envelope (all minimum values)
- Maximum evidence envelope (all 1.0 scores)
- NaN in evidence field (rejected at evidence layer)
- Infinity in evidence field (rejected at evidence layer)
- Null evidence field (rejected at evidence layer)
- Missing evidence field (rejected at evidence layer)

---

**Cross-Reference**: See EVIDENCE_PLAN for evidence field specifications. See MODEL_CONTRACT for AttributionResult and AttributionType models.
