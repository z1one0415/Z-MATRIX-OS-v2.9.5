import { useQuery } from '@tanstack/react-query';
import { fetchHealth } from '../api/endpoints';
import { MOCK_HEALTH } from '../api/mockClient';

export function Topbar() {
  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: fetchHealth,
    placeholderData: MOCK_HEALTH,
    staleTime: 30_000,
  });

  const status = health?.status ?? 'ok';
  const version = health?.version ?? 'v0.1.0-rc';

  const statusColor =
    status === 'ok' ? 'bg-skillos-green' : status === 'degraded' ? 'bg-skillos-amber' : 'bg-skillos-red';

  return (
    <header className="flex items-center justify-between px-6 py-3 border-b border-slate-800 bg-slate-900/60">
      {/* Breadcrumbs placeholder */}
      <div className="flex items-center gap-2 text-sm text-slate-400">
        <span>Z-SkillOS</span>
        <span className="text-slate-600">/</span>
        <span className="text-slate-300">Dashboard</span>
      </div>

      {/* Right-side indicators */}
      <div className="flex items-center gap-4">
        {/* Mode badges */}
        <span className="safety-badge safety-badge-readonly">
          <span>🔒</span>
          READ-ONLY
        </span>
        <span className="safety-badge safety-badge-disabled">
          <span>⛔</span>
          DISABLED_DEFAULT
        </span>

        {/* System status */}
        <div className="flex items-center gap-2 text-xs">
          <span className={`w-2 h-2 rounded-full ${statusColor} animate-pulse-slow`} />
          <span className="text-slate-400 capitalize">{status}</span>
        </div>

        {/* Version */}
        <div className="text-xs text-slate-500 border border-slate-700 rounded px-2 py-0.5">
          {version}
        </div>
      </div>
    </header>
  );
}
