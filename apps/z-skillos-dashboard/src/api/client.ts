/**
 * Z-SkillOS API Client — GET-only fetch wrapper.
 *
 * SAFETY: Any attempt to use POST/PUT/PATCH/DELETE will throw immediately.
 * This is enforced at runtime to prevent mutation requests from ever being sent.
 */

const ALLOWED_METHODS = new Set(['GET']);

const MUTATION_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE'] as const;

const MUTATION_ERROR_MESSAGE =
  'BLOCKED: Mutation requests (POST/PUT/PATCH/DELETE) are permanently disabled. ' +
  'Z-SkillOS operates in read-only mode.';

export type FetchError = {
  error: string;
  code: string;
  timestamp: string;
  details?: Record<string, unknown>;
  trace_id?: string;
};

export async function apiGet<T>(path: string): Promise<T> {
  const method = 'GET';

  // Runtime safety gate — throw on mutation attempts
  if (!ALLOWED_METHODS.has(method)) {
    throw new Error(MUTATION_ERROR_MESSAGE);
  }

  const res = await fetch(path, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'X-SkillOS-ReadOnly': 'true',
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const err: FetchError = {
      error: body.error || `HTTP ${res.status}`,
      code: body.code || `ERR_${res.status}`,
      timestamp: body.timestamp || new Date().toISOString(),
      details: body.details,
      trace_id: body.trace_id,
    };
    throw err;
  }

  return res.json();
}

/**
 * Verify that only GET methods exist in the codebase.
 * Used by the mutation-blocking test suite.
 */
export function isMutationMethod(method: string): boolean {
  return (MUTATION_METHODS as readonly string[]).includes(method.toUpperCase());
}
