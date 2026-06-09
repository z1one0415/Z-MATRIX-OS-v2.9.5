# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — EVIDENCE_CHAIN

> Evidence chain hash propagation rules for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | EVIDENCE_CHAIN |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | REPORT_SCHEMA.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document defines the evidence chain that the Z2 Research Report Node must inherit,
extend, and propagate. The evidence chain ensures full traceability from B1 CompositionGraphResponse
source through Z2 report output to z9_review_snapshot_candidate.

Every hash in the chain is immutable once computed. The chain enforces no_alpha_claim
and no_trade_signal by including these as verified invariants in the hash computation.

---

## 3. Dependency / Evidence

### 3.1 Inherited Evidence Chain Fields (from B1)

The following fields MUST be inherited from B1 CompositionGraphResponse:

| # | Field | Source | Propagation |
|---|-------|--------|-------------|
| 1 | source_class | B1 response | Copied verbatim |
| 2 | no_real_source_flag | B1 response | Copied verbatim |
| 3 | fixture_source_commit | B1 response | Copied verbatim |
| 4 | request_hash | B1 response | Copied verbatim |
| 5 | response_hash_placeholder | B1 response | Copied verbatim |
| 6 | factor_decision_hash | B1 evidence | Copied verbatim |
| 7 | bridge_decision_hash | B1 evidence | Copied verbatim |
| 8 | graph_node_hash | B1 evidence | Copied verbatim |
| 9 | graph_edge_hash | B1 evidence | Copied verbatim |
| 10 | permission_tier | B1 evidence | Copied verbatim |
| 11 | forbidden_outputs_removed_hash | B1 evidence | Copied, then extended by Z2 |
| 12 | rollback_marker | B1 evidence | Copied verbatim |
| 13 | privacy_marker | B1 evidence | Copied verbatim |
| 14 | c1_handoff_marker | B1 evidence | Copied verbatim |

### 3.2 Z2-Generated Evidence Chain Fields

The following fields are COMPUTED by Z2 and APPENDED to the chain:

| # | Field | Computation | Purpose |
|---|-------|-------------|---------|
| 15 | z2_report_node_hash | SHA256(all report fields + inherited chain) | Report instance integrity |
| 16 | z2_report_section_hash | SHA256(section_id + content + metadata) per section | Section integrity |
| 17 | z2_report_evidence_hash | SHA256(all evidence refs + inherited hashes) | Evidence completeness |

### 3.3 Hash Propagation Rules

```
B1 source_class ─────────────────────────────────┐
B1 no_real_source_flag ──────────────────────────┤
B1 fixture_source_commit ────────────────────────┤
B1 request_hash ─────────────────────────────────┤
B1 response_hash_placeholder ────────────────────┤
B1 factor_decision_hash ─────────────────────────┤
B1 bridge_decision_hash ─────────────────────────┤
B1 graph_node_hash ──────────────────────────────┤
B1 graph_edge_hash ──────────────────────────────┤
B1 permission_tier ──────────────────────────────┼──→ z2_report_evidence_hash
B1 forbidden_outputs_removed_hash ───────────────┤
B1 rollback_marker ──────────────────────────────┤
B1 privacy_marker ───────────────────────────────┤
B1 c1_handoff_marker ────────────────────────────┤
Z2 section hashes (×12) ─────────────────────────┤
Z2 blocked_outputs_removed ──────────────────────┘
                                                   │
                                                   ▼
                                        z2_report_node_hash
```

---

## 4. Boundary

- No hash field may be modified after initial computation
- Hash computation must be deterministic (same input → same hash)
- All inherited fields must be present; missing fields → DENY_Z2_EVIDENCE_INCOMPLETE
- z2_report_node_hash must include no_alpha_claim and no_trade_signal flags in its input
- Chain must be serializable for z9_review_snapshot_candidate transmission

---

## 5. Forbidden Actions

- Modifying any inherited hash field
- Computing hashes with incomplete evidence chain
- Omitting any of the 14 inherited fields from the chain
- Skipping z2_report_node_hash computation
- Producing z9_review_snapshot_candidate without complete evidence chain
- Using non-deterministic hash computation (e.g., including timestamps in hash input)

---

## 6. Proof / Review Requirements

- Hash determinism must be tested with fixture data (same input → same output)
- All 14 inherited fields must be verified present in test fixtures
- z2_report_evidence_hash must change if any input hash changes
- z2_report_node_hash must change if any section content changes
- Evidence chain completeness must be verified before z9_review_snapshot_candidate emission

---

## 7. Next Legal Entry

- Proceed to CONFIDENCE_POLICY.md for confidence level assignment rules
- Evidence chain feeds into Z9_HANDOFF_PREP.md
- Hash integrity feeds into REVIEW_CHECKLIST.md verification items
