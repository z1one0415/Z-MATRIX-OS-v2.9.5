# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — PRIVACY BOUNDARY PLAN

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_PRIVACY_BOUNDARY_PLAN_READY

## Scope
This document defines the privacy boundary — complete isolation between invocations, preventing any invocation from observing or influencing another.

## Evidence
Privacy boundary evidence is structural, not operational. The boundary is enforced by design, not by audit.

### Privacy Boundary Dimensions
| Dimension | Boundary Rule | Enforcement Mechanism |
|-----------|---------------|----------------------|
| Memory Isolation | No shared heap between invocations | Per-invocation memory arena |
| Hash Chain Isolation | No cross-invocation chain linking | Per-invocation chain root |
| Audit Sink Isolation | Sink indexes are invocation-scoped | Per-invocation audit sink instance |
| Ephemeral Key Isolation | Unique key per invocation | CSPRNG, no key reuse |
| Evidence Bundle Isolation | No bundle contains another invocation's data | Schema enforces single-invocation scope |
| Error Isolation | Errors in one invocation do not affect others | Try-catch per invocation boundary |
| Timing Isolation | No timing side-channel between invocations | Fixed-time operations where sensitive |
| Resource Isolation | No resource exhaustion cross-invocation | Per-invocation resource quotas |

### Memory Lifecycle
```
Invocation Start
  -> Allocate per-invocation memory arena
  -> Generate ephemeral key (CSPRNG)
  -> Initialize audit sink instance
  -> Initialize hash chain with null_anchor
Invocation Execution
  -> All operations within arena boundary
  -> All evidence within hash chain
  -> No cross-arena pointer access
Invocation End
  -> Deliver evidence bundle to consumer
  -> Await consumer acknowledgment or TTL expiry
  -> Zero-fill memory arena
  -> Deallocate arena
  -> Destroy ephemeral key
  -> Destroy audit sink
```

### No Hidden Persistence Guarantees
1. No environment variable side-effects
2. No temporary file creation
3. No syscall-based state leakage (flock, mmap with MAP_SHARED, shm_open)
4. No process-level state mutation (umask, signal handlers, atexit)
5. No IPC mechanism usage (pipes, sockets, shared memory segments)
6. No filesystem metadata modification (atime, ctime updates on reads)

## Boundary
- Privacy boundary is absolute: zero information flow between invocations
- Boundary is enforced at the memory allocator level, not application level
- Invocation arguments are not visible to other invocations
- Invocation results are not cached or shared
- Consumer callback is the only exit point for evidence

## Forbidden
1. Shared mutable state between invocations
2. Cross-invocation hash chain linking
3. Key reuse across invocations
4. Evidence bundle containing cross-invocation data
5. Environment variable leakage between invocations
6. Filesystem metadata side-effects from readonly operations
7. Timing side-channels observable between invocations
8. Process-level state mutations during invocation

## Proof
- Memory arena isolation prevents pointer-based data leakage
- Zero-fill on deallocation prevents data remnant attacks
- No hidden persistence vector is left unaddressed (6 categories enumerated)
- Ephemeral key destruction prevents post-hoc chain forgery
- Per-invocation audit sink prevents cross-invocation query leakage

## Next
- Validate privacy boundary against ROLLBACK_PLAN (rollback must not break isolation)
- Ensure FORBIDDEN_ACTIONS_MATRIX captures all boundary violations
- Proceed to ROLLBACK_PLAN
