import { useQuery } from '@tanstack/react-query';
import { fetchRunState } from '../api/endpoints';
import { MOCK_RUN_STATE } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { EmptyState } from '../components/empty/EmptyState';

export function RunStateRegistry() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['run-state'],
    queryFn: fetchRunState,
    placeholderData: MOCK_RUN_STATE,
  });

  if (isLoading && !data) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="w-8 h-8 border-2 border-skillos-blue border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (isError && !data) {
    return (
      <div className="card border-red-900/40">
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load run state</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data) {
    return <EmptyState title="No Pipeline Runs" message="No pipeline runs have been recorded." />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Run State Registry</h2>
          <p className="text-sm text-slate-500">Pipeline run status and history — view-only</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      {/* Current state */}
      <SummaryCard title="Current State" icon={'\u{1F4CA}'} status="info">
        <div className="flex items-center gap-3">
          <span className="text-lg text-slate-200 font-semibold capitalize">{data.current_state}</span>
          <StatusBadge status={data.current_state.toUpperCase()} />
        </div>
      </SummaryCard>

      {/* Pipeline runs */}
      <SummaryCard title="Pipeline Runs" icon={'\u{25B6}\u{FE0F}'}>
        {data.pipeline_runs.length === 0 ? (
          <EmptyState title="No Pipeline Runs" message="No pipeline runs have been recorded." />
        ) : (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Run ID</th>
                  <th>Pipeline</th>
                  <th>Status</th>
                  <th>Started</th>
                  <th>Completed</th>
                  <th>Abort Reason</th>
                </tr>
              </thead>
              <tbody>
                {data.pipeline_runs.map((run) => (
                  <tr key={run.run_id}>
                    <td className="font-mono text-xs text-skillos-blue">{run.run_id}</td>
                    <td className="text-slate-200">{run.pipeline}</td>
                    <td><StatusBadge status={run.status.toUpperCase()} /></td>
                    <td className="text-xs text-slate-500">{new Date(run.started_at).toLocaleString()}</td>
                    <td className="text-xs text-slate-500">
                      {run.completed_at ? new Date(run.completed_at).toLocaleString() : '—'}
                    </td>
                    <td className="text-xs text-slate-500">{run.abort_reason || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </SummaryCard>
    </div>
  );
}
