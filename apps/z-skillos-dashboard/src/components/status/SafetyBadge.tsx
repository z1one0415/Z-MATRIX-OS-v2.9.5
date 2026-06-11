type SafetyLabel = 'readonly' | 'disabled-default' | 'broker-blocked' | 'production-blocked' | 'runtime-disabled' | 'paper-trading-disabled';

interface SafetyBadgeProps {
  label: SafetyLabel;
}

const SAFETY_STYLES: Record<SafetyLabel, { text: string; classes: string }> = {
  readonly: { text: 'READ-ONLY', classes: 'bg-amber-900/40 text-amber-300 border-amber-600/40' },
  'disabled-default': { text: 'DISABLED_DEFAULT', classes: 'bg-slate-800 text-slate-400 border-slate-600' },
  'broker-blocked': { text: 'BROKER BLOCKED', classes: 'bg-red-900/40 text-red-300 border-red-600/40' },
  'production-blocked': { text: 'PROD BLOCKED', classes: 'bg-red-900/40 text-red-300 border-red-600/40' },
  'runtime-disabled': { text: 'RUNTIME DISABLED', classes: 'bg-slate-800 text-slate-400 border-slate-600' },
  'paper-trading-disabled': { text: 'PAPER TRADING OFF', classes: 'bg-slate-800 text-slate-400 border-slate-600' },
};

export function SafetyBadge({ label }: SafetyBadgeProps) {
  const style = SAFETY_STYLES[label];
  if (!style) return null;
  return (
    <span className={`safety-badge ${style.classes}`}>
      <span>{'\u{1F512}'}</span>
      {style.text}
    </span>
  );
}
