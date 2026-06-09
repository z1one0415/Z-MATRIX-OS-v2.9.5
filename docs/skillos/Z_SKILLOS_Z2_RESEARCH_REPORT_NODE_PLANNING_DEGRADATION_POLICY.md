# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — DEGRADATION_POLICY

> Degradation decision policy for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | DEGRADATION_POLICY |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | BLOCKED_OUTPUT_POLICY.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document defines all degradation decisions available to the Z2 Research Report Node.
Degradation decisions determine whether a report can be generated, and in what mode,
given the state of inputs, evidence, and safety checks.

The default state is DISABLED_DEFAULT_NOOP — no report is generated unless explicitly
enabled. This follows the B1 pattern of disabled-by-default safety. The node consumes
B1 CompositionGraphResponse and must validate it before proceeding.

---

## 3. Dependency / Evidence

### 3.1 Degradation Decisions (Exhaustive)

| # | Decision | Meaning | Trigger Condition |
|---|----------|---------|-------------------|
| 1 | ALLOW_Z2_READONLY_REPORT | Full readonly report permitted | All evidence present, no safety violations, B1 valid |
| 2 | ALLOW_Z2_DEGRADED_REPORT | Partial report with gaps noted | Some optional evidence missing, no safety violations |
| 3 | DENY_Z2_SOURCE_FORBIDDEN | Report denied: forbidden source | Input contains forbidden source type (not B1) |
| 4 | DENY_Z2_REAL_SOURCE_FORBIDDEN | Report denied: real data source | no_real_source_flag violated or real data detected |
| 5 | DENY_Z2_OUTPUTS_UNSAFE | Report denied: unsafe outputs | Forbidden output detected that cannot be removed |
| 6 | DENY_Z2_GRAPH_DENIED | Report denied: graph access denied | permission_tier insufficient or graph unavailable |
| 7 | DENY_Z2_EVIDENCE_INCOMPLETE | Report denied: evidence gaps | Mandatory evidence chain fields missing |
| 8 | DENY_Z2_EXECUTION_FORBIDDEN | Report denied: execution detected | Any execution/trade intent detected in pipeline |
| 9 | DISABLED_DEFAULT_NOOP | Default: no operation | Node not explicitly enabled (startup state) |

### 3.2 Decision Priority (highest to lowest)

1. DISABLED_DEFAULT_NOOP (if not enabled → immediate return)
2. DENY_Z2_EXECUTION_FORBIDDEN (execution intent → immediate reject)
3. DENY_Z2_SOURCE_FORBIDDEN (wrong source → reject)
4. DENY_Z2_REAL_SOURCE_FORBIDDEN (real data → reject)
5. DENY_Z2_OUTPUTS_UNSAFE (unsafe outputs → reject)
6. DENY_Z2_GRAPH_DENIED (access denied → reject)
7. DENY_Z2_EVIDENCE_INCOMPLETE (evidence gaps → reject)
8. ALLOW_Z2_DEGRADED_REPORT (partial evidence → degraded report)
9. ALLOW_Z2_READONLY_REPORT (full evidence → full report)

### 3.3 Degradation Flow

```
Input received
     │
     ▼
Is node enabled? ──NO──→ DISABLED_DEFAULT_NOOP (return empty)
     │ YES
     ▼
Execution intent? ──YES──→ DENY_Z2_EXECUTION_FORBIDDEN
     │ NO
     ▼
Source is B1? ──NO──→ DENY_Z2_SOURCE_FORBIDDEN
     │ YES
     ▼
Real source? ──YES──→ DENY_Z2_REAL_SOURCE_FORBIDDEN
     │ NO
     ▼
Outputs safe? ──NO──→ DENY_Z2_OUTPUTS_UNSAFE
     │ YES
     ▼
Graph access? ──NO──→ DENY_Z2_GRAPH_DENIED
     │ YES
     ▼
Evidence complete? ──NO──→ DENY_Z2_EVIDENCE_INCOMPLETE (if mandatory)
     │                  └──→ ALLOW_Z2_DEGRADED_REPORT (if optional only)
     │ YES
     ▼
ALLOW_Z2_READONLY_REPORT
```

---

## 4. Boundary

- Default state is ALWAYS DISABLED_DEFAULT_NOOP
- DENY decisions are terminal — no report is emitted
- ALLOW_Z2_DEGRADED_REPORT still requires no_alpha_claim = true, no_trade_signal = true
- degradation_status is included in z2_report_node_hash computation
- degradation_status is propagated to z9_review_snapshot_candidate
- Only ALLOW decisions permit z9_review_snapshot_candidate generation

---

## 5. Forbidden Actions

- Defaulting to ALLOW without explicit enablement
- Skipping degradation check pipeline
- Emitting report under any DENY decision
- Overriding DENY decisions via configuration
- Generating z9_review_snapshot_candidate under DENY decisions
- Treating DISABLED_DEFAULT_NOOP as an error (it is normal default behavior)

---

## 6. Proof / Review Requirements

- Test each of the 9 degradation decisions with dedicated fixtures
- Test priority ordering (higher priority DENY overrides lower ALLOW)
- Test DISABLED_DEFAULT_NOOP returns empty/noop output
- Test that DENY decisions prevent z9_review_snapshot_candidate generation
- Test that ALLOW_Z2_DEGRADED_REPORT still enforces all safety invariants
- Verify degradation_status in z2_report_node_hash computation

---

## 7. Next Legal Entry

- Proceed to Z9_HANDOFF_PREP.md for Z9 review snapshot preparation
- Degradation decisions feed into confidence_level assignment
- Degradation behavior verified in TEST_AND_PROOF_PLAN.md
