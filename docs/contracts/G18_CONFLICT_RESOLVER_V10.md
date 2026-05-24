# G18 Conflict Resolver v1.0

## Input
- upstream_evidence (dict with g09/g08/g11/g14/z16/g17)
- prediction (with action_proposal)

## Output Schema
- conflict_version: "v1.0"
- has_conflict: bool
- conflict_level: NONE|LOW|MEDIUM|HIGH
- suggested_action_cap: AVOID|BLOCKED|WAIT|WATCH|PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17|PAPER_TRACK|PAPER_PROBE_ELIGIBLE
- conflicts: list of {code, level, description, suggested_action_cap, source_pair}
- warnings: list[str]

## Rules
1. G09 sell vs G18 paper entry → HIGH/WAIT
2. G09 hard_blocks → HIGH/WAIT
3. G08 narrative decay>=0.7 or bubble>=0.8 → MEDIUM/WATCH
4. G11 warning only → LOW/MEDIUM, never WAIT
5. Z16/G17 unconfirmed for paper → MEDIUM/pending

## Principle
Conflict resolver can only DOWNGRADE actions, never upgrade.
CAP_ORDER: AVOID < BLOCKED < WAIT < WATCH < PAPER_PROBE_ELIGIBLE_PENDING < PAPER_TRACK < PAPER_PROBE_ELIGIBLE

## Not real trade
- No BUY/SELL/AUTO_TRADE/MARKET_ORDER ever
