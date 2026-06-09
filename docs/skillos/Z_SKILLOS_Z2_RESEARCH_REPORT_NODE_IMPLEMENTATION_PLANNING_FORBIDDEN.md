# Z2 Research Report Node Implementation Planning — FORBIDDEN

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
| Enforcement | Compile-time + runtime + CI |
| Severity | P0 security breach on violation |

## 2. Scope

This document is the canonical forbidden-field registry for the Z2 Research Report Node. Every field listed here MUST NOT appear in any model, contract, response, intermediate state, log output, or test fixture within the research_report_node module.

## 3. Dependency

- Forbidden list inherited from Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED
- Consistent with Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED constraints
- postmerge HEAD = c5f69f5

## 4. Boundary

Forbidden fields apply across ALL boundaries:
- Input models, output models, intermediate models
- Function parameters, return values, local variables with semantic meaning
- Log messages, error messages, debug output
- Test fixtures, test assertions, mock data
- Documentation examples, docstrings

## 5. Forbidden

### Forbidden Field Registry (14 items)

| # | Field Name | Category | Rationale |
|---|-----------|----------|-----------|
| 1 | alpha_claim | Trading signal | Implies tradeable alpha; Z2 is research-only |
| 2 | expected_return_claim | Trading signal | Implies forward return prediction for trading |
| 3 | buy_signal | Order generation | Direct trade instruction |
| 4 | sell_signal | Order generation | Direct trade instruction |
| 5 | position_weight | Portfolio mgmt | Implies allocation decision |
| 6 | order_signal | Order generation | Direct order routing |
| 7 | trade_instruction | Order generation | Direct trade command |
| 8 | paper_trade_order | Order generation | Even simulated orders forbidden |
| 9 | broker_action | Execution | Broker API interaction |
| 10 | portfolio_rebalance | Portfolio mgmt | Rebalance implies decision authority |
| 11 | real_trade_order | Execution | Real money order generation |
| 12 | production_decision | Decision authority | Production-level decision making |
| 13 | real_pnl | Execution tracking | Implies live tracking of trade results |
| 14 | trade_result | Execution tracking | Implies completed trade lifecycle |

### Forbidden Import Patterns

| # | Pattern | Rationale |
|---|---------|-----------|
| 1 | import requests / httpx / aiohttp | No network access |
| 2 | import socket | No network access |
| 3 | import subprocess | No process spawning |
| 4 | import sqlite3 / sqlalchemy / psycopg2 | No database access |
| 5 | from trading.* | No trading library access |
| 6 | from broker.* | No broker library access |
| 7 | from portfolio.* | No portfolio library access |
| 8 | from order.* | No order management access |

### Forbidden Behavioral Patterns

| # | Pattern | Rationale |
|---|---------|-----------|
| 1 | Writing to filesystem | Pure computation only |
| 2 | Reading environment variables at runtime (except kill-switch) | Deterministic behavior |
| 3 | Global mutable state | Thread safety and determinism |
| 4 | Implicit type coercion | Type safety |
| 5 | Catching and silencing exceptions | Fail-loud principle |

## 6. Proof

- test_no_forbidden_imports.py will scan all source files (planned)
- Model introspection will verify no forbidden field names exist (planned)
- CI grep scan will catch forbidden strings in any file (planned)
- Code review checklist includes forbidden-field verification
- Pydantic model_fields inspection covers runtime detection (planned)

## 7. Next

- Implementation MUST include test_no_forbidden_imports.py as first test
- Any attempt to add a forbidden field is auto-rejected
- Forbidden list is append-only; fields cannot be removed
- Quarterly audit of forbidden field compliance

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
