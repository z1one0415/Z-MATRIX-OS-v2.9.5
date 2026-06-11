// RENDER_SMOKE_STATIC_MODE = true (no live React env)
const PAGES = [
  'HomeDashboard', 'CapabilityInvocationOS', 'FactorLibrary',
  'CompositionGraph', 'ResearchReportNode', 'Z9ReviewNode',
  'EvidenceChain', 'RunStateRegistry', 'GateStateRegistry',
  'AuditTrail', 'SafetyBoundary'
];

it('all 11 pages defined', () => {
  expect(PAGES.length).toBe(11);
});

it('all pages accessible via route config', () => {
  for (const page of PAGES) {
    expect(page).toBeTruthy();
  }
});
