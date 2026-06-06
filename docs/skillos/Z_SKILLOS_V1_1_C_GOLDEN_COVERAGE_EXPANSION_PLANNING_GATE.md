# Z-SkillOS v1.1-C Golden Coverage Expansion Planning Gate

## Status

Z_SKILLOS_V1_1_C_COVERAGE_PLANNING_GATE_READY

## Current Baseline

- v1.1-B.x drift CI integration: SEALED (`48438d6`)
- Current golden regression: 12 cases, 12 domains
- v1.0 golden hash lock: 4 cases
- Level 2 CI integration reached
- Level 3-5: BLOCKED

## Expansion Targets

| Option | Cases | Domains | Risk |
|:--|:--:|:--:|:--|
| A (minimal) | 12 → 18 | 12 → 14 | Low |
| B (recommended) | 12 → 24 | 12 → 16+ | Low |
| C (ambitious) | 12 → 32 | 12 → 17 | Medium |
| D (full) | 12 → 104 | 12 → 17 | High |

**Recommendation: Option B — 24 cases, 16+ domains.**

## Selection Policy

1. All skill_ids must be registry-exact (from `skill_contract_registry.json`)
2. Priority: R0_READ > R1_ANNOTATE > R2_DRAFT
3. Exclude: narrative renderer, write/proposal skills
4. Prefer: uncovered domains first
5. Each new case auto-generated with expected hashes

## Key Decisions

| # | Question | Recommended |
|:--:|------|:--:|
| 1 | Target: 24 or 32 cases? | 24 |
| 2 | Prioritize uncovered domains? | Yes |
| 3 | Registry-exact only? | Yes (lesson from v1.0-B gate drift) |
| 4 | Exclude narrative/write skills? | Yes |
| 5 | Auto-generate expected hashes? | Yes (via v1.0-C skill_hashing) |
| 6 | New baseline snapshot? | Yes |
| 7 | Add to CI wrapper? | Yes, after standalone verified |

## Decision

PENDING

- [ ] GO: allow v1.1-C implementation — 24 registry-exact cases
- [ ] NO-GO: remain at 12 cases

## Explicit Non-Scope

- no implementation
- no 104-case full coverage
- no runtime integration
- no hard enforcement
- no invoke_skill / result_envelope
- no production / broker / real_trade
