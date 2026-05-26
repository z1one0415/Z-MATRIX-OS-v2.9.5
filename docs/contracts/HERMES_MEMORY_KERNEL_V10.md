# Hermes Memory Kernel Contract v1.0 — Read-Only / Preview-Only Coordinator

## Fields

kernel_id, kernel_version, mode, task_context, core_memory_preview, working_context_preview, relevant_heuristics, prompt_patch_preview, memory_candidate_preview_allowed, calibration_event_preview_allowed

## Safety

- Read-only / preview-only
- No Hermes memory write
- No real Z9 write
- No auto calibration
- No prompt auto injection
- No real trade

## Architecture

EventStore = event ledger
Hermes Memory Kernel = memory read + candidate generation
Approval Loop = future version (decides long-term memory write)
Prompt Hot-Patching = future version (decides prompt injection)
