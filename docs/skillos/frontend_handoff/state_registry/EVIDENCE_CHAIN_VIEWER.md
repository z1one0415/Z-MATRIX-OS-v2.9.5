# Evidence Chain Viewer

## Purpose

The Evidence Chain Viewer provides verifiable provenance for every decision gate in the system. Each evidence node is content-hashed, source-classified, and linked to a specific gate. The chain forms an append-only Merkle tree, enabling tamper-evident audit trails.

## Schema

Refer to `skillos/frontend_handoff/state_registry/evidence_chain_schema.json` for the authoritative JSON Schema definition.

## Source Classes

| Source Class | Description |
|:--|:--|
| `COMMIT_LOG` | Git commit log entry |
| `RESEARCH_ARTIFACT` | Research output artifact (JSON report) |
| `AUDIT_REPORT` | Formal audit report |
| `VALIDATION_OUTPUT` | Factor validation run output |
| `FACTOR_RESULT` | Factor evaluation result |
| `HUMAN_REVIEW` | Human review and annotation |
| `DECISION_GATE` | Decision gate record |
| `EXTERNAL_REFERENCE` | External reference material |
| `RUNTIME_LOG` | Runtime log entry |
| `SCHEMA_DEFINITION` | Schema definition file |

## Evidence Node Fields

| Field | Type | Description |
|:--|:--|:--|
| `node_id` | string | Unique node identifier |
| `hash` | string | Content hash (SHA-256 by default) |
| `hash_algorithm` | enum | `SHA-256`, `SHA-512`, `BLAKE3` |
| `source_class` | enum | Evidence source classification |
| `no_real_source_flag` | boolean | `true` if node is a placeholder/stub |
| `linked_gate_id` | string | Associated gate ID |
| `artifact_path` | string | Filesystem path to evidence artifact |
| `commit_sha` | string | Git commit SHA that produced this evidence |
| `description` | string | Human-readable description |
| `verified_at` | datetime | Last verification timestamp |
| `verification_status` | enum | `UNVERIFIED`, `VERIFIED`, `STALE`, `CORRUPT` |

## Root Hash

The `root_hash` field is computed as `SHA-256` of all individual node hashes concatenated in order. This enables quick integrity verification: any tampering with any node will change the root hash.

## API Endpoint

```
GET /api/evidence-chain
```

Returns an `EvidenceChainDemo` object conforming to `evidence_chain_schema.json`.

## F7.2 Evidence Chain

The F7.2 evidence chain contains 11 nodes (one per gate), all with `no_real_source_flag: false` and `verification_status: VERIFIED`.

| Node ID | Linked Gate | Source Class |
|:--|:--|:--|
| `ev-F7.0-001` | `F7.0-logical-reconcile` | RESEARCH_ARTIFACT |
| `ev-F7.2-plan-001` | `F7.2-planning-review` | RESEARCH_ARTIFACT |
| `ev-F7.2-exec-001` | `F7.2-execution-plan` | RESEARCH_ARTIFACT |
| `ev-F7.2-exec-auth-001` | `F7.2-execution-auth` | RESEARCH_ARTIFACT |
| `ev-F7.2-final-auth-001` | `F7.2-final-exec-auth` | DECISION_GATE |
| `ev-F7.2-human-val-001` | `F7.2-human-val-auth` | HUMAN_REVIEW |
| `ev-F7.2-val-run-001` | `F7.2-val-readonly` | VALIDATION_OUTPUT |
| `ev-F7.2-audit-001` | `F7.2-val-audit` | AUDIT_REPORT |
| `ev-F7.2-safety-001` | `F7.2-safety-patch` | RESEARCH_ARTIFACT |
| `ev-F7.2-interpret-001` | `F7.2-human-interpret` | HUMAN_REVIEW |
| `ev-F7.2-decision-001` | `F7.2-decision-gate` | DECISION_GATE |

## Safety

- All evidence nodes in frontend demo data have `no_real_source_flag: false`
- Root hash is recomputable for integrity verification
- Evidence nodes are immutable once sealed
