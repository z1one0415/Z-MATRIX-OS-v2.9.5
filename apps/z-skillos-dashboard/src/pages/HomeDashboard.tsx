import { useQuery } from '@tanstack/react-query';
import { fetchDashboardSummary } from '../api/endpoints';
import { MOCK_DASHBOARD } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { MetricCard } from '../components/cards/MetricCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { GateStatusChart } from '../components/charts/GateStatusChart';
import { EmptyState } from '../components/empty/EmptyState';

export function HomeDashboard() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: fetchDashboardSummary,
    placeholderData: MOCK_DASHBOARD,
  });

  // Loading state
  if (isLoading && !data) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-skillos-blue border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-slate-500">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (isError && !data) {
    return (
      <div className="card border-red-900/40">
        <div className="flex items-center gap-2 mb-2">
          <span>{'\u{274C}'}</span>
          <h2 className="text-lg font-bold text-red-300">Failed to load dashboard</h2>
        </div>
        <p className="text-sm text-slate-400">
          {error instanceof Error ? error.message : 'Unknown error occurred.'}
        </p>
      </div>
    );
  }

  // Empty state
  if (!data) {
    return (
      <EmptyState
        icon={'\u{1F4CA}'}
        title="No Dashboard Data"
        message="No dashboard data available yet. System may be initializing."
      />
    );
  }

  const { system_health, gate_summary, component_status, recent_activity } = data;

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Home Dashboard</h2>
          <p className="text-sm text-slate-500">System overview, gate status, and recent activity</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      {/* RESTRICTIONS BANNER */}
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

      {/* Metric cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard label="System Health" value={system_health.status} status="ok" />
        <MetricCard label="Uptime" value={Math.floor(system_health.uptime_seconds / 3600)} unit="hrs" status="ok" />
        <MetricCard label="Gates Passed" value={gate_summary.passed} status="ok" />
        <MetricCard label="Version" value={system_health.version ?? 'N/A'} />
      </div>

      {/* Gate Summary */}
      <SummaryCard title="Gate Summary" icon={'\u{1F6E1}\u{FE0F}'}>
        <GateStatusChart
          passed={gate_summary.passed}
          failed={gate_summary.failed}
          pending={gate_summary.pending}
          blocked={gate_summary.blocked}
        />
      </SummaryCard>

      {/* Component Status Grid */}
      <SummaryCard title="Component Status" icon={'\u{1F9E9}'}>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.entries(component_status).map(([name, status]) => (
            <div key={name} className="flex items-center justify-between p-2 rounded-lg bg-slate-800/40">
              <span className="text-xs font-medium text-slate-400 capitalize">
                {name.replace(/_/g, ' ')}
              </span>
              <StatusBadge status={status.toUpperCase()} />
            </div>
          ))}
        </div>
      </SummaryCard>

      {/* Recent Activity */}
      <SummaryCard title="Recent Activity" icon={'\u{1F4CB}'} status={recent_activity.length > 0 ? 'ok' : 'info'}>
        {recent_activity.length === 0 ? (
          <p className="text-sm text-slate-500">No recent activity recorded.</p>
        ) : (
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {recent_activity.map((entry) => (
              <div key={entry.id} className="flex items-start gap-3 p-2 rounded bg-slate-800/20 text-xs">
                <span className="text-slate-500 font-mono shrink-0">
                  {new Date(entry.timestamp).toLocaleTimeString()}
                </span>
                <span className="text-slate-400">{entry.type}</span>
                <span className="text-slate-300 flex-1">{entry.message}</span>
              </div>
            ))}
          </div>
        )}
      </SummaryCard>
    </div>
  );
}
