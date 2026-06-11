import { useQuery } from '@tanstack/react-query';
import { fetchFactorLibrary } from '../api/endpoints';
import { MOCK_FACTORS } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { MetricCard } from '../components/cards/MetricCard';
import { EmptyState } from '../components/empty/EmptyState';

export function FactorLibrary() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['factor-library'],
    queryFn: fetchFactorLibrary,
    placeholderData: MOCK_FACTORS,
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
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load factor library</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data || data.factors.length === 0) {
    return <EmptyState title="No Factors" message="No factors have been registered in the library." />;
  }

  const sealed = data.factors.filter((f) => f.seal_status === 'SEALED').length;
  const draft = data.factors.filter((f) => f.seal_status === 'DRAFT' || f.seal_status === 'DEGRADED').length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Factor Library</h2>
          <p className="text-sm text-slate-500">Browse factor seal status and evaluation matrix (read-only, diagnostic-only)</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <MetricCard label="Total Factors" value={data.factor_count} />
        <MetricCard label="Sealed" value={sealed} status="ok" />
        <MetricCard label="Draft/Degraded" value={draft} status={draft > 0 ? 'warning' : 'ok'} />
        <MetricCard label="Seal Status" value={data.seal_status} status={data.seal_status === 'SEALED' ? 'ok' : 'warning'} />
      </div>

      <SummaryCard title="Factor List" icon={'\u{1F9E9}'}>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Category</th>
                <th>Seal</th>
                <th>Evaluations</th>
                <th>Last Evaluated</th>
              </tr>
            </thead>
            <tbody>
              {data.factors.map((factor) => (
                <tr key={factor.id}>
                  <td className="font-mono text-xs text-skillos-blue">{factor.id}</td>
                  <td className="font-medium text-slate-200">{factor.name}</td>
                  <td><StatusBadge status={factor.category ?? 'N/A'} /></td>
                  <td><StatusBadge status={factor.seal_status} /></td>
                  <td className="text-slate-400">{factor.evaluation_count ?? 0}</td>
                  <td className="text-xs text-slate-500">
                    {factor.last_evaluated ? new Date(factor.last_evaluated).toLocaleDateString() : 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SummaryCard>
    </div>
  );
}
