# Hermes Memory Kernel Architecture v1.0

## Goal

Upgrade Hermes from inventory-only to read-only / preview-only Memory Kernel.

## Scope

- Core Memory Preview
- Working Context Preview
- Learned Heuristics Retrieval
- Prompt Patch Preview
- MemoryCandidate Preview
- CalibrationEvent Preview
- EventStore event packaging

## Not In Scope

- No Hermes memory write
- No memory_bank.json write
- No Z9 write
- No auto calibration
- No auto prompt injection
- No B/R/D / Z8 / G18 / Account Constitution modification
- No real trade

## Relationships

```
EventStore = event ledger (v2.9.11)
  ↓
Hermes Memory Kernel = memory read + candidate generation (v2.9.12, read-only)
  ↓
Approval Loop = future version (decides whether to write long-term memory)
  ↓
Prompt Hot-Patching = future version (decides whether to inject)
```

## Packages

- zmatrix/hermes_kernel/ — core schemas, validators, memory preview modules
- zmatrix/hermes_memory/ — MemoryCandidate, CalibrationEvent, Kernel coordinator, EventStore adapters
- docs/contracts/ — 7 contract documents
- docs/architecture/ — This document
