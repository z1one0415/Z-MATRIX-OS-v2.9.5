/**
 * Z-SkillOS API Endpoints — All GET-only, fully typed.
 *
 * 15 endpoints total. Every function returns a Promise<T> with Zod-validated types.
 */
import { apiGet } from './client';
import type {
  HealthResponse,
  VersionResponse,
  DashboardSummary,
  CapabilitiesResponse,
  FactorLibraryResponse,
  CompositionGraphResponse,
  ResearchReportResponse,
  Z9ReviewResponse,
  EvidenceChainResponse,
  RunStateResponse,
  GateStateResponse,
  AuditTrailResponse,
} from './schemas';

// ─── System ─────────────────────────────────────────────────────────────────

/** GET /api/health — System health check */
export function fetchHealth(): Promise<HealthResponse> {
  return apiGet<HealthResponse>('/api/health');
}

/** GET /api/version — Version and contract info */
export function fetchVersion(): Promise<VersionResponse> {
  return apiGet<VersionResponse>('/api/version');
}

// ─── Dashboard ──────────────────────────────────────────────────────────────

/** GET /api/dashboard/summary — Dashboard overview, gates, activity */
export function fetchDashboardSummary(): Promise<DashboardSummary> {
  return apiGet<DashboardSummary>('/api/dashboard/summary');
}

// ─── Capabilities ───────────────────────────────────────────────────────────

/** GET /api/capabilities — Capability Invocation OS skill catalog */
export function fetchCapabilities(): Promise<CapabilitiesResponse> {
  return apiGet<CapabilitiesResponse>('/api/capabilities');
}

// ─── Factor Library ─────────────────────────────────────────────────────────

/** GET /api/factor-library/summary — Factor seal status and evaluation matrix */
export function fetchFactorLibrary(): Promise<FactorLibraryResponse> {
  return apiGet<FactorLibraryResponse>('/api/factor-library/summary');
}

// ─── Composition Graph ──────────────────────────────────────────────────────

/** GET /api/composition-graph/summary — Node/edge status */
export function fetchCompositionGraph(): Promise<CompositionGraphResponse> {
  return apiGet<CompositionGraphResponse>('/api/composition-graph/summary');
}

// ─── Research Report ────────────────────────────────────────────────────────

/** GET /api/research-report/summary — Report previews */
export function fetchResearchReport(): Promise<ResearchReportResponse> {
  return apiGet<ResearchReportResponse>('/api/research-report/summary');
}

// ─── Z9 Review ──────────────────────────────────────────────────────────────

/** GET /api/z9-review/summary — Review queue status */
export function fetchZ9Review(): Promise<Z9ReviewResponse> {
  return apiGet<Z9ReviewResponse>('/api/z9-review/summary');
}

// ─── Evidence & State ───────────────────────────────────────────────────────

/** GET /api/evidence-chain — Evidence chain traversal */
export function fetchEvidenceChain(): Promise<EvidenceChainResponse> {
  return apiGet<EvidenceChainResponse>('/api/evidence-chain');
}

/** GET /api/run-state — Pipeline run status */
export function fetchRunState(): Promise<RunStateResponse> {
  return apiGet<RunStateResponse>('/api/run-state');
}

/** GET /api/gate-state — Gate pass/fail matrix */
export function fetchGateState(): Promise<GateStateResponse> {
  return apiGet<GateStateResponse>('/api/gate-state');
}

/** GET /api/audit-trail — Audit log viewer */
export function fetchAuditTrail(): Promise<AuditTrailResponse> {
  return apiGet<AuditTrailResponse>('/api/audit-trail');
}

// ─── Frontend Meta ──────────────────────────────────────────────────────────

/** GET /api/frontend/routes — Frontend route index */
export function fetchFrontendRoutes(): Promise<{ routes: Array<{ route: string; page_id: string; title: string }> }> {
  return apiGet('/api/frontend/routes');
}

/** GET /api/frontend/contracts — Frontend contract index */
export function fetchFrontendContracts(): Promise<{ contracts: Array<{ contract_id: string; name: string; version: string }> }> {
  return apiGet('/api/frontend/contracts');
}
