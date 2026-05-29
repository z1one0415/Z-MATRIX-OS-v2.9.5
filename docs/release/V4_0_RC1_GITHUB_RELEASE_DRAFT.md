# Z-MATRIX-OS v4.0-rc1

## Release Type

**Research-only Release Candidate.**

This release is not production-ready.
This release does not enable broker runtime.
This release does not allow real trade execution.
This release remains paper-only and human-review-required.

## Target Evidence

| Field | Value |
|-------|-------|
| Tag | v4.0-rc1 |
| Target commit | f8796f714740b5e8c76ab53d768888a8de87dfdd |
| CI run | 26629922144 (success) |
| Scorecard | 100/100 |
| Integrity | POST_RC1_INTEGRITY_PASS |
| Post-tag commit | 7cfd5ab |

## Included

- Platform hardgates and repository constitution
- Data governance and evidence contracts
- Factor registry and promotion pipeline
- Research Experiment OS
- Parser-Scorer split architecture
- LLM subjective scoring ban protocol
- ZC35 catalyst lifecycle and sell-on-news defense
- ZC40 execution quality and limit-board fillability gates
- ZC45 proxy hedge and beta budget guardrails
- 12 independent Research Council reviewers (unique scoring_configs)
- 12 report templates and snapshot rendering
- Audit ZIP real file export
- IRF-01 through IRF-08 integration chains (all 8 verified)
- RC1 Readiness Audit (RA-0 through RA-8)
- Cloud CI evidence lock and parity closeout
- Post-RC1 release integrity audit (PRI-0 through PRI-6)

## Explicitly Excluded

- ❌ Production trading
- ❌ Broker integration
- ❌ Runtime execution
- ❌ Real trade execution
- ❌ Autonomous buy/sell
- ❌ Live market data streaming
- ❌ Order placement
- ❌ Position management
- ❌ Classifier production-chain modification

## Safety

```
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
Paper-only: TRUE
Human review required: TRUE
```

## Known Limitations

- DataForge, FactorFactory, ExecutionQuality, and AccountGovernance remain at DEPTH_PARTIAL (research-grade).
- 49 pre-existing legacy test failures documented in RC1 audit (non-blocking).
- GitHub legacy combined status is empty; GitHub Actions run evidence is the authoritative CI record.
- This RC1 is a research platform baseline, not a live trading system.

---

**⛔ This GitHub Release is a DRAFT. It must NOT be published without explicit human approval.**
