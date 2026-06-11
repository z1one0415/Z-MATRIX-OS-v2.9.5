import { z } from 'zod';

// ─── Shared enums & helpers ─────────────────────────────────────────────────

const statusSchema = z.enum(['ok', 'degraded', 'error']);
const componentStatusSchema = z.enum([
  'ok',
  'degraded',
  'error',
  'disabled_default',
  'blocked',
]);

// ─── Health ─────────────────────────────────────────────────────────────────

export const healthSchema = z.object({
  status: z.enum(['ok']),
  version: z.string(),
  uptime_seconds: z.number(),
  components: z.object({
    factor_library: statusSchema,
    composition_graph: statusSchema,
    research_report: statusSchema,
    z9_review: statusSchema,
    evidence_chain: statusSchema,
    run_state: statusSchema,
    gate_state: statusSchema,
    audit_trail: statusSchema,
  }),
});

export type HealthResponse = z.infer<typeof healthSchema>;

// ─── Version ────────────────────────────────────────────────────────────────

export const versionSchema = z.object({
  version: z.string(),
  contract_version: z.string(),
  seal: z.string(),
  build_timestamp: z.string().optional(),
  readonly: z.literal(true),
});

export type VersionResponse = z.infer<typeof versionSchema>;

// ─── Dashboard Summary ──────────────────────────────────────────────────────

export const dashboardSummarySchema = z.object({
  system_health: z.object({
    status: z.enum(['ok', 'degraded', 'error']),
    uptime_seconds: z.number(),
    version: z.string().optional(),
    seal: z.string().optional(),
  }),
  gate_summary: z.object({
    passed: z.number().int().min(0),
    failed: z.number().int().min(0),
    pending: z.number().int().min(0),
    blocked: z.number().int().min(0),
  }),
  component_status: z.object({
    factor_library: componentStatusSchema,
    composition_graph: componentStatusSchema,
    research_report: componentStatusSchema,
    z9_review: componentStatusSchema,
    evidence_chain: componentStatusSchema,
    run_state: componentStatusSchema,
    gate_state: componentStatusSchema,
    audit_trail: componentStatusSchema,
  }),
  recent_activity: z.array(
    z.object({
      id: z.string(),
      type: z.enum([
        'gate_check',
        'pipeline_run',
        'component_status_change',
        'audit_event',
        'seal_change',
        'system_event',
      ]),
      message: z.string(),
      timestamp: z.string(),
      actor: z.string().optional(),
      details: z.record(z.unknown()).optional(),
    })
  ),
  readonly: z.literal(true),
});

export type DashboardSummary = z.infer<typeof dashboardSummarySchema>;

// ─── Capabilities ───────────────────────────────────────────────────────────

export const capabilitySchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string().optional(),
  status: z.enum(['disabled_default', 'enabled', 'degraded', 'blocked', 'error']),
  permissions: z.object({
    can_view: z.literal(true),
    can_invoke: z.literal(false),
    can_configure: z.literal(false),
    can_enable: z.literal(false),
  }).optional(),
});

export const capabilitiesSchema = z.object({
  capabilities: z.array(capabilitySchema),
  total_count: z.number().int(),
  enabled_count: z.literal(0),
  readonly: z.literal(true),
});

export type CapabilitiesResponse = z.infer<typeof capabilitiesSchema>;
export type Capability = z.infer<typeof capabilitySchema>;

// ─── Factor Library ─────────────────────────────────────────────────────────

export const factorSchema = z.object({
  id: z.string(),
  name: z.string(),
  seal_status: z.enum(['SEALED', 'UNSEALED', 'DEGRADED']),
  category: z.string().optional(),
  evaluation_count: z.number().int().optional(),
  last_evaluated: z.string().optional(),
});

export const factorLibrarySchema = z.object({
  seal_status: z.string(),
  factor_count: z.number().int(),
  readonly: z.literal(true),
  factors: z.array(factorSchema),
});

export type FactorLibraryResponse = z.infer<typeof factorLibrarySchema>;
export type Factor = z.infer<typeof factorSchema>;

// ─── Composition Graph ──────────────────────────────────────────────────────

export const graphNodeSchema = z.object({
  id: z.string(),
  label: z.string(),
  status: z.enum(['disabled_default', 'enabled', 'degraded', 'blocked']),
  type: z.enum(['skill', 'fact', 'evidence', 'review', 'report']).optional(),
  dependencies: z.array(z.string()).optional(),
});

export const graphEdgeSchema = z.object({
  from: z.string(),
  to: z.string(),
  type: z.enum(['depends_on', 'produces', 'reviews', 'feeds_into']),
  status: z.enum(['active', 'degraded', 'blocked']).optional(),
});

export const compositionGraphSchema = z.object({
  nodes: z.array(graphNodeSchema),
  edges: z.array(graphEdgeSchema),
  node_count: z.number().int(),
  edge_count: z.number().int(),
  readonly: z.literal(true),
  disabled_default: z.literal(true),
});

export type CompositionGraphResponse = z.infer<typeof compositionGraphSchema>;
export type GraphNode = z.infer<typeof graphNodeSchema>;
export type GraphEdge = z.infer<typeof graphEdgeSchema>;

// ─── Research Report ────────────────────────────────────────────────────────

export const researchReportSchema = z.object({
  report_status: z.enum(['disabled_default', 'generating', 'ready', 'error']),
  recent_reports: z.array(
    z.object({
      id: z.string(),
      title: z.string(),
      status: z.enum(['draft', 'generating', 'ready', 'error']),
      created_at: z.string(),
      confidence: z.number().min(0).max(1).optional(),
    })
  ),
  generation_enabled: z.literal(false),
  readonly: z.literal(true),
});

export type ResearchReportResponse = z.infer<typeof researchReportSchema>;

// ─── Z9 Review ──────────────────────────────────────────────────────────────

export const z9ReviewSchema = z.object({
  review_status: z.enum(['disabled_default', 'idle', 'reviewing', 'complete']),
  queue_size: z.number().int(),
  reviews: z.array(
    z.object({
      id: z.string(),
      target: z.string(),
      status: z.enum(['pending', 'in_progress', 'completed', 'rejected']),
      created_at: z.string(),
      findings: z.array(z.string()).optional(),
    })
  ),
  review_enabled: z.literal(false),
  readonly: z.literal(true),
});

export type Z9ReviewResponse = z.infer<typeof z9ReviewSchema>;

// ─── Evidence Chain ─────────────────────────────────────────────────────────

export const evidenceNodeSchema = z.object({
  id: z.string(),
  type: z.enum(['input', 'intermediate', 'output', 'decision', 'review']),
  content: z.string(),
  timestamp: z.string().optional(),
  hash: z.string().optional(),
  source: z.string().optional(),
});

export const evidenceLinkSchema = z.object({
  from: z.string(),
  to: z.string(),
  type: z.enum(['derives_from', 'confirms', 'contradicts', 'references']),
});

export const evidenceChainSchema = z.object({
  chain_id: z.string(),
  nodes: z.array(evidenceNodeSchema),
  links: z.array(evidenceLinkSchema),
  readonly: z.literal(true),
});

export type EvidenceChainResponse = z.infer<typeof evidenceChainSchema>;
export type EvidenceNode = z.infer<typeof evidenceNodeSchema>;

// ─── Run State ──────────────────────────────────────────────────────────────

export const pipelineRunSchema = z.object({
  run_id: z.string(),
  pipeline: z.string(),
  status: z.enum(['running', 'completed', 'aborted', 'degraded', 'blocked']),
  started_at: z.string(),
  completed_at: z.string().optional(),
  abort_reason: z.string().optional(),
  readonly: z.literal(true),
});

export const runStateSchema = z.object({
  current_state: z.enum(['idle', 'running', 'completed', 'aborted', 'degraded']),
  pipeline_runs: z.array(pipelineRunSchema),
  readonly: z.literal(true),
});

export type RunStateResponse = z.infer<typeof runStateSchema>;
export type PipelineRun = z.infer<typeof pipelineRunSchema>;

// ─── Gate State ─────────────────────────────────────────────────────────────

export const gateEntrySchema = z.object({
  gate_id: z.string(),
  name: z.string(),
  status: z.enum(['passed', 'failed', 'pending', 'blocked', 'skipped']),
  last_checked: z.string().optional(),
  details: z.string().optional(),
  required_permission: z.string().optional(),
});

export const gateStateSchema = z.object({
  gates: z.array(gateEntrySchema),
  summary: z.object({
    passed: z.number().int(),
    failed: z.number().int(),
    pending: z.number().int(),
    blocked: z.number().int(),
  }).optional(),
  readonly: z.literal(true),
});

export type GateStateResponse = z.infer<typeof gateStateSchema>;
export type GateEntry = z.infer<typeof gateEntrySchema>;

// ─── Audit Trail ────────────────────────────────────────────────────────────

export const auditEntrySchema = z.object({
  id: z.string(),
  action: z.string(),
  timestamp: z.string(),
  actor: z.string(),
  target: z.string().optional(),
  result: z.enum(['success', 'blocked', 'error', 'degraded']),
  details: z.record(z.unknown()).optional(),
});

export const auditTrailSchema = z.object({
  entries: z.array(auditEntrySchema),
  total_count: z.number().int(),
  readonly: z.literal(true),
});

export type AuditTrailResponse = z.infer<typeof auditTrailSchema>;
export type AuditEntry = z.infer<typeof auditEntrySchema>;
