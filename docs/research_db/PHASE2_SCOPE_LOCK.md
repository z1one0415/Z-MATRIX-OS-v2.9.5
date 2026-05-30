# Phase 2-A Scope Lock

> **Phase**: 2-A (Master Data Schema + Privacy Guardrails)
> **Status**: COMPLETE — no further expansion allowed before Phase 2-B
> **Date**: 2026-05-30

## Scope Definition

Phase 2-A delivers the **schema foundation** for master data, industry mapping, and chain taxonomy. All business logic, loaders, normalizers, and report generators are deferred to later batches.

## Files Created

| File | Type | Purpose |
|------|------|---------|
| `zmatrix/research_db/master_data/__init__.py` | Code | 4 Enums + 6 Dataclasses (SecurityMaster, TickerAlias, IndustryMapping, SectorMapping, ChainTaxonomy, ChainNodeMapping) |
| `templates/research_db/master_data/` (6 templates) | Data | CSV templates for each master data table |
| `tests/fixtures/master_data/` (6 fixtures) | Data | Synthetic sample data: 5 stocks (600519/000001/002472/300750/688981) |
| `tests/research_db/master_data/test_master_schema.py` | Test | Enum validation, dataclass creation, default values, forbidden token scan |
| `tests/research_db/master_data/test_private_master_data_guardrail.py` | Test | No xlsx/vendor tracked, production_allowed always False |
| `docs/research_db/PHASE2_SCOPE_LOCK.md` | Doc | This file |

## Explicitly NOT in Scope

- ❌ Loaders / importers (→ Phase 2-B)
- ❌ Normalizers / validators (→ Phase 2-B)
- ❌ Conflict detectors (→ Phase 2-C)
- ❌ Report generators (→ Phase 2-C)
- ❌ universe/raw, staging, normalized directories (→ Phase 2-B)
- ❌ Any business logic beyond schema definition
- ❌ Any real data import

## Safety State

```
real_trade_allowed=False
broker_order_allowed=False
runtime_enabled=False
auto_buy_allowed=False
auto_sell_allowed=False
production_allowed=False
paper_only=True
human_review_required=True
```

All 6 dataclasses have `production_allowed=False` enforced via `__post_init__` and default field values.

## Next Batch

Phase 2-B: Mapping Logic — universe_loader, normalizer, validator, chain classifier, benchmark resolver, peer builder.
