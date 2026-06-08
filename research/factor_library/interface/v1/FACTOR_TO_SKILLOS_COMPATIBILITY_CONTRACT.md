# Factor to SkillOS Compatibility Contract v1

**Status**: READONLY_CONTRACT | **SkillOS Adapter**: NOT_IMPLEMENTED

## 1. Purpose

Define the boundary between the Factor Library and SkillOS Capability Invocation OS. SkillOS must not execute, modify, or generate alpha from any factor. SkillOS may only read factor artifacts through the interface contract.

## 2. SkillOS Restrictions

SkillOS currently:
- ✅ MUST NOT implement a factor adapter.
- ✅ MUST NOT actively execute any factor formula.
- ✅ MUST NOT modify any factor lifecycle state.
- ✅ MUST NOT generate any alpha claim from factor output.
- ✅ MUST NOT generate any trade signal from factor output.
- ✅ MUST NOT bypass the application contract gate.
- ✅ MUST only consume factor artifacts in readonly mode.

## 3. Allowed Readonly Intents

The following intents are allowed for future SkillOS readonly consumption:

| Intent | Purpose |
|--------|---------|
| `REGISTRY_READ` | Read factor registry metadata |
| `EVIDENCE_READ` | Read evidence envelope |
| `VALIDATION_SUMMARY` | Read validation snapshot |
| `GUARDRAIL_SUMMARY` | Read guardrail profile |
| `CANDIDATE_MONITOR` | Read monitoring state |
| `RESEARCH_CONTEXT` | Provide factor context for research prompts |
| `SCORING_CONTEXT_DRY_PLAN` | Scoring context (no execution) |
| `COMPOSITION_GRAPH_DRY_PLAN` | Composite research graph (no execution) |

## 4. Forbidden Intents

| Intent | Reason |
|--------|--------|
| `ALPHA_SIGNAL` | Prohibited by application contract |
| `ORDER_SIGNAL` | Prohibited by application contract |
| `PORTFOLIO_WEIGHT` | Prohibited by application contract |
| `PAPER_TRADING` | Prohibited by application contract |
| `BROKER_RUNTIME` | Prohibited by application contract |
| `REAL_TRADE` | Prohibited by application contract |
| `PRODUCTION` | Prohibited by application contract |

## 5. Enforcement

- All factor artifacts include `alpha_claim_allowed: false`, `production: "BLOCKED"`, `broker_runtime: "BLOCKED"`, `real_trade: "BLOCKED"`.
- Any SkillOS code attempting to bypass these flags would violate its charter.
- This contract is reviewed at each Factor Library milestone.
