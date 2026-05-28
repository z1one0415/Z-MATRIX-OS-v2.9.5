# DATA PIT POLICY
pit_rules:
  financial: announce_date <= trade_date REQUIRED
  daily_price: trade_date close for next-day decision
  event: publish_time <= decision_cutoff REQUIRED
  lhb: 披露时间之后才可用
  fund_flow: 按可获得时间切分
pit_violation: BLOCKED from any decision
proxy_policy: ALLOWED_FOR_RESEARCH_ONLY
proxy_production: BLOCKED
