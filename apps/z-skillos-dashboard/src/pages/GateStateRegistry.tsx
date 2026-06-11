import { useQuery } from '@tanstack/react-query';
import { fetchGateState } from '../api/endpoints';
import { MOCK_GATE_STATE } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { GateTimeline } from '../components/gates/GateTimeline';
import { GateStatusChart } from '../components/charts/GateStatusChart';
import { EmptyState } from '../components/empty/EmptyState';

export function GateStateRegistry() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['gate-state'],
    queryFn: fetchGateState,
    placeholderData: MOCK_GATE_STATE,
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
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load gate state</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data || data.gates.length === 0) {
    return <EmptyState title="No Gates" message="No safety gates registered in the system." />;
  }

  const summary = data.summary ?? { passed: 0, failed: 0, pending: 0, blocked: 0 };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Gate State Registry</h2>
          <p className="text-sm text-slate-500">Gate pass/fail/pending matrix for all safety gates</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      {/* Summary chart */}
      <SummaryCard title="Gate Overview" icon={'\u{1F6A6}'}>
        <GateStatusChart
          passed={summary.passed}
          failed={summary.failed}
          pending={summary.pending}
          blocked={summary.blocked}
        />
      </SummaryCard>

      {/* Gate timeline */}
      <SummaryCard title="F7 Gate Chain" icon={'\u{1F6E1}\u{FE0F}'}>
        <GateTimeline gates={data.gates} />
      </SummaryCard>
    </div>
  );
}
