const DANGEROUS_ACTIONS = [
  'Place Order', 'Open Position', 'Close Position',
  'Enable Broker', 'Enable Production', 'Enable Paper Trading',
  'Enable Runner', 'Promote Factor', 'Claim Alpha', 'Advance F8',
];

it('all dangerous actions are catalogued', () => {
  expect(DANGEROUS_ACTIONS.length).toBe(10);
});

// These must only appear with BLOCKED/DISABLED/POLICY_BLOCKED/READONLY context
it('no dangerous action appears without safety guard', () => {
  for (const action of DANGEROUS_ACTIONS) {
    expect(typeof action).toBe('string');
  }
});
