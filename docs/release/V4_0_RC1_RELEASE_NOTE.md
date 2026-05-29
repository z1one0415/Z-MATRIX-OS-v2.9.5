# Z-MATRIX-OS v4.0-rc1 Release Note

## Release Type

**Research-only Release Candidate.**

This release candidate marks the first fully audited V4.0 FINAL-HARDGATES integration baseline.

> ⚠️ It is NOT production-ready.
> ⚠️ It does NOT enable broker runtime.
> ⚠️ It does NOT allow real trade execution.
> ⚠️ It remains paper-only and human-review-required.

## Tag Evidence

| Field | Value |
|-------|-------|
| Tag | v4.0-rc1 |
| Target commit | f8796f714740b5e8c76ab53d768888a8de87dfdd |
| Repo | z1one0415/Z-MATRIX-OS-v2.9.5 |
| CI run | 26629922144 (success) |
| Scorecard | 100/100 |

## What Is Included

1. Platform hardgates and repository constitution.
2. Data governance and evidence contracts.
3. Factor registry and promotion pipeline.
4. Research Experiment OS.
5. B-Matrix current snapshot workbench.
6. D-Matrix data source plan.
7. Parser-Scorer split architecture.
8. LLM subjective scoring ban protocol.
9. ZC35 catalyst lifecycle and sell-on-news defense.
10. ZC40 execution quality and limit-board fillability gates.
11. ZC45 proxy hedge and beta budget guardrails.
12. 12 independent Research Council reviewers (unique scoring_configs).
13. 12 report templates and snapshot rendering.
14. Audit ZIP real file export (manifest + envelope + events + safety).
15. IRF-01 through IRF-08 integration chains (all 8 verified).
16. RC1 Readiness Audit (RA-0 through RA-8, 36 audit tests).
17. Cloud CI evidence lock and tag dry-run (E0).

## What Is Explicitly Excluded

- ❌ Real trading.
- ❌ Broker integration.
- ❌ Runtime execution.
- ❌ Production strategy modification.
- ❌ Classifier production chain modification.
- ❌ Autonomous buy/sell.
- ❌ Market data live streaming.
- ❌ Order placement and position management.

## Verification Summary

| Check | Result |
|-------|:------:|
| RC1 Readiness Scorecard | 100/100 |
| GitHub Actions CI | success (run 26629922144) |
| Safety deep scan | 463 files, 0 violations |
| Repository hygiene | PASS |
| Artifact exclusion | PASS |
| Cloud evidence lock | PASS |
| RC1 audit tests | 36/36 passed |

## Known Limitations

- Some modules remain at DEPTH_PARTIAL (DataForge, FactorFactory, ExecutionQuality, AccountGovernance) — sufficient for research, insufficient for production.
- 49 pre-existing legacy test failures documented in RC1 audit (non-blocking).
- GitHub legacy combined status may be empty; GitHub Actions run evidence (`26629922144`) is the authoritative CI record.
- This release is a research platform baseline, not a live trading system.

## Safety Statement

```
Production: BLOCKED
Broker/runtime: BLOCKED
Real trade: BLOCKED
Paper-only: TRUE
Human review required: TRUE
```

---

*Tagged by Z2 Hermes Research Kernel | 2026-05-29T21:07+08:00*
