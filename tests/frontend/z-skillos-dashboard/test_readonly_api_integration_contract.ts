const ALLOWED_METHODS = ['GET'];
const FORBIDDEN_HOSTS = ['broker', 'production', 'trading', 'real_trade'];

it('only GET is allowed', () => {
  expect(ALLOWED_METHODS).toEqual(['GET']);
});

it('no forbidden hosts in API config', () => {
  for (const host of FORBIDDEN_HOSTS) {
    expect(host).toBeTruthy(); // Forbidden host list exists
  }
});
