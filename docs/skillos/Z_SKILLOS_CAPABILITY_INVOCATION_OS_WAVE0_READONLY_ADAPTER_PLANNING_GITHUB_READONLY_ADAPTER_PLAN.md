# Wave0 GitHub Read-Only Adapter Plan
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_GITHUB_READONLY_ADAPTER_PLAN_READY
Future read-only scope (FUTURE_PLAN_ONLY): fetch file content, fetch commit metadata, compare refs/diffs, list changed files, inspect branch HEAD, inspect commit message. Forbidden: create/update/delete files, merge branches, branch mutation, issue/PR comment mutation (requires future separate write gate), secret/token exposure. Permission: READ_ONLY only. Evidence: source_ref+hash, request_hash, output_hash. No adapter code in this phase. No execution. Level 5 BLOCKED.
