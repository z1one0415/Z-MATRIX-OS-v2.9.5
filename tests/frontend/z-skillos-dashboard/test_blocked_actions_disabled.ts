/**
 * test_blocked_actions_disabled.ts
 *
 * Verifies that all UI components reference blocking/disabling language
 * and that no dangerous action buttons are rendered as enabled.
 *
 * Scans all .tsx files for forbidden action patterns.
 */

import * as fs from 'fs';
import * as path from 'path';

const SRC_DIR = path.resolve(__dirname, '../../../../../apps/z-skillos-dashboard/src');

const DANGEROUS_ACTIONS = [
  'start_pipeline', 'stop_pipeline', 'abort_pipeline',
  'enable_skill', 'disable_skill', 'invoke_skill', 'configure_skill',
  'promote_factor', 'create_factor', 'modify_factor', 'delete_factor',
  'add_node', 'remove_node', 'add_edge', 'remove_edge',
  'generate_report', 'modify_report', 'delete_report',
  'start_review', 'submit_review', 'approve_review', 'reject_review',
  'modify_evidence', 'delete_evidence',
  'start_run', 'stop_run', 'retry_run',
  'open_gate', 'close_gate', 'bypass_gate',
  'modify_audit', 'delete_audit',
  'modify_permissions', 'enable_runtime', 'enable_production',
];

const ENABLED_BUTTON_PATTERNS = [
  /onClick\s*=\s*\{[^}]*start/,
  /onClick\s*=\s*\{[^}]*enable/,
  /onClick\s*=\s*\{[^}]*invoke/,
  /onClick\s*=\s*\{[^}]*submit/,
  /onClick\s*=\s*\{[^}]*create/,
  /onClick\s*=\s*\{[^}]*delete/,
  /onClick\s*=\s*\{[^}]*modify/,
];

function walkDir(dir: string): string[] {
  const files: string[] = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkDir(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.tsx')) {
      files.push(fullPath);
    }
  }
  return files;
}

function main() {
  console.log('🔍 Checking for enabled dangerous action buttons...\n');

  const files = walkDir(SRC_DIR);
  console.log(`  Files to scan: ${files.length}\n`);

  const violations: string[] = [];

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    const relPath = path.relative(SRC_DIR, file);

    for (const pattern of ENABLED_BUTTON_PATTERNS) {
      if (pattern.test(content)) {
        // Find the matching lines
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
          const trimmed = lines[i].trim();
          if (pattern.test(trimmed) && !trimmed.includes('disabled') && !trimmed.includes('BLOCKED')) {
            violations.push(`${relPath}:${i + 1} — ${trimmed.substring(0, 100)}`);
          }
        }
      }
    }

    // Verify that at least some blocked/disabled language exists
    const hasDisabledRef = /disabled|BLOCKED|DISABLED|blocked/i.test(content);
    if (!hasDisabledRef) {
      violations.push(`${relPath} — WARNING: No disabled/blocked language found`);
    }
  }

  if (violations.length === 0) {
    console.log('✅ PASS: No enabled dangerous action buttons found.');
    console.log('   All dangerous actions are disabled or not rendered.');
    process.exit(0);
  } else {
    console.log(`❌ FAIL: Found ${violations.length} potential violations:\n`);
    for (const v of violations) {
      console.log(`  ${v}`);
    }
    process.exit(1);
  }
}

main();
