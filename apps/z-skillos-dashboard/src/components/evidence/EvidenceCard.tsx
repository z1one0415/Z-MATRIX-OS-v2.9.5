import type { EvidenceNode } from '../../api/schemas';

interface EvidenceCardProps {
  node: EvidenceNode;
  index: number;
  isLast: boolean;
}

export function EvidenceCard({ node, index, isLast }: EvidenceCardProps) {
  const typeIcons: Record<string, string> = {
    input: '\u{1F4E5}',
    intermediate: '\u{2699}\u{FE0F}',
    output: '\u{1F4E4}',
    decision: '\u{1F3AF}',
    review: '\u{1F50D}',
  };

  return (
    <div className="relative pl-8 pb-6">
      {/* Timeline connector */}
      {!isLast && (
        <div className="absolute left-4 top-8 bottom-0 w-0.5 bg-slate-700" />
      )}

      {/* Node dot */}
      <div className="absolute left-2.5 top-1 w-3 h-3 rounded-full bg-skillos-blue border-2 border-slate-800" />

      <div className="card p-4">
        <div className="flex items-center gap-2 mb-2">
          <span>{typeIcons[node.type] || '\u{2753}'}</span>
          <span className="text-xs font-semibold text-skillos-blue uppercase">{node.type}</span>
          <span className="text-xs text-slate-500">{node.id}</span>
        </div>
        <p className="text-sm text-slate-300 mb-2">{node.content}</p>
        <div className="flex gap-4 text-xs text-slate-500">
          {node.timestamp && <span>{'\u{1F552}'} {new Date(node.timestamp).toLocaleString()}</span>}
          {node.source && <span>{'\u{1F4E1}'} {node.source}</span>}
          {node.hash && (
            <span className="font-mono text-slate-600">{node.hash}</span>
          )}
        </div>
      </div>
    </div>
  );
}
