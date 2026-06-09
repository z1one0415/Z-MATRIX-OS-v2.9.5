# Z2 Research Report Node Implementation Planning — BOUNDARY

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
| Boundary type | Hard (no exceptions) |
| Degradation | DENY_Z2_OUTPUTS_UNSAFE |

## 2. Scope

This document defines the hard boundaries for the Z2 Research Report Node implementation. These boundaries are non-negotiable and enforced via tests.

## 3. Dependency

- All upstream sealed (see DEPENDENCY_MAP)
- postmerge HEAD = c5f69f5
- B1 CompositionGraphResponse is the SOLE data input
- z9_review_snapshot_candidate is the SOLE structured output

## 4. Boundary

### Input Boundaries

| Constraint | Enforcement |
|-----------|-------------|
| Only B1 CompositionGraphResponse accepted | Type check at entry |
| No raw market data input | Contract validation |
| No user-supplied free-text input | Schema rejection |
| No database query results as input | Import ban |
| No network response as input | Import ban |
| Input must be non-None | Null check with degradation |
| Input must pass schema validation | Pydantic validation |

### Output Boundaries

| Constraint | Enforcement |
|-----------|-------------|
| Only ResearchReportNodeResponse emitted | Return type annotation |
| z9_review_snapshot_candidate must conform to Z9 contract | Schema validation |
| No trading signals in output | Forbidden field scan |
| No portfolio recommendations | Forbidden field scan |
| No confidence scores implying trade action | Semantic review |
| Output must be JSON-serializable | Pydantic model |
| Degraded output uses ReportDegradationStatus | Type enforcement |

### Computational Boundaries

| Constraint | Enforcement |
|-----------|-------------|
| No network calls | Import ban (socket, requests, httpx, urllib) |
| No file I/O | Import ban (open, pathlib write, os.write) |
| No database access | Import ban (sqlalchemy, psycopg2, sqlite3) |
| No subprocess spawning | Import ban (subprocess, os.system) |
| No threading/multiprocessing | Import ban (threading, multiprocessing) |
| Deterministic output for same input | Unit test assertion |
| Maximum execution time: 30s | Timeout wrapper |
| No global mutable state | Static analysis |

### Module Boundaries

| Constraint | Enforcement |
|-----------|-------------|
| No imports outside skillos/ and stdlib | test_no_forbidden_imports.py |
| No cross-node imports (e.g., no importing z9 internals) | Import ban |
| No importing from tests/ in source | Static check |
| Registry is the only public API surface | __init__.py exports |

## 5. Forbidden

Permanently forbidden in any boundary-crossing interface:
- alpha_claim, expected_return_claim, buy_signal, sell_signal
- position_weight, order_signal, trade_instruction, paper_trade_order
- broker_action, portfolio_rebalance, real_trade_order, production_decision
- real_pnl, trade_result

## 6. Proof

- Boundary constraints are testable (each has enforcement mechanism)
- Import bans verified via test_no_forbidden_imports.py (planned)
- Schema validation verified via test_contracts.py (planned)
- Forbidden field scan verified via model introspection tests (planned)
- Determinism verified via repeated-input tests (planned)
- Timeout enforcement verified via integration test (planned)

## 7. Next

- Implementation must not violate any boundary listed here
- Boundary violations are P0 blocking issues
- Any boundary relaxation requires re-review and new seal
- Boundary test suite is first implementation priority

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
