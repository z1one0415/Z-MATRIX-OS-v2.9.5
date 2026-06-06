# Z-SkillOS Level 3 Audit Storage Bound Policy

## Status

Z_SKILLOS_LEVEL3_AUDIT_STORAGE_BOUND_POLICY_READY

## Principles

Evidence bounded. Default writes disabled. Production runtime_reports forbidden. Non-runtime audit path. Explicit max size. Lifecycle includes cleanup. No auto-expand without gate.

## Proposed Bounds

max_event_size: 4096 bytes. max_file_size: 5MB. max_retained_files: 10. max_total: 50MB. default_retention: 7 days. production: not approved.

## Required Future Tests

Rotation/blocking at bound. Cleanup scoped. Disabled writes nothing. No production/broker/real_trade.

## Final

Policy only. No implementation.
