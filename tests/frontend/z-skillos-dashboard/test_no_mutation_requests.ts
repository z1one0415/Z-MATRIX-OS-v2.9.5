/**
 * test_no_mutation_requests.ts
 *
 * Verifies that the Z-SkillOS frontend dashboard contains NO
 * POST, PUT, PATCH, or DELETE HTTP calls anywhere in the source.
 *
 * This test reads all .ts and .tsx files under apps/z-skillos-dashboard/src/
 * and asserts that no mutation HTTP method strings appear in fetch/axios calls.
 */

import * as fs from 'fs';
import * as path from 'path';

const SRC_DIR = path.resolve(__dirname, '../../../../../apps/z-skillos-dashboard/src');

const MUTATION_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE'];

const EXCLUSIONS = [
  // Allowed: the client.ts file that checks for and blocks mutations
  'client.ts',
  // Test files themselves
  '.test.ts',
  '.spec.ts',
];

function walkDir(dir: string): string[] {
  const files: string[] = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkDir(fullPath));
    } else if (entry.isFile() && (entry.name.endsWith('.ts') || entry.name.endsWith('.tsx'))) {
      // Skip exclusions
      if (!EXCLUSIONS.some((ex) => entry.name === ex || entry.name.includes(ex))) {
        files.push(fullPath);
      }
    }
  }
  return files;
}

interface Violation {
  file: string;
  line: number;
  method: string;
  snippet: string;
}

function checkFile(filePath: string): Violation[] {
  const violations: Violation[] = [];
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Only check lines that are not comments
    const trimmed = line.trim();
    if (trimmed.startsWith('//') || trimmed.startsWith('*') || trimmed.startsWith('/**')) {
      continue;
    }

    for (const method of MUTATION_METHODS) {
      // Check for method strings in HTTP context
      // Patterns: method: 'POST', "POST", fetch(..., { method: 'POST' })
      const methodPattern = new RegExp(
        `['"\`]${method}['"\`]|method\\s*:\\s*['"\`]${method}['"\`]`,
        'i'
      );

      // Skip if line is defining a constant/var about blocking
      if (line.includes('BLOCKED') || line.includes('blocked') || line.includes('MUTATION')) {
        continue;
      }

      if (methodPattern.test(line)) {
        violations.push({
          file: path.relative(SRC_DIR, filePath),
          line: i + 1,
          method,
          snippet: trimmed.substring(0, 80),
        });
      }
    }
  }

  return violations;
}

// ─── Main ───────────────────────────────────────────────────────────────────

function main() {
  console.log('🔍 Checking for mutation HTTP methods in Z-SkillOS source...\n');

  const files = walkDir(SRC_DIR);
  console.log(`  Files to scan: ${files.length}\n`);

  const allViolations: Violation[] = [];
  for (const file of files) {
    const violations = checkFile(file);
    allViolations.push(...violations);
  }

  // Filter out false positives from client.ts (the mutation blocker itself)
  // This is already handled by EXCLUSIONS

  if (allViolations.length === 0) {
    console.log('✅ PASS: No POST/PUT/PATCH/DELETE HTTP calls found.');
    console.log('   All API calls are GET-only.');
    process.exit(0);
  } else {
    console.log(`❌ FAIL: Found ${allViolations.length} mutation HTTP method(s):\n`);
    for (const v of allViolations) {
      console.log(`  ${v.file}:${v.line} — ${v.method}`);
      console.log(`    → ${v.snippet}`);
    }
    process.exit(1);
  }
}

main();
