# Factor Application Standard Interface v1

## 1. Interface Purpose

This document defines the **Factor Application Standard Interface v1** for the Z-MATRIX-OS factor library. All factors — frozen, monitored, pre-interface, or source-audit — must conform before entering candidate review or any downstream consumption.

## 2. Interface Contract

Every factor MUST produce the following artifacts before it can be considered for candidate review:

| Artifact | Schema | Required For |
|----------|--------|:------------:|
| Factor Manifest | `factor_manifest.schema.json` | Candidate review |
| Factor Family Profile | `factor_family_profile.schema.json` | Family registration |
| Validation Snapshot | `factor_validation_snapshot.schema.json` | Candidate review |
| Guardrail Profile | `factor_guardrail_profile.schema.json` | Freeze review |
| Application Contract | `factor_application_contract.schema.json` | Any review |
| Evidence Envelope | `factor_evidence_envelope.schema.json` | Freeze review |

## 3. Blocked Application Modes

The following application modes are **blocked for ALL factors** in the library:

- `ALPHA_SIGNAL` — No alpha claim generation
- `PORTFOLIO_WEIGHT` — No portfolio weight assignment
- `ORDER_SIGNAL` — No order signal generation
- `PAPER_TRADING` — No paper trading
- `BROKER_RUNTIME` — No broker runtime
- `REAL_TRADE` — No real trade
- `PRODUCTION` — No production deployment

## 4. Blocked Outputs

- `buy_signal`
- `sell_signal`
- `position_weight`
- `expected_return_claim`
- `alpha_claim`

## 5. Blocked Downstream Consumers

- `Z8_EXECUTION_RUNTIME`
- `V3_TRADE_SANDBOX`
- `BROKER`
- `REAL_TRADE`

## 6. Schema Compliance

All JSON artifacts must:

1. Conform to JSON Schema draft 2020-12.
2. Include `pipeline_signature` field.
3. Include `alpha_claim_allowed: false`.
4. Include `production: "BLOCKED"`.
5. Include `broker_runtime: "BLOCKED"`.
6. Include `real_trade: "BLOCKED"`.

## 7. Pre-Interface Artifacts

Factors with `pre_interface_artifacts: true` exist in the factor library but have not been backfilled to interface v1. They may NOT enter candidate review or any downstream consumption until backfilled.

Pre-interface factors as of v1:
- F21–F34 (Batch3, pending F5.1.2 backfill)
- F17–F20 (source audit, pending future gate)

## 8. Interface Evolution

- Current version: v1
- Schema changes must be additive only.
- Version tracked via `pipeline_signature`.
- Breaking changes require v2 interface.
