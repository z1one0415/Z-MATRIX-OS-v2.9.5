# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — BLOCKED_OUTPUT_POLICY

> Blocked output detection and removal policy for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | BLOCKED_OUTPUT_POLICY |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | CONFIDENCE_POLICY.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document defines the blocked output detection and removal policy. Every report
produced by the Z2 Research Report Node must pass through a blocked output scanner
before emission. The scanner ensures no_alpha_claim and no_trade_signal invariants
are enforced at the output boundary.

The blocked_outputs_removed field is mandatory in every report and every section,
recording what was detected and removed. The z2_report_node_hash includes the
blocked_outputs_removed content in its computation.

---

## 3. Dependency / Evidence

### 3.1 Forbidden Output Blocklist

The following output fields/patterns MUST be detected and blocked:

| # | Blocked Output | Pattern Match | Action |
|---|---------------|---------------|--------|
| 1 | alpha_claim | Field name or content containing "alpha_claim" | Remove + log |
| 2 | expected_return_claim | Field name or content pattern | Remove + log |
| 3 | buy_signal | Field name or content pattern | Remove + log |
| 4 | sell_signal | Field name or content pattern | Remove + log |
| 5 | position_weight | Field name or numeric weight pattern | Remove + log |
| 6 | order_signal | Field name or order pattern | Remove + log |
| 7 | trade_instruction | Field name or instruction pattern | Remove + log |
| 8 | paper_trade_order | Field name or order pattern | Remove + log |
| 9 | broker_action | Field name or action pattern | Remove + log |
| 10 | portfolio_rebalance | Field name or rebalance pattern | Remove + log |
| 11 | real_trade_order | Field name or order pattern | Remove + log |
| 12 | production_decision | Field name or decision pattern | Remove + log |

### 3.2 Detection Pipeline

```
Report Generation
       │
       ▼
┌──────────────────────┐
│ Section Builder       │ ← Generates raw section content
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Blocked Output Scanner│ ← Scans each section for forbidden patterns
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Removal & Logging     │ ← Removes detected items, logs to blocked_outputs_removed
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Hash Computation      │ ← Computes z2_report_node_hash including removals
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Output Emission       │ ← Clean output with blocked_outputs_removed populated
└──────────────────────┘
```

### 3.3 blocked_outputs_removed Field Format

```json
{
  "blocked_outputs_removed": [
    {
      "field_name": "alpha_claim",
      "section_id": 6,
      "detection_method": "field_name_match",
      "action_taken": "removed"
    }
  ]
}
```

---

## 4. Boundary

- Scanner runs AFTER section generation, BEFORE hash computation
- Scanner is mandatory — cannot be bypassed or disabled
- Even if no blocked outputs found, blocked_outputs_removed must be present (empty list)
- Scanner operates on field names AND content patterns
- forbidden_outputs_removed_hash computed from the final blocked_outputs_removed content
- B1 CompositionGraphResponse inherited forbidden_outputs_removed_hash is preserved separately

---

## 5. Forbidden Actions

- Bypassing the blocked output scanner
- Emitting output without blocked_outputs_removed field
- Suppressing detection logging
- Allowing any of the 12 forbidden outputs through the scanner
- Modifying blocked_outputs_removed after z2_report_node_hash computation
- Disabling the scanner via configuration or environment variable

---

## 6. Proof / Review Requirements

- Test each of the 12 forbidden outputs individually (inject → verify blocked)
- Test with clean input (verify empty blocked_outputs_removed list)
- Test with multiple simultaneous forbidden outputs
- Verify forbidden_outputs_removed_hash changes when blocked items change
- Verify z2_report_node_hash includes blocked_outputs_removed in computation
- Test scanner cannot be bypassed via configuration

---

## 7. Next Legal Entry

- Proceed to DEGRADATION_POLICY.md for degradation decision rules
- Blocked output policy feeds into z9_review_snapshot_candidate (blocked_outputs_removed field)
- Scanner behavior verified in REVIEW_CHECKLIST.md
