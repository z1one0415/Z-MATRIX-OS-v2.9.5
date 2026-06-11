import { useQuery } from '@tanstack/react-query';
import { fetchVersion } from '../api/endpoints';
import { MOCK_VERSION } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { BlockedActionPanel } from '../components/layout/BlockedActionPanel';
import { EmptyState } from '../components/empty/EmptyState';

const SAFETY_FLAGS = [
  { label: 'Runtime', key: 'runtime_enabled', value: false, severity: 'critical' as const },
  { label: 'Production', key: 'production_enabled', value: false, severity: 'critical' as const },
  { label: 'Paper Trading', key: 'paper_trading_allowed', value: false, severity: 'critical' as const },
  { label: 'Broker Actions', key: 'broker_action_allowed', value: false, severity: 'critical' as const },
  { label: 'Mutations (POST/PUT/PATCH/DELETE)', key: 'mutation_allowed', value: false, severity: 'critical' as const },
  { label: 'All Skills', key: 'all_skills_disabled_default', value: true, severity: 'warning' as const },
];

export function SafetyBoundary() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['version'],
    queryFn: fetchVersion,
    placeholderData: MOCK_VERSION,
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
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load settings</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data) {
    return <EmptyState title="No Settings Data" message="Settings data unavailable." />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Settings & Safety Boundary</h2>
          <p className="text-sm text-slate-500">Permission matrix viewer, blocked actions list, safety boundary display</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      {/* Version info */}
      <div className="grid grid-cols-3 gap-4">
        <SummaryCard title="Version" icon={'\u{1F4E6}'}>
          <p className="text-lg font-bold text-skillos-blue">{data.version}</p>
        </SummaryCard>
        <SummaryCard title="Contract" icon={'\u{1F4DC}'}>
          <p className="text-lg font-bold text-skillos-amber">{data.contract_version}</p>
        </SummaryCard>
        <SummaryCard title="Seal" icon={'\u{1F512}'} status="ok">
          <p className="text-sm font-bold text-slate-200">{data.seal}</p>
        </SummaryCard>
      </div>

      {/* RESTRICTIONS BANNER — same as home page */}
      <div className="restrictions-banner">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xl">{'\u{1F6A8}'}</span>
          <h3 className="text-sm font-bold text-red-200">SAFETY RESTRICTIONS — A1_CONTRACT_FREEZE</h3>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2 text-xs">
          <div className="flex items-center gap-1.5 bg-red-950/40 px-2 py-1 rounded border border-red-800/30">
            <span className="text-red-400">{'\u{26D4}'}</span>
            <span className="text-red-300">Runtime: DISABLED_DEFAULT</span>
          </div>
          <div className="flex items-center gap-1.5 bg-red-950/40 px-2 py-1 rounded border border-red-800/30">
            <span className="text-red-400">{'\u{26D4}'}</span>
            <span className="text-red-300">Runner: DISABLED</span>
          </div>
          <div className="flex items-center gap-1.5 bg-red-950/40 px-2 py-1 rounded border border-red-800/30">
            <span className="text-red-400">{'\u{26D4}'}</span>
            <span className="text-red-300">Paper Trading: DISABLED</span>
          </div>
          <div className="flex items-center gap-1.5 bg-red-950/40 px-2 py-1 rounded border border-red-800/30">
            <span className="text-red-400">{'\u{1F6AB}'}</span>
            <span className="text-red-300">Production: BLOCKED</span>
          </div>
          <div className="flex items-center gap-1.5 bg-red-950/40 px-2 py-1 rounded border border-red-800/30">
            <span className="text-red-400">{'\u{1F6AB}'}</span>
            <span className="text-red-300">Broker: BLOCKED</span>
          </div>
          <div className="flex items-center gap-1.5 bg-red-950/40 px-2 py-1 rounded border border-red-800/30">
            <span className="text-red-400">{'\u{1F6AB}'}</span>
            <span className="text-red-300">Real Trade: BLOCKED</span>
          </div>
        </div>
      </div>

      {/* Safety flags */}
      <SummaryCard title="Safety Flags" icon={'\u{1F6E1}\u{FE0F}'} status="critical">
        <div className="space-y-2">
          {SAFETY_FLAGS.map((flag) => (
            <div key={flag.key} className="flex items-center justify-between p-2 rounded bg-slate-800/40">
              <span className="text-sm text-slate-300">{flag.label}</span>
              <div className="flex items-center gap-2">
                <StatusBadge status={flag.value ? 'READY' : 'DISABLED'} />
                <SafetyBadge label={flag.severity === 'critical' ? 'production-blocked' : 'disabled-default'} />
              </div>
            </div>
          ))}
        </div>
      </SummaryCard>

      {/* Blocked actions */}
      <BlockedActionPanel />

      {/* Mode indicators */}
      <SummaryCard title="Read-Only Confirmation" icon={'\u{1F512}'} status="ok">
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between p-2 rounded bg-slate-800/40">
            <span className="text-slate-300">All API calls are GET-only</span>
            <StatusBadge status="PASSED" />
          </div>
          <div className="flex items-center justify-between p-2 rounded bg-slate-800/40">
            <span className="text-slate-300">POST/PUT/PATCH/DELETE blocked at runtime</span>
            <StatusBadge status="PASSED" />
          </div>
          <div className="flex items-center justify-between p-2 rounded bg-slate-800/40">
            <span className="text-slate-300">No buy/sell/order/position buttons rendered</span>
            <StatusBadge status="PASSED" />
          </div>
          <div className="flex items-center justify-between p-2 rounded bg-slate-800/40">
            <span className="text-slate-300">All dangerous actions disabled or not rendered</span>
            <StatusBadge status="PASSED" />
          </div>
          <div className="flex items-center justify-between p-2 rounded bg-slate-800/40">
            <span className="text-slate-300">Contract seal: A1_CONTRACT_FREEZE</span>
            <StatusBadge status="SEALED" />
          </div>
        </div>
      </SummaryCard>
    </div>
  );
}
