# Impl ✓ PERMISSION_CHECK_PLAN

## Status: IMPLEMENTATION_PLANNING_PERMISSION_CHECK_PLAN_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED

## Three-Tier Permission
T0 SYSTEM: cap_os.enabled + wave0.enabled + no kill switch
T1 ADAPTER: adapter.name.enabled + registered + valid contract
T2 OPERATION: operation in allowed_ops + params valid + rate limit

## Per-Adapter Operations
**GitHub Readonly**: read_file(30rpm,repo whitelist) | list_repos(10rpm,org whitelist) | get_commits(10rpm) | get_file_tree(10rpm,max_depth≤3)
**Doc Gen**: generate_doc(20rpm,allowed_dirs+formats) | validate_template(unlimited) | render_template(30rpm)
**Report Reader**: read_report(30rpm,allowed_dirs+extensions) | parse_report(30rpm) | list_reports(10rpm) | analyze_report(10rpm)

## Forbidden Operations(永远拒绝)
write_file(Any) | delete_repo(GitHub) | create_pr(GitHub) | push_commit(GitHub) | delete_doc(DocGen) | delete_report(ReportReader) | exec_command(Any)

> Cap OS Phase 11 | Permission Check | 3-tier | Level 5 BLOCKED