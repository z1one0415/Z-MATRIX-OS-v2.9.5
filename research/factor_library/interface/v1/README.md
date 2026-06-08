# Factor Application Standard Interface v1

**Status**: V13.F5.0.1 | **Base**: 8140ecab | **Mode**: DOCS_SCHEMA_INTERFACE_ONLY

## Purpose

Standardize how all factors in the Z-MATRIX-OS factor library are registered, validated, monitored, and consumed across research pipelines. Every factor — frozen, monitore, pre-interface, or source-audit — must conform to these interfaces before entering candidate review or any downstream consumption.

## Scope

- All 40 factors (Core 20 + Extended 20) are subject to this interface.
- All Batch1/Batch2/Batch3 artifacts are pre-interface until backfilled.
- This interface does not implement SkillOS adapters.
- This interface does not modify existing runtime artifacts retroactively.

## Key Documents

| Document | Purpose |
|----------|---------|
| `FACTOR_APPLICATION_STANDARD_INTERFACE_V1.md` | This file — top-level standard definition |
| `FACTOR_LIFECYCLE_STATE_MACHINE.md` | Canonical lifecycle from NOT_EXECUTED to REJECTED |
| `FACTOR_TO_SKILLOS_COMPATIBILITY_CONTRACT.md` | SkillOS readonly contract |
| `FACTOR_MAINLINE_PR_CHECKLIST.md` | PR checklist for factor library changes |
| `FACTOR_INTERFACE_CI_GATE_PLAN.md` | CI gate configuration plan |

## Interface Objects (11 schemas)

| Schema | Purpose |
|--------|---------|
| `factor_manifest.schema.json` | Factor identity, family, hypothesis, formula contract |
| `factor_family_profile.schema.json` | Family grouping, overlap risk, diversification boundary |
| `factor_validation_snapshot.schema.json` | PIT/coverage/IC/bucket/spread snapshot |
| `factor_guardrail_profile.schema.json` | Gates, monitoring rules, suspension thresholds |
| `factor_application_contract.schema.json` | Allowed/blocked application modes |
| `factor_invocation_request.schema.json` | Readonly invocation request |
| `factor_invocation_response.schema.json` | Readonly invocation response |
| `factor_evidence_envelope.schema.json` | Proof chain — materialization/PIT/coverage/validation |
| `factor_batch_closeout.schema.json` | Batch closeout summary |
| `factor_registry.schema.json` | Complete factor registry |
| `factor_family_registry.schema.json` | Factor family registry |

## Blocked Modes (universal for all factors)

```json
{
 "blocked_application_modes": [
  "ALPHA_SIGNAL",
  "PORTFOLIO_WEIGHT",
  "ORDER_SIGNAL",
  "PAPER_TRADING",
  "BROKER_RUNTIME",
  "REAL_TRADE",
  "PRODUCTION"
 ],
 "blocked_outputs": [
  "buy_signal",
  "sell_signal",
  "position_weight",
  "expected_return_claim",
  "alpha_claim"
 ],
 "blocked_downstream_consumers": [
  "Z8_EXECUTION_RUNTIME",
  "V3_TRADE_SANDBOX",
  "BROKER",
  "REAL_TRADE"
 ]
}
```

## Versioning

- Current: v1
- Schema evolution: additive only. No breaking changes to existing fields.
- Version stored in `pipeline_signature` of each artifact.

## Enforcement

- All factor library PRs must include `FACTOR_MAINLINE_PR_CHECKLIST.md` checks.
- All new factors must produce interface-compliant manifest, validation snapshot, guardrail profile, and application contract.
- Pre-interface artifacts (all Batch3, F17-F20 source audits) must be backfilled before candidate review.
