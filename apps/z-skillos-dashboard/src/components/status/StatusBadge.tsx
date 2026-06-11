type StatusType = 'PASS' | 'PASSED' | 'FAIL' | 'FAILED' | 'PENDING' | 'BLOCKED' | 'DEGRADED' | 'SKIPPED' | 'DISABLED' | 'DISABLED_DEFAULT' | 'READY' | 'GREEN' | 'AMBER' | 'RED' | 'OK' | 'NOMINAL' | 'SEALED' | 'UNSEALED' | 'DRAFT' | 'COMPLETED' | 'COMPLETE' | 'IDLE' | string;

interface StatusBadgeProps {
  status: StatusType;
  size?: 'sm' | 'md';
}

const STATUS_STYLES: Record<StatusType, string> = {
  PASS: 'bg-green-900/30 text-green-400 border-green-600/40',
  PASSED: 'bg-green-900/30 text-green-400 border-green-600/40',
  FAIL: 'bg-red-900/30 text-red-400 border-red-600/40',
  FAILED: 'bg-red-900/30 text-red-400 border-red-600/40',
  PENDING: 'bg-amber-900/30 text-amber-400 border-amber-600/40',
  BLOCKED: 'bg-slate-800 text-slate-400 border-slate-600',
  DEGRADED: 'bg-amber-900/30 text-amber-400 border-amber-600/40',
  SKIPPED: 'bg-slate-800 text-slate-500 border-slate-600',
  DISABLED: 'bg-slate-800 text-slate-500 border-slate-600',
  DISABLED_DEFAULT: 'bg-slate-800 text-slate-500 border-slate-600',
  READY: 'bg-green-900/30 text-green-400 border-green-600/40',
  GREEN: 'bg-green-900/30 text-green-400 border-green-600/40',
  AMBER: 'bg-amber-900/30 text-amber-400 border-amber-600/40',
  RED: 'bg-red-900/30 text-red-400 border-red-600/40',
  OK: 'bg-green-900/30 text-green-400 border-green-600/40',
  NOMINAL: 'bg-green-900/30 text-green-400 border-green-600/40',
  SEALED: 'bg-green-900/30 text-green-400 border-green-600/40',
  UNSEALED: 'bg-amber-900/30 text-amber-400 border-amber-600/40',
  DRAFT: 'bg-slate-800 text-slate-500 border-slate-600',
  COMPLETED: 'bg-green-900/30 text-green-400 border-green-600/40',
  COMPLETE: 'bg-green-900/30 text-green-400 border-green-600/40',
  IDLE: 'bg-slate-800 text-slate-400 border-slate-600',
  SCHEDULED: 'bg-blue-900/30 text-blue-400 border-blue-600/40',
  RUNNING: 'bg-blue-900/30 text-blue-400 border-blue-600/40',
  ABORTED: 'bg-red-900/30 text-red-400 border-red-600/40',
  ERROR: 'bg-red-900/30 text-red-400 border-red-600/40',
};

function getStatusStyle(status: StatusType): string {
  // Normalize case
  const upper = status.toUpperCase() as StatusType;
  if (STATUS_STYLES[upper]) return STATUS_STYLES[upper];
  // Fallback
  if (status.toLowerCase().includes('disabled')) return STATUS_STYLES.DISABLED_DEFAULT;
  if (status.toLowerCase().includes('blocked')) return STATUS_STYLES.BLOCKED;
  if (status.toLowerCase().includes('error')) return STATUS_STYLES.FAILED;
  if (status.toLowerCase().includes('ok')) return STATUS_STYLES.OK;
  return 'bg-slate-800 text-slate-400 border-slate-600';
}

export function StatusBadge({ status, size = 'sm' }: StatusBadgeProps) {
  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm';
  return (
    <span className={`inline-flex items-center rounded-full border font-semibold ${sizeClasses} ${getStatusStyle(status)}`}>
      {status}
    </span>
  );
}
