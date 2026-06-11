interface DegradedStateProps {
  title: string;
  message: string;
  degradedComponents?: string[];
  remainingComponents?: string[];
}

export function DegradedState({
  title,
  message,
  degradedComponents = [],
  remainingComponents = [],
}: DegradedStateProps) {
  return (
    <div className="card border-amber-900/40 bg-amber-950/20">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">{'\u{26A0}\u{FE0F}'}</span>
        <h3 className="text-sm font-semibold text-amber-300">{title}</h3>
        <span className="safety-badge bg-amber-900/40 border-amber-600/40 text-amber-300">DEGRADED</span>
      </div>
      <p className="text-xs text-slate-400 mb-3">{message}</p>
      {degradedComponents.length > 0 && (
        <div className="text-xs mb-2">
          <span className="text-amber-400">Degraded: </span>
          {degradedComponents.map((c, i) => (
            <span key={c} className="inline-flex items-center">
              <code className="bg-red-900/30 text-red-300 px-1 py-0.5 rounded text-xs">{c}</code>
              {i < degradedComponents.length - 1 && <span className="text-slate-600">, </span>}
            </span>
          ))}
        </div>
      )}
      {remainingComponents.length > 0 && (
        <div className="text-xs">
          <span className="text-green-400">Available: </span>
          {remainingComponents.map((c, i) => (
            <span key={c} className="inline-flex items-center">
              <code className="bg-green-900/30 text-green-300 px-1 py-0.5 rounded text-xs">{c}</code>
              {i < remainingComponents.length - 1 && <span className="text-slate-600">, </span>}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
