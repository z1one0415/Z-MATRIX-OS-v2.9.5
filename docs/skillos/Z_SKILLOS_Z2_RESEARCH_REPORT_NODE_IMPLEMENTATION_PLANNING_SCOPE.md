# Z2 Research Report Node Implementation Planning — SCOPE

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
| Gate | Implementation blocked until review approval |
| Degradation mode | DENY_Z2_OUTPUTS_UNSAFE |

## 2. Scope

### In-Scope

| Area | Description |
|------|-------------|
| Models | ResearchReportNodeRequest, ResearchReportNodeResponse, ResearchReportSection, ResearchReportEvidence, ResearchReportDecision, ResearchReportSummary, Z9ReviewSnapshotCandidate, ReportDegradationStatus |
| Contracts | Input contract: B1 CompositionGraphResponse consumption; Output contract: z9_review_snapshot_candidate emission |
| Kill-switch | Disabled-by-default pattern; explicit env-var enablement required |
| Section builder | Pipeline for constructing report sections from composition graph data |
| Evidence layer | Validation and structuring of evidence references |
| Degradation | Graceful failure with DENY_Z2_OUTPUTS_UNSAFE status |
| Report builder | Orchestration of section assembly into complete report |
| Z9 snapshot | Transform report into z9_review_snapshot_candidate format |
| Registry | Node registration within capability invocation framework |

### Out-of-Scope

| Area | Reason |
|------|--------|
| Actual code implementation | This is planning phase only |
| Database schemas | Node is stateless; no persistence layer |
| API endpoints | Node is invoked internally via graph |
| UI/frontend | No user-facing components |
| Factor library internals | Consumed via sealed upstream contracts |
| B1 composition logic | Consumed as read-only input |
| Z9 review logic | Downstream consumer; interface defined only |
| Trading signals | PERMANENTLY FORBIDDEN |
| Portfolio management | PERMANENTLY FORBIDDEN |

### Boundary Conditions

- Maximum report sections: defined in constants (planned: 12)
- Maximum evidence items per section: defined in constants (planned: 8)
- Report generation timeout: defined in config (planned: 30s)
- Degradation threshold: defined in config (planned: 3 consecutive failures)

## 3. Dependency

All upstream dependencies are merged and sealed:
- Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED
- Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED
- B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED
- A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED
- FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED
- postmerge HEAD = c5f69f5

## 4. Boundary

- Module path: skillos/capability_invocation_os/research_report_node/
- Test path: tests/skillos/capability_invocation_os/research_report_node/
- No cross-module imports outside defined contracts
- No runtime network access
- No file system access
- No database connections
- Pure functional transformation pipeline

## 5. Forbidden

All trading/portfolio fields permanently banned:
alpha_claim, expected_return_claim, buy_signal, sell_signal, position_weight, order_signal, trade_instruction, paper_trade_order, broker_action, portfolio_rebalance, real_trade_order, production_decision, real_pnl, trade_result

## 6. Proof

- Scope boundaries verified against upstream sealed plans
- In/out-of-scope table covers all relevant areas
- Forbidden field list matches canonical list (14 items)
- Boundary conditions are measurable and testable
- No ambiguous scope items remain

## 7. Next

- Proceed to DEPENDENCY_MAP for detailed dependency analysis
- Proceed to BOUNDARY for detailed boundary constraints
- Proceed to FORBIDDEN for exhaustive forbidden-field rationale
- Implementation gated on human review approval

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
