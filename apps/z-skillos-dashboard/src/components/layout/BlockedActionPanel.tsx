const BLOCKED_ACTIONS = [
  'start_pipeline', 'stop_pipeline', 'abort_pipeline',
  'enable_skill', 'disable_skill', 'invoke_skill', 'configure_skill', 'promote_skill',
  'promote_factor', 'advance_f8', 'unseal_factor', 'create_factor', 'modify_factor', 'delete_factor',
  'add_node', 'remove_node', 'add_edge', 'remove_edge', 'modify_graph', 'reconfigure_flow',
  'generate_report', 'modify_report', 'delete_report',
  'start_review', 'submit_review', 'approve_review', 'reject_review', 'modify_review_criteria',
  'modify_evidence', 'delete_evidence', 'inject_evidence', 'tamper_hash',
  'start_run', 'stop_run', 'retry_run', 'modify_run_config',
  'open_gate', 'close_gate', 'bypass_gate', 'modify_gate_rules',
  'modify_audit', 'delete_audit', 'redact_entry', 'purge_trail',
  'modify_permissions', 'enable_runtime', 'enable_production', 'enable_paper_trading',
  'modify_safety_boundary', 'change_contract',
  'set_confidence', 'promote_to_production',
];

export function BlockedActionPanel() {
  return (
    <div className="card border-red-900/40">
      <div className="flex items-center gap-2 mb-3">
        <span>{'\u{1F6AB}'}</span>
        <h3 className="text-sm font-semibold text-red-300">Blocked Actions (Contract Freeze)</h3>
        <span className="safety-badge safety-badge-blocked">{BLOCKED_ACTIONS.length} BLOCKED</span>
      </div>
      <p className="text-xs text-slate-400 mb-3">
        These actions are permanently blocked under the A1_CONTRACT_FREEZE seal.
      </p>
      <div className="flex flex-wrap gap-1">
        {BLOCKED_ACTIONS.map((action) => (
          <span
            key={action}
            className="px-2 py-0.5 text-xs font-mono rounded bg-slate-800 text-slate-500 border border-slate-700"
            title={`Permanently blocked: ${action}`}
          >
            {action}
          </span>
        ))}
      </div>
    </div>
  );
}
