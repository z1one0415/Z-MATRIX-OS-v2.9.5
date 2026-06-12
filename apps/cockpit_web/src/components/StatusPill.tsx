import type { LucideIcon } from "lucide-react";

type StatusPillProps = {
  icon: LucideIcon;
  label: string;
  tone?: "gold" | "red" | "green";
  compact?: boolean;
  tooltip?: string;
};

export function StatusPill({ icon: Icon, label, tone = "gold", compact = false, tooltip }: StatusPillProps) {
  const accessibleLabel = tooltip || label;
  const iconSize = compact ? 18 : 15;

  return (
    <span
      className={`status-pill status-pill--${tone}${compact ? " status-pill--compact" : ""}`}
      aria-label={accessibleLabel}
      title={accessibleLabel}
      tabIndex={compact ? 0 : undefined}
    >
      <Icon aria-hidden="true" size={iconSize} strokeWidth={2.2} />
      <span className="status-pill__label">{label}</span>
      {compact && tooltip ? <span className="status-pill__tooltip">{tooltip}</span> : null}
    </span>
  );
}
