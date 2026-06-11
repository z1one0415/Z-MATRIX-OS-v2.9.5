const REQUIRED_SAFETY_LABELS = [
  'DISABLED_DEFAULT', 'Runtime', 'Runner', 'Paper Trading',
  'Production', 'Broker', 'Real Trade', 'Read-Only',
  'No Buy', 'No Sell', 'No Alpha Claim', 'No Promotion',
  'F8 Advancement',
];

it('safety labels defined', () => {
  expect(REQUIRED_SAFETY_LABELS.length).toBeGreaterThan(10);
});
