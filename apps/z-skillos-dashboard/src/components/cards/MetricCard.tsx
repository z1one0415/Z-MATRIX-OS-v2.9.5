interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  trend?: 'up' | 'down' | 'flat';
  status?: 'ok' | 'warning' | 'critical';
}

const statusColorMap: Record<string, string> = {
  ok: 'text-skillos-green',
  warning: 'text-skillos-amber',
  critical: 'text-skillos-red',
};

export function MetricCard({ label, value, unit, trend, status = 'ok' }: MetricCardProps) {
  const trendIcon = trend === 'up' ? '\u{2191}' : trend === 'down' ? '\u{2193}' : '';

  return (
    <div className="card text-center py-4">
      <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">{label}</p>
      <p className={`text-2xl font-bold ${statusColorMap[status]}`}>
        {value}
        {unit && <span className="text-sm ml-1 text-slate-400">{unit}</span>}
      </p>
      {trend && (
        <p className="text-xs text-slate-500 mt-1">
          {trendIcon} {trend}
        </p>
      )}
    </div>
  );
}
