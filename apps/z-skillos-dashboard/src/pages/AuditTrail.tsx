import { useQuery } from '@tanstack/react-query';
import { fetchAuditTrail } from '../api/endpoints';
import { MOCK_AUDIT_TRAIL } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { EmptyState } from '../components/empty/EmptyState';

export function AuditTrail() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['audit-trail'],
    queryFn: fetchAuditTrail,
    placeholderData: MOCK_AUDIT_TRAIL,
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
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load audit trail</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data) {
    return <EmptyState title="No Audit Entries" message="No audit entries recorded yet." />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Audit Trail</h2>
          <p className="text-sm text-slate-500">Full audit trail of all actions, decisions, and timestamps</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      <SummaryCard title="Audit Log" icon={'\u{1F4CB}'} status="info">
        <p className="text-xs text-slate-500 mb-3">
          Total entries: <span className="font-semibold text-slate-200">{data.total_count}</span>
        </p>
        {data.entries.length === 0 ? (
          <EmptyState title="No Audit Entries" message="No audit entries recorded yet." />
        ) : (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Timestamp</th>
                  <th>Actor</th>
                  <th>Action</th>
                  <th>Result</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                {data.entries.map((entry) => (
                  <tr key={entry.id}>
                    <td className="font-mono text-xs text-skillos-blue">{entry.id}</td>
                    <td className="text-xs text-slate-500 whitespace-nowrap">
                      {new Date(entry.timestamp).toLocaleString()}
                    </td>
                    <td className="font-medium text-slate-300">{entry.actor}</td>
                    <td className="text-slate-200">{entry.action}</td>
                    <td><StatusBadge status={entry.result.toUpperCase()} /></td>
                    <td className="text-xs text-slate-400 max-w-xs truncate">
                      {entry.details ? JSON.stringify(entry.details) : '—'}
                    </td>
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
