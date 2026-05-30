# Research OS V3 Whitepaper

## Abstract

Research OS V3 is a **personal quantitative research operating system** designed to close the loop from raw data to validated investment decisions. It is NOT a trading bot, broker interface, or production execution platform. It operates entirely in **paper-only research mode**.

## System Goals

1. **Truth**: Reconstruct 5-year personal trading reality (Account Truth)
2. **Validation**: Verify every signal, factor, and thesis with strict outcome horizons
3. **Attribution**: Decompose returns into market/industry/selection alpha
4. **Reproducibility**: Every experiment is replayable with deterministic hash chains
5. **Council**: 12 independent reviewers challenge every thesis
6. **Evolution**: Machine-discovered patterns generate new hypotheses

## Theoretical Framework

The Research OS is built on four pillars:

### Pillar 1: Truth-First Data
All research starts from verified account data (broker exports, positions, cashflows). No synthetic data enters the main pipeline without explicit marking.

### Pillar 2: Strict Outcome Horizons
T20 requires 20 forward trading days. T60 requires 60. No fallback. No last-price substitution. Insufficient windows are blocked, not approximated.

### Pillar 3: Append-Only Immutability
All decisions, predictions, and council verdicts are recorded in append-only ledgers with SHA256 hash chains. Nothing is overwritten.

### Pillar 4: Devil's Advocate Mandate
Every council decision must include a counter-argument. No thesis passes without challenge.

## Architecture

```
Layer 6: Evolution (hypothesis evolution, pattern mining, meta research)
Layer 5: Operations (ROL: registry, monitor, workflow, memory)
Layer 4: Decision Intelligence (thesis, prediction market, forecaster ranking)
Layer 3: Portfolio (factory, reality, capacity/liquidity/drift)
Layer 2: Research (account truth, master data, market, outcome, attribution, replay)
Layer 1: Foundation (council, alpha factory, factor foundation, cockpit)
Layer 0: Governance (constitution, policies, guardrails, no-production boundary)
```

## Key Metrics (as of V3)

- Modules: 130+
- Test cases: 1,190
- Test coverage: 97%
- Production: BLOCKED
- Broker/Runtime/RealTrade: BLOCKED
- Paper-only: TRUE

## Boundary Conditions

- Does NOT execute real trades
- Does NOT connect to brokers
- Does NOT run as a daemon/runtime
- Does NOT auto-buy or auto-sell
- All output is research-only

## Future Directions

The Research OS V3 architecture is designed for two natural extensions:
1. **Alpha Factory**: Automated factor lifecycle (discover → validate → promote → retire)
2. **Knowledge Compounding**: Pattern mining feeds hypothesis evolution, creating a self-improving research loop

Neither extension requires breaking the Paper-Only boundary.
