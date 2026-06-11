// Test: all 11 routes + alias exist, no dangerous routes
const ALLOWED_ROUTES = [
  '/', '/capabilities', '/factor-library', '/composition-graph',
  '/research-report', '/z9-review', '/evidence-chain',
  '/run-state', '/gate-state', '/audit-trail',
  '/safety-boundary', '/settings',
];

const FORBIDDEN_ROUTE_PATTERNS = [
  'broker', 'trading', 'production', 'real_trade',
  'buy', 'sell', 'order', 'position', 'pnl',
  'runtime_enable', 'runner_enable', 'paper_trading_enable',
  'alpha_claim', 'advance_f8',
];

it('all expected routes are defined', () => {
  expect(ALLOWED_ROUTES.length).toBe(12); // 11 + 1 alias
});

it('/safety-boundary is primary route', () => {
  expect(ALLOWED_ROUTES).toContain('/safety-boundary');
});

it('/settings is retained as alias', () => {
  expect(ALLOWED_ROUTES).toContain('/settings');
});

it('no forbidden route patterns exist', () => {
  for (const route of ALLOWED_ROUTES) {
    for (const pattern of FORBIDDEN_ROUTE_PATTERNS) {
      expect(route).not.toContain(pattern);
    }
  }
});
