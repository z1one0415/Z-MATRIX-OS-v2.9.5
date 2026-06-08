# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — HASH CHAIN PLAN

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_HASH_CHAIN_PLAN_READY

## Scope
This document defines the hash chain construction, verification, and immutability guarantees for the evidence system.

## Evidence
The hash chain provides forward-secure cryptographic linkage between all evidence events in a single invocation.

### Chain Construction Algorithm
```
function build_chain(events):
    chain = []
    prev_hash = null_anchor  // deterministic: 64 bytes of 0x00
    for event in events:
        link_input = prev_hash || event.request_hash || event.decision_hash || event.tamper_seal
        link_hash = SHA-256(link_input)
        chain.append(ChainLink(prev_hash, link_hash, event))
        prev_hash = link_hash
    chain_root = chain[0].link_hash
    chain_seal = HMAC-SHA-512(ephemeral_key, serialize_chain(chain))
    return HashChain(chain_root, chain, chain_seal)
```

### Chain Properties
1. Forward Security — Breaking link n does not compromise links 0..n-1
2. Append-Only — Once a link is added, it cannot be removed or reordered
3. Tamper-Evident — Any modification to any link invalidates chain_seal
4. Non-Repudiable — The chain root proves the exact sequence of events
5. Ephemeral Binding — Chain is bound to invocation via ephemeral_key

### Chain Verification Algorithm
```
function verify_chain(chain):
    prev_hash = null_anchor
    for link in chain.links:
        if link.prev_hash != prev_hash: return false
        expected = SHA-256(prev_hash || link.event.request_hash || link.event.decision_hash || link.event.tamper_seal)
        if link.link_hash != expected: return false
        prev_hash = link.link_hash
    expected_seal = HMAC-SHA-512(chain.ephemeral_key, serialize_chain(chain.links))
    return chain.chain_seal == expected_seal
```

## Boundary
- Hash chain is per-invocation; no cross-invocation chaining
- Chain destruction on consumer acknowledgment or TTL expiry
- Ephemeral key never leaves memory
- Maximum chain length: 256 links per invocation (safety bound)

## Forbidden
1. Cross-invocation hash chaining (privacy boundary violation)
2. Ephemeral key persistence
3. Chain truncation without seal invalidation
4. Link reordering
5. Chain serialization to disk or network
6. Unbounded chain growth (max 256 links)

## Proof
- Construction algorithm is deterministic given same inputs
- Verification catches: missing links, reordered links, modified links, forged seals
- SHA-256 collision resistance provides >128-bit security
- HMAC-SHA-512 provides >256-bit authentication security
- Max 256 links prevents memory exhaustion attacks

## Next
- Validate chain compatibility with AUDIT_SINK_PLAN query patterns
- Ensure PRIVACY_BOUNDARY_PLAN enforces no cross-chain leakage
- Proceed to AUDIT_SINK_PLAN
