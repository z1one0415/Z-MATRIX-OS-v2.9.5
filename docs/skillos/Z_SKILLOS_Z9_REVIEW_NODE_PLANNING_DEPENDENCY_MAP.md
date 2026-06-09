# Z9 Review Node Planning — DEPENDENCY MAP

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Upstream Dependencies

| Dependency | Source | Interface | Required |
|---|---|---|---|
| z9_review_snapshot_candidate | Z2 report_node | Frozen snapshot dict | YES |
| report_node_id | Z2 | UUID string | YES |
| source_graph_hash | Z2 | SHA-256 | YES |
| factor_context_summary_hash | Z2 | SHA-256 | YES |
| evidence_chain_hash | Z2 | SHA-256 | YES |
| research_summary_hash | Z2 | SHA-256 | YES |
| risk_warning_hash | Z2 | SHA-256 | YES |
| confidence_level | Z2 | Float 0.0-1.0 | YES |
| confidence_reason | Z2 | String | YES |
| missing_evidence | Z2 | List[str] | YES |
| degradation_status | Z2 | Enum | YES |
| blocked_outputs_removed | Z2 | List[str] | YES |
| review_required | Z2 | Boolean | YES |
| review_reason | Z2 | String | YES |
| readonly_only | Z2 | Boolean (always True) | YES |

## 2. Downstream Consumers

| Consumer | Interface | Nature |
|---|---|---|
| z2_feedback_candidate | Advisory dict | Readonly |
| Human reviewer | Rendered report | Read-only |
| Audit log | Immutable append | Readonly |

## 3. Forbidden Dependencies

- NO dependency on Z8 execution engine
- NO dependency on broker API
- NO dependency on position manager
- NO dependency on trade_result pipeline
- NO dependency on V3 sandbox
- NO dependency on real PnL data source
- DENY_Z9_TRADE_RESULT_FORBIDDEN enforced at import level

## 4. Internal Module Dependencies

```
review_node/
├── __init__.py          → imports registry
├── constants.py         → no internal deps
├── config.py            → constants
├── models.py            → constants, config
├── contracts.py         → models, constants
├── evidence.py          → models, contracts
├── attribution.py       → models, constants
├── degradation.py       → models, constants, config
├── review_builder.py    → evidence, attribution, degradation, contracts
├── z2_feedback.py       → models, review_builder
├── kill_switch.py       → constants, config
└── registry.py          → all modules
```

## 5. Hash Chain Dependencies

The evidence chain inherits from Z2 snapshot:
- source_graph_hash → factor_context_summary_hash → evidence_chain_hash
- research_summary_hash → risk_warning_hash
- z9_review_node_hash (produced by Z9)
- z9_review_section_hash (produced per section)
- z9_feedback_candidate_hash (produced for feedback)
- rollback_marker (inherited, never modified)
- privacy_marker (inherited, never modified)

## 6. Kill Switch Dependencies

- DENY_Z9_SOURCE_FORBIDDEN: blocks if source is not z9_review_snapshot_candidate
- DENY_Z9_REAL_SOURCE_FORBIDDEN: blocks if real trade data detected
- DENY_Z9_OUTPUTS_UNSAFE: blocks if forbidden output fields present
- DENY_Z9_EXECUTION_FORBIDDEN: blocks any execution path
- DENY_Z9_EVIDENCE_INCOMPLETE: blocks if evidence hash missing
- DISABLED_DEFAULT_NOOP: default state, no review produced

## 7. Version Compatibility

- Z-MATRIX-OS: v2.9.5
- Z2 Report Node: v2.1+ (must emit z9_review_snapshot_candidate)
- Python: 3.11+
- No external API dependencies (pure logic node)
- no_trade_result marker required in all outputs
- Z9 feedback is advisory and readonly
