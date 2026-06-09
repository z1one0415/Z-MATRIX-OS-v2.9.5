# Z2 Research Report Node Implementation Planning — CONTRACTS

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
| Input contract | B1 CompositionGraphResponse |
| Output contract | z9_review_snapshot_candidate |
| Degradation contract | DENY_Z2_OUTPUTS_UNSAFE |

## 2. Scope

This document defines the input/output contracts for the Z2 Research Report Node.

### Input Contract

| Field | Type | Source | Required |
|-------|------|--------|----------|
| composition_graph | B1 CompositionGraphResponse | Upstream B1 node | Yes |
| request_id | str (UUID) | Orchestrator | Yes |
| timestamp | datetime (UTC) | Orchestrator | Yes |
| config_override | Optional[dict] | Orchestrator | No |

### Output Contract (Success)

| Field | Type | Consumer | Required |
|-------|------|----------|----------|
| report | ResearchReportNodeResponse | Orchestrator | Yes |
| z9_candidate | Z9ReviewSnapshotCandidate | Z9 Review Node | Yes |
| request_id | str (UUID) | Correlation | Yes |
| timestamp | datetime (UTC) | Audit | Yes |
| duration_ms | int | Monitoring | Yes |

### Output Contract (Degraded)

| Field | Type | Consumer | Required |
|-------|------|----------|----------|
| degradation | ReportDegradationStatus | Orchestrator | Yes |
| reason | str | Logging | Yes |
| request_id | str (UUID) | Correlation | Yes |
| timestamp | datetime (UTC) | Audit | Yes |
| partial_data | Optional[dict] | Debug | No |

### Z9 Snapshot Contract

| Field | Type | Constraint |
|-------|------|-----------|
| snapshot_id | str (UUID) | Generated per invocation |
| source_node | Literal["z2_research_report"] | Hardcoded |
| sections_summary | list[dict] | Derived from report sections |
| evidence_count | int | Total evidence items |
| confidence_level | str | HIGH_WITH_STRUCTURE_ONLY or degraded |
| created_at | datetime (UTC) | Invocation timestamp |

## 3. Dependency

- Input type B1 CompositionGraphResponse defined in B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED
- Output type z9_review_snapshot_candidate defined in Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED
- postmerge HEAD = c5f69f5

## 4. Boundary

- Contracts are the ONLY public interface of this node
- Internal implementation details are not part of the contract
- Contract changes require version bump and re-review
- Backward compatibility required for output contracts
- Input contract may be extended (additive only)

## 5. Forbidden

No contract field may be named or semantically equivalent to:
alpha_claim, expected_return_claim, buy_signal, sell_signal, position_weight, order_signal, trade_instruction, paper_trade_order, broker_action, portfolio_rebalance, real_trade_order, production_decision, real_pnl, trade_result

## 6. Proof

- test_contracts.py will validate input/output schema compliance (planned)
- test_contracts.py will verify Z9 snapshot contract conformance (planned)
- test_contracts.py will check degradation contract completeness (planned)
- Contract round-trip serialization tests planned
- Contract evolution (additive-only) tests planned

## 7. Next

- contracts.py implements these specifications
- All contract types exported via __init__.py
- Contract validation is fail-fast (no partial acceptance)
- Contract documentation auto-generated from Pydantic schemas

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
