/**
 * test_no_trade_language.ts
 *
 * Verifies that no trading language (buy, sell, order, position,
 * broker_action, runtime_enable, production_enable, paper_trading_start,
 * alpha_claim) appears in the UI source code.
 *
 * Excludes: mockClient.ts (has broker descriptions for mock data),
 * test files, and docs.
 */

import * as fs from 'fs';
import * as path from 'path';

const SRC_DIR = path.resolve(__dirname, '../../../../../apps/z-skillos-dashboard/src');

const FORBIDDEN_TERMS = [
  /\bbuy\b/i,
  /\bsell\b/i,
  /\border\b(?!ed)/i, // "order" but not "ordered"
  /\bposition\b(?!s)/i, // "position" but not "positions"
  /\bbroker_action\b/i,
  /\bruntime_enable\b/i,
  /\bproduction_enable\b/i,
  /\bpaper_trading_start\b/i,
  /\balpha_claim\b/i,
  /\bexecute trade\b/i,
  /\bplace trade\b/i,
  /\btrade confirmation\b/i,
];

// Files allowed to contain "broker" in mock data descriptions
const ALLOWED_FILES = ['mockClient.ts'];

function walkDir(dir: string): string[] {
  const files: string[] = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkDir(fullPath));
    } else if (entry.isFile() && (entry.name.endsWith('.ts') || entry.name.endsWith('.tsx') || entry.name.endsWith('.css'))) {
      files.push(fullPath);
    }
  }
  return files;
}

function main() {
  console.log('🔍 Checking for trading language in Z-SkillOS source...\n');

  const files = walkDir(SRC_DIR);
  console.log(`  Files to scan: ${files.length}\n`);

  const violations: string[] = [];

  for (const file of files) {
    const fileName = path.basename(file);
    if (ALLOWED_FILES.includes(fileName)) continue;

    const content = fs.readFileSync(file, 'utf-8');
    const relPath = path.relative(SRC_DIR, file);
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();

      // Skip comments and test blocks
      if (trimmed.startsWith('//') || trimmed.startsWith('*') || trimmed.startsWith('/**')) {
        continue;
      }

      // Skip lines that are referencing the BLOCKED list itself
      if (trimmed.includes('BLOCKED') || trimmed.includes('blocked_actions') || trimmed.includes('safety_flags')) {
        continue;
      }

      for (const term of FORBIDDEN_TERMS) {
        if (term.test(trimmed)) {
          violations.push(`${relPath}:${i + 1} — "${trimmed.substring(0, 100)}"`);
          break; // one violation per line is enough
        }
      }
    }
  }

  if (violations.length === 0) {
    console.log('✅ PASS: No trading language found in source code.');
    console.log('   No buy/sell/order/position terminology in UI.');
    process.exit(0);
  } else {
    console.log(`❌ FAIL: Found ${violations.length} trading language violations:\n`);
    for (const v of violations) {
      console.log(`  ${v}`);
    }
    process.exit(1);
  }
}

main();
