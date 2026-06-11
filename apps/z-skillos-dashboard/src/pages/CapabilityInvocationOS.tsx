import { useQuery } from '@tanstack/react-query';
import { fetchCapabilities } from '../api/endpoints';
import { MOCK_CAPABILITIES } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { EmptyState } from '../components/empty/EmptyState';

export function CapabilityInvocationOS() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['capabilities'],
    queryFn: fetchCapabilities,
    placeholderData: MOCK_CAPABILITIES,
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
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load capabilities</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data || data.capabilities.length === 0) {
    return (
      <EmptyState
        title="No Capabilities"
        message="No capabilities registered in the system."
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Capability Invocation OS</h2>
          <p className="text-sm text-slate-500">Read-only skill catalog viewer — all skills disabled by default</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      {/* Summary metrics */}
      <div className="grid grid-cols-3 gap-4">
        <SummaryCard title="Total" icon={'\u{1F4E6}'}>
          <p className="text-3xl font-bold text-slate-100">{data.total_count}</p>
        </SummaryCard>
        <SummaryCard title="Enabled" icon={'\u{2705}'} status="ok">
          <p className="text-3xl font-bold text-skillos-green">{data.enabled_count}</p>
        </SummaryCard>
        <SummaryCard title="Mode" icon={'\u{1F512}'} status="info">
          <p className="text-sm text-slate-300 mt-1">All skills disabled by default (P0 merge policy)</p>
        </SummaryCard>
      </div>

      {/* Capability table */}
      <SummaryCard title="Skill Catalog" icon={'\u{1F5A5}\u{FE0F}'}>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Status</th>
                <th>Can Invoke</th>
                <th>Can Configure</th>
              </tr>
            </thead>
            <tbody>
              {data.capabilities.map((cap) => (
                <tr key={cap.id}>
                  <td className="font-mono text-xs text-skillos-blue">{cap.id}</td>
                  <td className="font-medium text-slate-200">{cap.name}</td>
                  <td className="text-slate-400 max-w-xs truncate">{cap.description}</td>
                  <td><StatusBadge status={cap.status.toUpperCase()} /></td>
                  <td><span className="text-xs text-slate-600">{'\u{1F6AB}'} Blocked</span></td>
                  <td><span className="text-xs text-slate-600">{'\u{1F6AB}'} Blocked</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SummaryCard>
    </div>
  );
}
