/**
 * Mock Client — Reads fixtures from skillos/frontend_handoff/fixtures/
 *
 * Used when the backend is unavailable (dev/offline mode).
 * Detected automatically by the query hooks; falls back to mock data when API fails.
 */

import type {
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
  HealthResponse,
  VersionResponse,
} from './schemas';

// ─── Mock Health ────────────────────────────────────────────────────────────

export const MOCK_HEALTH: HealthResponse = {
  status: 'ok',
  version: 'v0.1.0-rc',
  uptime_seconds: 12345,
  components: {
    factor_library: 'ok',
    composition_graph: 'ok',
    research_report: 'ok',
    z9_review: 'ok',
    evidence_chain: 'ok',
    run_state: 'ok',
    gate_state: 'ok',
    audit_trail: 'ok',
  },
};

// ─── Mock Version ───────────────────────────────────────────────────────────

export const MOCK_VERSION: VersionResponse = {
  version: 'v0.1.0-rc',
  contract_version: 'v1',
  seal: 'A1_CONTRACT_FREEZE',
  build_timestamp: '2026-06-12T00:00:00Z',
  readonly: true,
};

// ─── Mock Dashboard ─────────────────────────────────────────────────────────

export const MOCK_DASHBOARD: DashboardSummary = {
  system_health: {
    status: 'ok',
    uptime_seconds: 12345,
    version: 'v2.9.6-draft',
    seal: 'A1_CONTRACT_FREEZE',
  },
  gate_summary: {
    passed: 8,
    failed: 0,
    pending: 3,
    blocked: 0,
  },
  component_status: {
    factor_library: 'ok',
    composition_graph: 'ok',
    research_report: 'disabled_default',
    z9_review: 'disabled_default',
    evidence_chain: 'ok',
    run_state: 'ok',
    gate_state: 'ok',
    audit_trail: 'ok',
  },
  recent_activity: [],
  readonly: true,
};

// ─── Mock Capabilities ──────────────────────────────────────────────────────

export const MOCK_CAPABILITIES: CapabilitiesResponse = {
  capabilities: [
    { id: 'CAP-001', name: 'F7 Gate Chain', status: 'disabled_default', description: 'Seven-gate pipeline from sensor to decision envelope' },
    { id: 'CAP-002', name: 'B-Matrix Classifier', status: 'disabled_default', description: 'Five-category bottom-qualification scoring gate' },
    { id: 'CAP-003', name: 'D-Matrix Radar', status: 'disabled_default', description: 'Dark-horse origin signal detection with 7-factor scoring' },
    { id: 'CAP-004', name: 'R-Matrix Oscillation', status: 'disabled_default', description: 'Type-A horizontal / Type-B ascending channel oscillator ranker' },
    { id: 'CAP-005', name: 'Z2 Research Kernel', status: 'disabled_default', description: 'Industrial chain evidence layering and financial gate analysis' },
    { id: 'CAP-006', name: 'Z8 Position Control', status: 'disabled_default', description: 'Pre-trade checklist and allocation sizing validator' },
    { id: 'CAP-007', name: 'Z9 Calibration Engine', status: 'disabled_default', description: 'Prediction accuracy tracking and regime-aware calibration' },
    { id: 'CAP-008', name: 'Z9 Review Node', status: 'disabled_default', description: 'Disabled-default review module per P0 merge policy' },
    { id: 'CAP-009', name: 'Macro Veto L2.5', status: 'blocked', description: 'Eight-domain directional shock assessment gate' },
    { id: 'CAP-010', name: 'Narrative Radar L1.6', status: 'disabled_default', description: 'Slogan/exhaustion/diversity signal extraction from newsflow' },
    { id: 'CAP-011', name: 'Composition Graph', status: 'degraded', description: 'Factor-to-skill dependency graph across Z-MATRIX-OS' },
    { id: 'CAP-012', name: 'Event Store', status: 'disabled_default', description: 'Immutable event log with lineage tracking' },
    { id: 'CAP-013', name: 'Audit Trail', status: 'disabled_default', description: 'Full decision-audit chain with timestamped actions' },
    { id: 'CAP-014', name: 'Evidence Chain', status: 'disabled_default', description: 'Hash-chained evidence traversal from FactorLib to Z9' },
    { id: 'CAP-015', name: 'Portfolio Exposure', status: 'disabled_default', description: 'Beta/correlation exposure reporting (offline maintenance)' },
    { id: 'CAP-016', name: 'Tail Risk Controller', status: 'disabled_default', description: 'Limit-down blackhole detection (suspended per v3.6)' },
    { id: 'CAP-017', name: 'Research Asset Index', status: 'disabled_default', description: 'Cross-pipeline asset discovery and catalog' },
    { id: 'CAP-018', name: 'Hermes Memory Kernel', status: 'blocked', description: 'Knowledge graph persistence layer (blocked by schema migration)' },
  ],
  total_count: 18,
  enabled_count: 0,
  readonly: true,
};

// ─── Mock Factor Library ────────────────────────────────────────────────────

export const MOCK_FACTORS: FactorLibraryResponse = {
  seal_status: 'SEALED',
  factor_count: 23,
  readonly: true,
  factors: [
    { id: 'F001', name: 'Dividend Yield 3Y', seal_status: 'SEALED', category: 'B-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F002', name: 'FCF Reinvestment Rate', seal_status: 'SEALED', category: 'B-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F003', name: 'Resource ROE 5Y', seal_status: 'SEALED', category: 'B-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F004', name: 'Infrastructure Moat Width', seal_status: 'SEALED', category: 'B-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F005', name: 'Brand Scarcity Index', seal_status: 'DEGRADED', category: 'B-Matrix', evaluation_count: 2200, last_evaluated: '2026-06-10T09:30:00Z' },
    { id: 'F008', name: 'Gene Expression Score', seal_status: 'SEALED', category: 'D-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F009', name: 'Sector Tailwind Index', seal_status: 'SEALED', category: 'D-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F010', name: 'Theme Alignment', seal_status: 'SEALED', category: 'D-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F011', name: 'Silent Accumulation', seal_status: 'SEALED', category: 'D-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F012', name: 'Smart Money Footprint', seal_status: 'DEGRADED', category: 'D-Matrix', evaluation_count: 1800, last_evaluated: '2026-06-09T15:00:00Z' },
    { id: 'F015', name: 'Horizontal Oscillation Score', seal_status: 'SEALED', category: 'R-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F016', name: 'Channel Slope Integrity', seal_status: 'SEALED', category: 'R-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F017', name: 'Bounce Frequency Ratio', seal_status: 'SEALED', category: 'R-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F018', name: 'False Breakout Penalty', seal_status: 'SEALED', category: 'R-Matrix', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F019', name: 'Volume Confirmation Ratio', seal_status: 'DEGRADED', category: 'R-Matrix', evaluation_count: 2400, last_evaluated: '2026-06-08T15:00:00Z' },
    { id: 'F020', name: 'Coverage Discount', seal_status: 'SEALED', category: 'Shared', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F021', name: 'M1 240bar Standard Axis', seal_status: 'SEALED', category: 'Shared', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F022', name: 'False Preheat Penalty', seal_status: 'SEALED', category: 'Shared', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
    { id: 'F023', name: 'Rating Cap Enforcer', seal_status: 'SEALED', category: 'Shared', evaluation_count: 3676, last_evaluated: '2026-06-11T15:00:00Z' },
  ],
};

// ─── Mock Composition Graph ─────────────────────────────────────────────────

export const MOCK_COMPOSITION_GRAPH: CompositionGraphResponse = {
  nodes: [
    { id: 'N01', type: 'skill', label: 'F7.0 TruthGate', status: 'enabled' },
    { id: 'N02', type: 'skill', label: 'Sensor Array', status: 'enabled' },
    { id: 'N03', type: 'skill', label: 'L2.5 MacroVeto', status: 'enabled' },
    { id: 'N04', type: 'skill', label: 'L1.6 NarrativeRadar', status: 'enabled' },
    { id: 'N05', type: 'skill', label: 'B-Matrix v2.1.1', status: 'enabled' },
    { id: 'N06', type: 'skill', label: 'D-Matrix v2.2', status: 'enabled' },
    { id: 'N07', type: 'skill', label: 'R-Matrix v1.1', status: 'enabled' },
    { id: 'N08', type: 'report', label: 'Z2 Research Kernel', status: 'enabled' },
    { id: 'N09', type: 'skill', label: 'Z8 Allocation Control', status: 'enabled' },
    { id: 'N10', type: 'review', label: 'Z9 Calibration', status: 'degraded' },
    { id: 'N11', type: 'review', label: 'Z9 Review Node', status: 'disabled_default' },
    { id: 'N12', type: 'skill', label: 'F7.2 Decision Gate', status: 'enabled' },
    { id: 'N13', type: 'evidence', label: 'Hermes Memory Kernel', status: 'blocked' },
    { id: 'N14', type: 'evidence', label: 'Event Store', status: 'enabled' },
  ],
  edges: [
    { from: 'N01', to: 'N02', type: 'depends_on' },
    { from: 'N02', to: 'N03', type: 'feeds_into' },
    { from: 'N02', to: 'N04', type: 'feeds_into' },
    { from: 'N03', to: 'N05', type: 'depends_on' },
    { from: 'N04', to: 'N06', type: 'feeds_into' },
    { from: 'N05', to: 'N08', type: 'feeds_into' },
    { from: 'N06', to: 'N08', type: 'feeds_into' },
    { from: 'N07', to: 'N08', type: 'feeds_into' },
    { from: 'N08', to: 'N09', type: 'produces' },
    { from: 'N09', to: 'N10', type: 'feeds_into' },
    { from: 'N10', to: 'N11', type: 'feeds_into' },
    { from: 'N10', to: 'N12', type: 'feeds_into' },
    { from: 'N12', to: 'N14', type: 'produces' },
    { from: 'N14', to: 'N13', type: 'depends_on' },
  ],
  node_count: 14,
  edge_count: 14,
  readonly: true,
  disabled_default: true,
};

// ─── Mock Research Report ───────────────────────────────────────────────────

export const MOCK_RESEARCH_REPORT: ResearchReportResponse = {
  report_status: 'disabled_default',
  recent_reports: [],
  generation_enabled: false,
  readonly: true,
};

// ─── Mock Z9 Review ─────────────────────────────────────────────────────────

export const MOCK_Z9_REVIEW: Z9ReviewResponse = {
  review_status: 'disabled_default',
  queue_size: 0,
  reviews: [],
  review_enabled: false,
  readonly: true,
};

// ─── Mock Evidence Chain ────────────────────────────────────────────────────

export const MOCK_EVIDENCE_CHAIN: EvidenceChainResponse = {
  chain_id: 'EC-2026-06-12-001',
  nodes: [
    { id: 'E1', type: 'input', content: 'FactorLib: v2.9.6-draft sealed and exported', timestamp: '2026-06-12T03:50:00Z', hash: 'sha256:9a7f3b...', source: 'FactorLib' },
    { id: 'E2', type: 'intermediate', content: 'A1 Ingestion: 3676 stocks, 882240 OHLCV bars loaded', timestamp: '2026-06-12T03:52:00Z', hash: 'sha256:a1b2c3...', source: 'A1' },
    { id: 'E3', type: 'intermediate', content: 'B1 Classifier: 42 candidates from 3676 stocks', timestamp: '2026-06-12T03:55:00Z', hash: 'sha256:b1c2d3...', source: 'B-Matrix' },
    { id: 'E4', type: 'decision', content: 'Z2 Research: 10 chains, 38 financial gates passed', timestamp: '2026-06-12T03:58:00Z', hash: 'sha256:z2c3d4...', source: 'Z2' },
    { id: 'E5', type: 'output', content: 'Z9 Calibration: 1547 samples, regime NORMAL_RISK_ON', timestamp: '2026-06-12T04:00:00Z', hash: 'sha256:z9d4e5...', source: 'Z9' },
  ],
  links: [
    { from: 'E1', to: 'E2', type: 'derives_from' },
    { from: 'E2', to: 'E3', type: 'derives_from' },
    { from: 'E3', to: 'E4', type: 'derives_from' },
    { from: 'E4', to: 'E5', type: 'derives_from' },
  ],
  readonly: true,
};

// ─── Mock Run State ─────────────────────────────────────────────────────────

export const MOCK_RUN_STATE: RunStateResponse = {
  current_state: 'idle',
  pipeline_runs: [
    {
      run_id: 'RUN-2026-06-12-0403',
      pipeline: 'Z-G14 Monthly BRD Rescan',
      status: 'completed',
      started_at: '2026-06-12T03:50:00Z',
      completed_at: '2026-06-12T04:00:30Z',
      readonly: true,
    },
    {
      run_id: 'RUN-2026-06-11-1500',
      pipeline: 'Z-G06 Daily Review',
      status: 'completed',
      started_at: '2026-06-11T15:00:00Z',
      completed_at: '2026-06-11T15:05:20Z',
      readonly: true,
    },
    {
      run_id: 'RUN-2026-06-11-0930',
      pipeline: 'Z-G03 Intraday Confirm',
      status: 'completed',
      started_at: '2026-06-11T09:30:00Z',
      completed_at: '2026-06-11T10:15:00Z',
      readonly: true,
    },
    {
      run_id: 'RUN-2026-06-11-0900',
      pipeline: 'Z-G02 Sensor Array',
      status: 'completed',
      started_at: '2026-06-11T09:00:00Z',
      completed_at: '2026-06-11T09:28:00Z',
      readonly: true,
    },
  ],
  readonly: true,
};

// ─── Mock Gate State ────────────────────────────────────────────────────────

export const MOCK_GATE_STATE: GateStateResponse = {
  gates: [
    { gate_id: 'F7.0', name: 'TruthGate', status: 'passed', last_checked: '2026-06-12T03:50:02Z', details: '7/7 preconditions met' },
    { gate_id: 'F7.1a', name: 'Macro Gate', status: 'passed', last_checked: '2026-06-12T03:52:45Z', details: 'L2.5 MacroVeto: no directional shocks' },
    { gate_id: 'F7.1b', name: 'Data Quality Gate', status: 'passed', last_checked: '2026-06-12T03:52:50Z', details: 'OHLCV completeness: 99.97%' },
    { gate_id: 'F7.1c', name: 'Matrix Reliability Gate', status: 'passed', last_checked: '2026-06-12T03:55:10Z', details: 'B:0.94 D:0.89 R:0.91' },
    { gate_id: 'F7.1d', name: 'Evidence Chain Gate', status: 'passed', last_checked: '2026-06-12T03:58:15Z', details: 'Hash continuity verified across 5 nodes' },
    { gate_id: 'F7.1e', name: 'Conflict Resolution Gate', status: 'passed', last_checked: '2026-06-12T03:59:30Z', details: '0 conflicts detected' },
    { gate_id: 'F7.2', name: 'Decision Gate', status: 'passed', last_checked: '2026-06-12T04:00:27Z', details: '28 stock final selection' },
  ],
  summary: { passed: 7, failed: 0, pending: 0, blocked: 0 },
  readonly: true,
};

// ─── Mock Audit Trail ───────────────────────────────────────────────────────

export const MOCK_AUDIT_TRAIL: AuditTrailResponse = {
  entries: [
    { id: 'A01', action: 'PIPELINE_TRIGGER', timestamp: '2026-06-12T03:50:00Z', actor: 'SCHEDULER', result: 'success', details: { detail: 'Z-G14 monthly run triggered' } },
    { id: 'A02', action: 'GATE_CHECK_START', timestamp: '2026-06-12T03:50:00Z', actor: 'TRUTH_GATE', result: 'success', details: { detail: 'F7.0 preconditions evaluation' } },
    { id: 'A03', action: 'GATE_CHECK_PASS', timestamp: '2026-06-12T03:50:02Z', actor: 'TRUTH_GATE', result: 'success', details: { detail: '7/7 preconditions met' } },
    { id: 'A04', action: 'INGESTION_START', timestamp: '2026-06-12T03:50:02Z', actor: 'DATA_PIPELINE', result: 'success', details: { detail: 'A1 OHLCV + financial data loading' } },
    { id: 'A05', action: 'INGESTION_COMPLETE', timestamp: '2026-06-12T03:52:47Z', actor: 'DATA_PIPELINE', result: 'success', details: { detail: '3676 stocks, 882240 bars loaded' } },
    { id: 'A06', action: 'SCAN_START', timestamp: '2026-06-12T03:52:50Z', actor: 'B_MATRIX', result: 'success', details: { detail: 'B-Matrix v2.1.1 full scan' } },
    { id: 'A07', action: 'SCAN_COMPLETE', timestamp: '2026-06-12T03:55:57Z', actor: 'B_MATRIX', result: 'success', details: { detail: '42 candidates' } },
    { id: 'A08', action: 'SCAN_START', timestamp: '2026-06-12T03:55:57Z', actor: 'D_MATRIX', result: 'success', details: { detail: 'D-Matrix v2.2 full scan' } },
    { id: 'A09', action: 'SCAN_COMPLETE', timestamp: '2026-06-12T03:58:43Z', actor: 'D_MATRIX', result: 'success', details: { detail: '87 candidates' } },
    { id: 'A10', action: 'SCAN_START', timestamp: '2026-06-12T03:58:43Z', actor: 'R_MATRIX', result: 'success', details: { detail: 'R-Matrix v1.1 full scan' } },
    { id: 'A11', action: 'GATE_CHECK_PASS', timestamp: '2026-06-12T04:01:58Z', actor: 'DECISION_GATE', result: 'success', details: { detail: 'F7.2: 28 stocks final' } },
    { id: 'A12', action: 'ARCHIVE_COMPLETE', timestamp: '2026-06-12T04:02:33Z', actor: 'ARCHIVE_ENGINE', result: 'success', details: { detail: '47 EventStore entries, 112 graph nodes' } },
  ],
  total_count: 12,
  readonly: true,
};
