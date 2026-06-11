import { useQuery } from '@tanstack/react-query';
import { fetchEvidenceChain } from '../api/endpoints';
import { MOCK_EVIDENCE_CHAIN } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { EvidenceCard } from '../components/evidence/EvidenceCard';
import { EmptyState } from '../components/empty/EmptyState';

export function EvidenceChain() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['evidence-chain'],
    queryFn: fetchEvidenceChain,
    placeholderData: MOCK_EVIDENCE_CHAIN,
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
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load evidence chain</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data || data.nodes.length === 0) {
    return <EmptyState title="No Evidence Chain" message="No evidence chain data available." />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Evidence Chain Viewer</h2>
          <p className="text-sm text-slate-500">
            Full evidence chain traversal with hash verification — chain ID: {data.chain_id}
          </p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      <SummaryCard title="Chain Integrity" icon={'\u{1F512}'} status="ok">
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-slate-500">Chain ID: </span>
            <span className="font-mono text-skillos-blue">{data.chain_id}</span>
          </div>
          <div>
            <span className="text-slate-500">Nodes: </span>
            <span className="text-slate-200">{data.nodes.length}</span>
          </div>
          <div>
            <span className="text-slate-500">Links: </span>
            <span className="text-slate-200">{data.links.length}</span>
          </div>
        </div>
      </SummaryCard>

      {/* Evidence timeline */}
      <div>
        <h3 className="text-sm font-semibold text-slate-300 mb-4 ml-1">Evidence Chain Traversal</h3>
        {data.nodes.map((node, idx) => (
          <EvidenceCard
            key={node.id}
            node={node}
            index={idx}
            isLast={idx === data.nodes.length - 1}
          />
        ))}
      </div>

      {/* Links table */}
      {data.links.length > 0 && (
        <SummaryCard title="Evidence Links" icon={'\u{1F517}'}>
          <table className="data-table">
            <thead>
              <tr>
                <th>From</th>
                <th>To</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              {data.links.map((link, i) => (
                <tr key={`${link.from}-${link.to}-${i}`}>
                  <td className="font-mono text-xs text-skillos-blue">{link.from}</td>
                  <td className="font-mono text-xs text-skillos-blue">{link.to}</td>
                  <td>{link.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </SummaryCard>
      )}
    </div>
  );
}
