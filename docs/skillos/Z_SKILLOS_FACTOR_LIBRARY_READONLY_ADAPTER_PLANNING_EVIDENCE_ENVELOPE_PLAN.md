# Factor Library Read-Only Adapter Planning — Evidence Envelope Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_EVIDENCE_ENVELOPE_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan the FactorEvidenceEnvelope read-only adapter component. Evidence packaging for factor library data. Integrates with C1 sandbox evidence schema via source_commit field.

### Evidence Envelope Fields (future read-only)
- source_commit (SHA256: commit of factor library state at evidence time — anchors to C1 evidence chain)
- artifact_refs (list: references to factor library artifacts — manifest, formula, validation, guardrail, contract)
- evidence_hashes (dict: SHA256 hashes for each artifact type)
  - manifest_hash (SHA256 of FactorManifest)
  - formula_hash (SHA256 of factor formula)
  - validation_hash (SHA256 of FactorValidationSnapshot)
  - guardrail_hash (SHA256 of FactorGuardrailProfile)
  - contract_hash (SHA256 of FactorApplicationContract)
- envelope_metadata (dict: adapter_id, source_class="factor_library", permission_tier, gate_state)

### C1 Sandbox Evidence Dependency
C1 (Read-Only Invocation Sandbox Evidence) is already merged and sealed at 22252711. Its generic evidence schema (request_hash, response_hash_placeholder, decision_hash, source_class) is compatible. The FactorEvidenceEnvelope.source_commit field plugs into C1's hash chain as the request_hash source. No C1 rework required.

### Evidence Rules
- Hash-only: no raw content in evidence
- In-memory only: no file writes
- No hidden persistence: evidence lives only in the evidence sink
- No runtime_audit / runtime_reports / data writes
- source_commit must be set before any factor evidence is stored

## Boundary: No implementation. No code. Level 5 BLOCKED.

## Next: Canonical Intent Plan.

> Factor Library | Planning | Evidence Envelope | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Factor Library | Hardening v2 | Level 5 BLOCKED
