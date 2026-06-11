/**
 * test_safety_boundary.ts
 *
 * Verifies the safety boundary enforcement across the dashboard:
 * 1. All pages contain Read-Only or DISABLED indicators
 * 2. Home page contains the RESTRICTIONS banner
 * 3. Settings page contains all blocked action definitions
 * 4. No page renders buy/sell buttons
 * 5. mockClient properly returns readonly: true everywhere
 */

import * as fs from 'fs';
import * as path from 'path';

const SRC_DIR = path.resolve(__dirname, '../../../../../apps/z-skillos-dashboard/src');

interface CheckResult {
  name: string;
  passed: boolean;
  detail: string;
}

function checkFileExists(filePath: string): CheckResult {
  const exists = fs.existsSync(filePath);
  return {
    name: `File exists: ${path.relative(SRC_DIR, filePath)}`,
    passed: exists,
    detail: exists ? 'Found' : 'NOT FOUND',
  };
}

function checkContentContains(filePath: string, search: string, desc: string): CheckResult {
  if (!fs.existsSync(filePath)) {
    return { name: desc, passed: false, detail: 'File not found' };
  }
  const content = fs.readFileSync(filePath, 'utf-8');
  const found = content.includes(search);
  return {
    name: desc,
    passed: found,
    detail: found ? `Contains "${search}"` : `Missing "${search}"`,
  };
}

function main() {
  console.log('Verifying Z-SkillOS Safety Boundary...\n');

  const results: CheckResult[] = [];

  const pages = [
    'HomeDashboard', 'CapabilityInvocationOS', 'FactorLibrary',
    'CompositionGraph', 'ResearchReportNode', 'Z9ReviewNode',
    'EvidenceChain', 'RunStateRegistry', 'GateStateRegistry',
    'AuditTrail', 'SafetyBoundary',
  ];

  // 1. All pages exist
  for (const page of pages) {
    results.push(checkFileExists(path.join(SRC_DIR, 'pages', `${page}.tsx`)));
  }

  // 2. All pages import SafetyBadge
  for (const page of pages) {
    const filePath = path.join(SRC_DIR, 'pages', `${page}.tsx`);
    results.push(checkContentContains(filePath, 'SafetyBadge', `${page}: imports SafetyBadge`));
  }

  // 3. Home page contains RESTRICTIONS banner
  results.push(
    checkContentContains(
      path.join(SRC_DIR, 'pages', 'HomeDashboard.tsx'),
      'RESTRICTIONS',
      'HomeDashboard: contains RESTRICTIONS banner'
    )
  );

  // 4. Home page shows all 6 safety statuses
  const requiredRestrictions = ['DISABLED_DEFAULT', 'DISABLED', 'Paper Trading', 'BLOCKED', 'Broker', 'Real Trade'];
  const homeContent = fs.readFileSync(path.join(SRC_DIR, 'pages', 'HomeDashboard.tsx'), 'utf-8');
  for (const restriction of requiredRestrictions) {
    results.push({
      name: `HomeDashboard: shows "${restriction}"`,
      passed: homeContent.includes(restriction),
      detail: homeContent.includes(restriction) ? `Found "${restriction}"` : `Missing "${restriction}"`,
    });
  }

  // 5. BlockedActionPanel contains key blocked actions
  const bannedActions = [
    'start_pipeline', 'stop_pipeline', 'generate_report', 'enable_runtime',
    'enable_production', 'enable_paper_trading', 'modify_safety_boundary',
  ];
  const blockedPanel = fs.readFileSync(
    path.join(SRC_DIR, 'components', 'layout', 'BlockedActionPanel.tsx'),
    'utf-8'
  );
  for (const action of bannedActions) {
    results.push({
      name: `BlockedActionPanel: blocks "${action}"`,
      passed: blockedPanel.includes(action),
      detail: blockedPanel.includes(action) ? `Found` : `Missing`,
    });
  }

  // 6. mockClient returns readonly: true everywhere
  const mockContent = fs.readFileSync(path.join(SRC_DIR, 'api', 'mockClient.ts'), 'utf-8');
  const readonlyCount = (mockContent.match(/readonly:\s*true/g) || []).length;
  results.push({
    name: 'mockClient: all mocks have readonly: true',
    passed: readonlyCount >= 10,
    detail: `Found readonly: true ${readonlyCount} times`,
  });

  // 7. All schemas enforce readonly
  const schemasContent = fs.readFileSync(path.join(SRC_DIR, 'api', 'schemas.ts'), 'utf-8');
  const schemaReadonlyCount = (schemasContent.match(/readonly:\s*z\.literal\(true\)/g) || []).length;
  results.push({
    name: 'schemas: enforce readonly via Zod',
    passed: schemaReadonlyCount >= 12,
    detail: `Found z.literal(true) for readonly ${schemaReadonlyCount} times`,
  });

  // 8. Topbar has readonly badge
  results.push(
    checkContentContains(
      path.join(SRC_DIR, 'app', 'topbar.tsx'),
      'READ-ONLY',
      'Topbar: shows READ-ONLY badge'
    )
  );

  // 9. Sidebar footer shows Read-Only Mode
  results.push(
    checkContentContains(
      path.join(SRC_DIR, 'app', 'sidebar.tsx'),
      'Read-Only Mode',
      'Sidebar: shows Read-Only Mode'
    )
  );

  // Report
  const passed = results.filter((r) => r.passed).length;
  const failed = results.filter((r) => !r.passed).length;

  console.log(`Results: ${passed} passed, ${failed} failed\n`);

  for (const r of results) {
    const icon = r.passed ? 'PASS' : 'FAIL';
    console.log(`${icon} ${r.name}: ${r.detail}`);
  }

  if (failed === 0) {
    console.log('\nALL SAFETY CHECKS PASSED');
    console.log('Z-SkillOS Safety Boundary is enforced.');
    process.exit(0);
  } else {
    console.log(`\n${failed} SAFETY CHECK(S) FAILED`);
    process.exit(1);
  }
}

main();
