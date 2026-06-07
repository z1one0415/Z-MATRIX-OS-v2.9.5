# Z-SkillOS Level 4 Implementation Gate — Warning Side-Channel Path Spec

## Status

Z_SKILLOS_LEVEL4_IMPL_GATE_WARNING_SIDECHANNEL_SPEC_READY

## Purpose

Define the exact delivery mechanisms for Level 4 warnings. Level 4 must emit warnings only through approved side channels; never through result_envelope, caller response, or runtime exceptions.

## Allowed Delivery Paths

| Path | Target | Format | Visibility | Status |
|:--|:--|:--|:--|:--:|
| Internal audit file | `runtime_audit/level4_warnings.jsonl` | JSONL, one warning per line | File system only | CANDIDATE |
| Operator review report | `runtime_reports/level4_operator_review.md` | Markdown table | File system only | CANDIDATE |
| Side-channel bus | Future message queue | TBD | Internal services only | DEFER |

## Forbidden Delivery Paths

| Path | Rationale |
|:--|:--|
| result_envelope mutation | Violates audit-first contract |
| Caller response body | Violates operator-control boundary |
| Runtime exception / raise | Violates CONTINUE safety |
| stdout / stderr | Uncontrolled visibility |
| Broker / trade channel | Permanent boundary |
| Production log | Production linkage forbidden |
| Network / external API | Privacy boundary |

## Internal Audit File Spec

```
Path: runtime_audit/level4_warnings.jsonl
Format: One JSON object per line
Rotation: Daily, keep 30 days

Schema per warning:
{
  "warning_id": "uuid",
  "timestamp": "ISO-8601",
  "category": "SCHEMA_DRIFT|HASH_DRIFT|GOLDEN_MISMATCH|SEMANTIC_DRIFT|...",
  "severity": "INFO|NOTICE|WARN|ESCALATE_REVIEW",
  "source_gate": "gate identifier",
  "evidence_ref": "hash or file reference",
  "recommended_action": "human-readable suggestion",
  "caller_visibility": "INTERNAL_ONLY",
  "rollback_policy": "downgrade|suppress|retract",
  "created_by": "skillos_level4"
}

Forbidden fields: raw_prompt, user_data, output, account, broker, trading,
                  production_secrets, real_trade_payload, PII
```

## Operator Review Report Spec

```
Path: runtime_reports/level4_operator_review.md
Format: Markdown table, append-only
Trigger: On ESCALATE_REVIEW severity or on scheduled interval

Table columns:
| warning_id | timestamp | category | severity | source_gate | action |
```

## Side-Channel Bus (Future)

```
Status: DEFER
Preconditions: Internal audit file stable for 30+ days, no FP issues,
               operator review process validated
```

## Proof Requirements

| # | Test | Assertion |
|:--|:--|:--|
| SC-1 | Emit all categories to audit file | File contains valid JSONL |
| SC-2 | Emit ESCALATE_REVIEW to operator report | Report contains entry |
| SC-3 | result_envelope hash unchanged after emission | Pre/post hash equal |
| SC-4 | No stdout/stderr from warning path | Output capture empty |
| SC-5 | No broker/trade module imports | Static analysis clean |
| SC-6 | PII/raw_data absent from warning payload | Schema validation |
| SC-7 | File rotation respects 30-day retention | Old files removed |

## Constraints

- Disabled by default (LEVEL4_WARNING_ENABLED=false)
- Failure to write = CONTINUE silently (no crash)
- No network calls
- No external API access
- File write errors swallowed, never propagated
