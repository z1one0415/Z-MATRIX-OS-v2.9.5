# V3.5.20 BASELINE IMPORT MANIFEST
imports:
  - source: v3.5.20 Research OS RC
    commit: dc4b980
    status: FROZEN
  - source: v3.5.20-PATCH-A→H
    commit: dc4b980
    patches: [A,B,C,D,E,F,G,H]
    status: COMPLETE
  - source: R-Matrix historical replay
    status: RESEARCH_READY
  - source: B-Matrix current snapshot
    status: RESEARCH_READY (81 candidates)
  - source: B-Matrix historical PIT
    status: BLOCKED_DATA_INSUFFICIENT
  - source: D-Matrix
    status: BLOCKED
  - source: production/real_trade
    status: BLOCKED
