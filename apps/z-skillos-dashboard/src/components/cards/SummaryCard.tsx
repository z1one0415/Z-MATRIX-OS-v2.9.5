import React from 'react';

interface SummaryCardProps {
  title: string;
  icon: string;
  children: React.ReactNode;
  status?: 'ok' | 'warning' | 'critical' | 'info';
  className?: string;
}

const statusBorderMap: Record<string, string> = {
  ok: 'border-l-skillos-green',
  warning: 'border-l-skillos-amber',
  critical: 'border-l-skillos-red',
  info: 'border-l-skillos-blue',
};

export function SummaryCard({ title, icon, children, status = 'info', className = '' }: SummaryCardProps) {
  return (
    <div className={`card border-l-4 ${statusBorderMap[status]} ${className}`}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">{icon}</span>
        <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
      </div>
      {children}
    </div>
  );
}
