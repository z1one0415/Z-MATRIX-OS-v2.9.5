# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — SCOPE

> Detailed scope definition for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | SCOPE |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | OVERVIEW.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

### 2.1 In-Scope Capabilities

The Z2 Research Report Node SHALL:

1. Accept B1 CompositionGraphResponse as its sole structured data input
2. Parse B1 graph evidence chain for report construction
3. Accept A1 bridge evidence only when transited through B1
4. Accept Factor Library readonly metadata only through B1/A1 path
5. Accept optional future FactorEvaluationMatrix readonly handoff (when available)
6. Accept optional future Small Real Sample Read-Only summary (when available)
7. Accept static user research question context at runtime
8. Maintain local in-memory report template for section construction
9. Produce 12-section structured research reports
10. Compute z2_report_node_hash for each report instance
11. Compute z2_report_section_hash for each report section
12. Compute z2_report_evidence_hash for evidence chain integrity
13. Produce z9_review_snapshot_candidate for downstream Z9 review
14. Enforce no_alpha_claim = true invariant
15. Enforce no_trade_signal = true invariant
16. Apply degradation decisions when evidence is incomplete
17. Remove blocked outputs before emission (blocked_outputs_removed)
18. Report confidence_level restricted to LOW / MEDIUM / HIGH_WITH_STRUCTURE_ONLY

### 2.2 Out-of-Scope

The Z2 Research Report Node SHALL NOT:

1. Generate investment advice of any kind
2. Produce trade signals, buy/sell recommendations
3. Calculate position weights or portfolio allocations
4. Access broker systems or trading infrastructure
5. Access production decision systems
6. Access real returns, real trades, or paper trade systems
7. Access Z8, Z9, or V3 runtime internals directly
8. Consume FactorInvocationResponse directly
9. Read raw factor values from any source
10. Read research/factor_library files directly (only through B1/A1 metadata)

### 2.3 Scope Invariants

- readonly_only = true (always)
- no_alpha_claim = true (always)
- no_trade_signal = true (always)
- Confidence never exceeds HIGH_WITH_STRUCTURE_ONLY
- All evidence must trace to B1 CompositionGraphResponse origin

---

## 3. Dependency / Evidence

| Layer | Component | Access Mode |
|-------|-----------|-------------|
| Primary | B1 CompositionGraphResponse | Direct consumption |
| Secondary | B1 graph evidence chain | Inherited |
| Tertiary | A1 bridge evidence | Through B1 only |
| Quaternary | Factor Library metadata | Readonly through B1/A1 |
| Future-1 | FactorEvaluationMatrix | Optional readonly handoff |
| Future-2 | Small Real Sample summary | Optional readonly |
| Runtime | User research question | Static context |
| Internal | Report template | In-memory |

All dependencies trace to postmerge HEAD = 74c27fa.

---

## 4. Boundary

### Hard Boundaries:
- No network I/O to external trading systems
- No file system writes outside report output directory
- No direct database access to factor stores
- No import of forbidden modules (broker, trading, execution)
- No runtime modification of evidence chain hashes

### Soft Boundaries:
- Report length advisory limits (configurable)
- Section ordering preference (configurable within schema)
- Confidence threshold for z9_review_snapshot_candidate emission

---

## 5. Forbidden Actions

| Action | Reason | Detection Method |
|--------|--------|-----------------|
| Import broker modules | Production safety | test_no_forbidden_imports.py |
| Emit alpha_claim | Regulatory/safety | Contract validation |
| Emit trade_signal | Regulatory/safety | Contract validation |
| Emit position_weight | Scope violation | Output schema enforcement |
| Access raw factors | Input contract violation | Import guard + runtime check |
| Modify evidence hashes | Integrity violation | Hash verification |
| Skip degradation check | Safety bypass | Mandatory pipeline step |
| Emit without blocked_outputs_removed | Safety violation | Output validator |

---

## 6. Proof / Review Requirements

- Scope document must enumerate all in-scope and out-of-scope items
- Each in-scope item must map to at least one test in TEST_AND_PROOF_PLAN.md
- Each out-of-scope item must have a corresponding forbidden action check
- Boundary enforcement must be verifiable through static analysis
- z2_report_node_hash must be deterministically reproducible

---

## 7. Next Legal Entry

- Proceed to DEPENDENCY_MAP.md for detailed dependency graph
- All scope items feed into INPUT_CONTRACT.md and OUTPUT_CONTRACT.md
- Scope violations detected at review gate block merge
