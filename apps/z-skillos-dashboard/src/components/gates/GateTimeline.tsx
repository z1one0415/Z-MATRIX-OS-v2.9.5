import type { GateEntry } from '../../api/schemas';
import { StatusBadge } from '../status/StatusBadge';

interface GateTimelineProps {
  gates: GateEntry[];
}

export function GateTimeline({ gates }: GateTimelineProps) {
  if (gates.length === 0) {
    return <p className="text-sm text-slate-500">No gates registered.</p>;
  }

  return (
    <div className="relative">
      <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-slate-700" />
      <div className="space-y-4">
        {gates.map((gate, idx) => (
          <div key={gate.gate_id} className="relative pl-10">
            {/* Connector dot */}
            <div
              className={`absolute left-2.5 top-1.5 w-3 h-3 rounded-full border-2 border-slate-800 ${
                gate.status === 'passed' ? 'bg-skillos-green' :
                gate.status === 'failed' ? 'bg-skillos-red' :
                gate.status === 'blocked' ? 'bg-slate-600' :
                'bg-skillos-amber'
              }`}
            />

            <div className="card p-4">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-skillos-blue">{gate.gate_id}</span>
                  <span className="text-sm font-semibold text-slate-200">{gate.name}</span>
                </div>
                <StatusBadge status={gate.status.toUpperCase()} />
              </div>
              {gate.details && (
                <p className="text-xs text-slate-400 mt-1">{gate.details}</p>
              )}
              {gate.last_checked && (
                <p className="text-xs text-slate-600 mt-1">
                  Checked: {new Date(gate.last_checked).toLocaleString()}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
