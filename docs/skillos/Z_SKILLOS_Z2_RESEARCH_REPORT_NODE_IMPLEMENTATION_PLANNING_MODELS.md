# Z2 Research Report Node Implementation Planning — MODELS

> Status: PLANNING_COMPLETE
> Seal: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED
> Date: 2026-06-09
> Branch: plan/skillos-z2-research-report-node-implementation-planning
> Base: c5f69f5

---

## 1. Status

| Field | Value |
|-------|-------|
| Phase | Planning (docs-only) |
| Confidence | HIGH_WITH_STRUCTURE_ONLY |
| Model count | 8 planned |
| Validation | Pydantic v2 BaseModel |

## 2. Scope

This document specifies the planned model hierarchy for the Z2 Research Report Node.

### Planned Models

| # | Model | Role | Location |
|---|-------|------|----------|
| 1 | ResearchReportNodeRequest | Node entry point input | models.py |
| 2 | ResearchReportNodeResponse | Node output envelope | models.py |
| 3 | ResearchReportSection | Individual report section | models.py |
| 4 | ResearchReportEvidence | Evidence reference item | models.py |
| 5 | ResearchReportDecision | Section-level research decision | models.py |
| 6 | ResearchReportSummary | Report-level summary | models.py |
| 7 | Z9ReviewSnapshotCandidate | Output for Z9 consumption | models.py |
| 8 | ReportDegradationStatus | Degradation state envelope | models.py |

### Model Relationships

```
ResearchReportNodeRequest
    └── contains: B1 CompositionGraphResponse reference

ResearchReportNodeResponse
    ├── sections: list[ResearchReportSection]
    ├── summary: ResearchReportSummary
    ├── z9_candidate: Z9ReviewSnapshotCandidate
    └── degradation: Optional[ReportDegradationStatus]

ResearchReportSection
    ├── evidence: list[ResearchReportEvidence]
    └── decision: ResearchReportDecision

ResearchReportEvidence
    └── (leaf node — structured evidence reference)

ResearchReportDecision
    └── (leaf node — research conclusion for section)

ResearchReportSummary
    └── (aggregation of section decisions)

Z9ReviewSnapshotCandidate
    └── (Z9-contract-compliant output projection)

ReportDegradationStatus
    └── (failure mode + reason + partial data)
```

### Field Design Principles

- All fields use explicit types (no Any, no dynamic)
- Optional fields have explicit None default
- Enum fields for status/category (not raw strings)
- Datetime fields use UTC timezone-aware format
- List fields have explicit item type
- No nested dicts — always typed models

## 3. Dependency

- Models consume B1 CompositionGraphResponse (sealed upstream)
- Models emit z9_review_snapshot_candidate (Z9 contract sealed)
- postmerge HEAD = c5f69f5
- Pydantic v2 BaseModel as foundation

## 4. Boundary

- Models are pure data containers (no business logic in models)
- Validation logic in validators only (not in __init__)
- No model methods that perform I/O
- No model methods that call external services
- Models are immutable after creation (frozen=True planned)

## 5. Forbidden

No model may contain any of these fields:
alpha_claim, expected_return_claim, buy_signal, sell_signal, position_weight, order_signal, trade_instruction, paper_trade_order, broker_action, portfolio_rebalance, real_trade_order, production_decision, real_pnl, trade_result

## 6. Proof

- test_models.py will verify all 8 models instantiate correctly (planned)
- test_models.py will verify frozen immutability (planned)
- test_models.py will introspect model_fields for forbidden names (planned)
- test_contracts.py will verify input/output contract compliance (planned)
- Model serialization round-trip tests planned

## 7. Next

- Implementation: models.py is Batch 1 priority
- All models must pass forbidden-field scan before merge
- Model changes require contract review
- Z9ReviewSnapshotCandidate must pass Z9 contract validation

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
