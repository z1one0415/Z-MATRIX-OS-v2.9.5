import { useQuery } from '@tanstack/react-query';
import { fetchCompositionGraph } from '../api/endpoints';
import { MOCK_COMPOSITION_GRAPH } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { MetricCard } from '../components/cards/MetricCard';
import { EmptyState } from '../components/empty/EmptyState';

const NODE_COLORS: Record<string, string> = {
  enabled: 'bg-skillos-green',
  degraded: 'bg-skillos-amber',
  disabled_default: 'bg-slate-600',
  blocked: 'bg-skillos-red',
};

export function CompositionGraph() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['composition-graph'],
    queryFn: fetchCompositionGraph,
    placeholderData: MOCK_COMPOSITION_GRAPH,
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
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load composition graph</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data || data.nodes.length === 0) {
    return <EmptyState title="No Graph Data" message="No composition graph data available. Graph may be uninitialized." />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Composition Graph</h2>
          <p className="text-sm text-slate-500">B1 graph summary — view-only, no editing</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <MetricCard label="Nodes" value={data.node_count} />
        <MetricCard label="Edges" value={data.edge_count} />
        <MetricCard label="Read Only" value="Yes" status="ok" />
      </div>

      {/* Nodes */}
      <SummaryCard title="Nodes" icon={'\u{1F5A5}\u{FE0F}'}>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
          {data.nodes.map((node) => (
            <div key={node.id} className="flex items-center gap-2 p-2 rounded bg-slate-800/40">
              <div className={`w-2.5 h-2.5 rounded-full ${NODE_COLORS[node.status] ?? 'bg-slate-600'}`} />
              <div className="min-w-0">
                <p className="text-xs text-slate-200 truncate">{node.label}</p>
                <p className="text-xs text-slate-500">{node.type} - <StatusBadge status={node.status.toUpperCase()} /></p>
              </div>
            </div>
          ))}
        </div>
      </SummaryCard>

      {/* Edges */}
      <SummaryCard title="Edges" icon={'\u{1F517}'}>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>From</th>
                <th>To</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              {data.edges.map((edge, i) => (
                <tr key={`${edge.from}-${edge.to}-${i}`}>
                  <td className="font-mono text-xs text-skillos-blue">{edge.from}</td>
                  <td className="font-mono text-xs text-skillos-blue">{edge.to}</td>
                  <td><StatusBadge status={edge.type.replace(/_/g, ' ')} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SummaryCard>
    </div>
  );
}
