# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — SCHEMA_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Schema Philosophy

Every Z-MATRIX Module Adapter defines explicit JSON Schema for its inputs
and outputs. Schema validation is mandatory before and after execution.
Schema violations are caught at the contract layer before any business
logic executes, providing a type-safe invocation boundary.

---

## §2 — Standard Input Envelope

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["invocation_id", "adapter_id", "timestamp", "parameters"],
  "properties": {
    "invocation_id": {"type": "string", "format": "uuid"},
    "adapter_id": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"},
    "caller_id": {"type": "string"},
    "parameters": {"type": "object"},
    "trace_context": {"type": "object"},
    "evidence_mode": {"type": "string", "enum": ["full", "summary", "none"]}
  }
}
```

---

## §3 — Standard Output Envelope

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["invocation_id", "status", "evidence_hash", "result"],
  "properties": {
    "invocation_id": {"type": "string", "format": "uuid"},
    "adapter_id": {"type": "string"},
    "status": {"type": "string", "enum": ["SUCCESS", "REJECTED", "TIMEOUT", "ERROR", "KILLED"]},
    "evidence_hash": {"type": "string"},
    "result": {"type": "object"},
    "errors": {"type": "array", "items": {"type": "object"}},
    "warnings": {"type": "array", "items": {"type": "object"}},
    "duration_ms": {"type": "integer"},
    "output_size_bytes": {"type": "integer"}
  }
}
```

---

## §4 — Per-Adapter Parameter Schemas

### A1: capability_registry_readonly
```json
{
  "parameters": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "adapter_filter": {"type": "array", "items": {"type": "string"}},
      "status_filter": {"type": "array", "items": {"type": "string"}},
      "limit": {"type": "integer", "minimum": 1, "maximum": 100}
    }
  }
}
```

### A2: z9_memory_review_readonly
```json
{
  "parameters": {
    "type": "object",
    "required": ["query"],
    "properties": {
      "query": {"type": "string", "minLength": 1},
      "max_results": {"type": "integer", "minimum": 1, "maximum": 50},
      "min_score": {"type": "number", "minimum": 0, "maximum": 1},
      "corpus": {"type": "string", "enum": ["memory", "wiki", "all", "sessions"]}
    }
  }
}
```

### A3: z2_research_output_readonly
```json
{
  "parameters": {
    "type": "object",
    "required": ["report_path"],
    "properties": {
      "report_path": {"type": "string", "pattern": "^记忆宫殿/"},
      "sections": {"type": "array", "items": {"type": "string"}},
      "format": {"type": "string", "enum": ["markdown", "json", "summary"]}
    }
  }
}
```

### A4: local_report_reading
```json
{
  "parameters": {
    "type": "object",
    "required": ["file_path"],
    "properties": {
      "file_path": {"type": "string"},
      "offset": {"type": "integer", "minimum": 0},
      "limit": {"type": "integer", "minimum": 1, "maximum": 5000},
      "encoding": {"type": "string", "default": "utf-8"}
    }
  }
}
```

### A5: document_generation_in_memory
```json
{
  "parameters": {
    "type": "object",
    "required": ["content", "template"],
    "properties": {
      "content": {"type": "object"},
      "template": {"type": "string"},
      "format": {"type": "string", "enum": ["markdown", "html", "json"]},
      "metadata": {"type": "object"}
    }
  }
}
```

---

## §5 — Schema Validation Rules

1. Input validation runs BEFORE execution. Invalid input = REJECT.
2. Output validation runs AFTER execution. Invalid output = REJECT + evidence.
3. Schema is versioned with the adapter contract.
4. Schema evolution requires contract version bump.
5. Backward-incompatible schema changes require new adapter registration.
6. All schema validations are logged to the evidence chain.

---

## §6 — Schema Registry

A central schema registry stores all current and historical schemas:
- Current schemas: indexed by `adapter_id + version`
- Historical schemas: retained for evidence replay
- Schema hash: SHA-256 of canonical JSON Schema
- Schema diff: stored on version change for audit

---

## §7 — Governance

All schemas are FUTURE_PLAN_ONLY. The schema registry, validation engine,
and per-adapter schemas are defined but not implemented. Schema enforcement
is gated behind the full planning-review-merge pipeline.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Schema Plan
