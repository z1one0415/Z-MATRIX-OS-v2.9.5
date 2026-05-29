# V4.0 FINAL-HARDGATES Hardening-C3 Acceptance Matrix

| Phase | Item | Status | Verify Script |
|:-----:|------|:------:|------|
| C3-0 | Scope Lock + Acceptance Matrix | NOT_STARTED | verify_v40_hardening_c3_0_scope.sh |
| C3-1 | Research Council Independent Reviewers | NOT_STARTED | verify_v40_hardening_c3_1_research_council.sh |
| C3-2 | Report Template Snapshot Rendering | NOT_STARTED | verify_v40_hardening_c3_2_reports.sh |
| C3-3 | Audit ZIP Real Export | NOT_STARTED | verify_v40_hardening_c3_3_audit_zip.sh |
| C3-4 | IRF-02/05/06/07/08 Chain Integration | NOT_STARTED | verify_v40_hardening_c3_4_irf_chains.sh |
| C3-5 | Total Verify + Truth Closeout | NOT_STARTED | verify_v40_hardening_c3_all.sh |

## Forbidden Statuses

- ❌ ACCEPTANCE_DONE
- ❌ RC1_APPROVED
- ❌ PRODUCTION_READY
- ❌ BROKER_READY
- ❌ RUNTIME_READY

## Safety Gates (all phases)

- real_trade_allowed=False
- broker_order_allowed=False
- runtime_enabled=False
- auto_buy_allowed=False
- auto_sell_allowed=False
- production_allowed=False
