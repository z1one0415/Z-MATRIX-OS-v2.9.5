interface GateStatusChartProps {
  passed: number;
  failed: number;
  pending: number;
  blocked: number;
}

export function GateStatusChart({ passed, failed, pending, blocked }: GateStatusChartProps) {
  const total = passed + failed + pending + blocked;
  if (total === 0) return <p className="text-sm text-slate-500">No gate data.</p>;

  const passedPct = (passed / total) * 100;
  const failedPct = (failed / total) * 100;
  const pendingPct = (pending / total) * 100;
  const blockedPct = (blocked / total) * 100;

  return (
    <div className="space-y-3">
      <div className="h-3 rounded-full overflow-hidden flex bg-slate-800">
        {passedPct > 0 && (
          <div className="bg-skillos-green h-full" style={{ width: `${passedPct}%` }} title={`Passed: ${passed}`} />
        )}
        {failedPct > 0 && (
          <div className="bg-skillos-red h-full" style={{ width: `${failedPct}%` }} title={`Failed: ${failed}`} />
        )}
        {pendingPct > 0 && (
          <div className="bg-skillos-amber h-full" style={{ width: `${pendingPct}%` }} title={`Pending: ${pending}`} />
        )}
        {blockedPct > 0 && (
          <div className="bg-slate-600 h-full" style={{ width: `${blockedPct}%` }} title={`Blocked: ${blocked}`} />
        )}
      </div>
      <div className="flex gap-4 text-xs text-slate-400">
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-sm bg-skillos-green" />
          <span>Passed ({passed})</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-sm bg-skillos-red" />
          <span>Failed ({failed})</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-sm bg-skillos-amber" />
          <span>Pending ({pending})</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-sm bg-slate-600" />
          <span>Blocked ({blocked})</span>
        </div>
      </div>
    </div>
  );
}
