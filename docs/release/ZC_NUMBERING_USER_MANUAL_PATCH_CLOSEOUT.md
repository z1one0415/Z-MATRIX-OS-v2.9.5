# ZC Numbering & User Manual Patch v1.1 Closeout

| Field | Value |
|-------|-------|
| Patch name | ZC Numbering & User Manual Patch v1.1 — Post-RC1 Safe |
| Patch status | PASS |
| Date | 2026-05-29T22:28+08:00 |

## Files

| File | Status |
|------|:--:|
| `docs/manuals/ZMATRIX_USER_OPERATION_MANUAL_V1.md` | ✅ Added |
| `docs/architecture/ZC_NUMBERING_MAP_V1.md` | ✅ Added |
| `docs/upgrade/V40_CONTENT_ASSET_INDEX.md` | ✅ Synchronized |
| `scripts/verify_zc_numbering_user_manual_patch.sh` | ✅ Added |
| `tests/docs/test_zc_numbering_user_manual_patch.py` | ✅ Added |

## Key Fixes

| Issue | Resolution |
|-------|------|
| ZC numbering chain missing from manual | All ZC00-ZC50/ZSC mapped |
| ZC30 MultiStrategy conflict | ZC30=FactorFactory, ZC31=MultiStrategy, ZC32=PortfolioOptimizer |
| Asset index status stale | Updated to V4.0-RC1_TAGGED_RESEARCH_ONLY |
| AutoCaseForge status ambiguous | PLANNED_NOT_IMPLEMENTED |
| ZC35-v2.1 scope unclear | RESEARCH_PROTOTYPE_EXCLUDED_FROM_RC1 |

## Safety

| Gate | Value |
|------|:------:|
| RC1 tag | v4.0-rc1 |
| Tag target | f8796f714740b5e8c76ab53d768888a8de87dfdd |
| Tag moved | FALSE |
| Tag retagged | FALSE |
| Production | BLOCKED |
| Broker/runtime | BLOCKED |
| Real trade | BLOCKED |
| Paper-only | TRUE |

## Patch v1.1.1 — Markdown Table Format Fix

Status: PASS
Scope: Documentation format only
File fixed: docs/upgrade/V40_CONTENT_ASSET_INDEX.md
Issue: Asset Index Markdown table header had 4 columns but separator had 3 columns.
Fix: Updated separator to `|---|---|---|---|`.

No business logic changed.
No strategy logic changed.
No tag moved.
No retag performed.
Production remains BLOCKED.
Broker/runtime remains BLOCKED.
Real trade remains BLOCKED.
