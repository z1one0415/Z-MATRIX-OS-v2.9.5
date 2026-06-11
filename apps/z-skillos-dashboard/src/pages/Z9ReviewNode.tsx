import { useQuery } from '@tanstack/react-query';
import { fetchZ9Review } from '../api/endpoints';
import { MOCK_Z9_REVIEW } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { EmptyState } from '../components/empty/EmptyState';

export function Z9ReviewNode() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['z9-review'],
    queryFn: fetchZ9Review,
    placeholderData: MOCK_Z9_REVIEW,
  });

  if (isLoading && !data) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="w-8 h-8 border-2 border-skillos-blue border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (isError && !data) {
    return (
      <div className="card border-red-900/40">
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load Z9 review</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <EmptyState
        title="No Reviews"
        message="No reviews pending. Review system is disabled by default."
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Z9 Review Node</h2>
          <p className="text-sm text-slate-500">Review status — disabled by default per P0 merge policy</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <SummaryCard title="Review Status" icon={'\u{1F50D}'}>
          <StatusBadge status={data.review_status.toUpperCase()} />
        </SummaryCard>
        <SummaryCard title="Queue Size" icon={'\u{1F4CB}'}>
          <p className="text-2xl font-bold text-slate-100">{data.queue_size}</p>
        </SummaryCard>
        <SummaryCard title="Review Enabled" icon={'\u{26D4}'}>
          <StatusBadge status={data.review_enabled ? 'ENABLED' : 'DISABLED'} />
        </SummaryCard>
      </div>

      <SummaryCard title="Reviews" icon={'\u{2705}'}>
        {data.reviews.length === 0 ? (
          <EmptyState title="No Reviews in Queue" message="No reviews pending. Review system is disabled by default." />
        ) : (
          <div className="space-y-3">
            {data.reviews.map((review) => (
              <div key={review.id} className="card p-4 border-slate-700/30">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-slate-200">Target: {review.target}</span>
                  <StatusBadge status={review.status.toUpperCase()} />
                </div>
                <div className="text-xs text-slate-500 space-y-1">
                  <p>ID: {review.id}</p>
                  <p>Created: {new Date(review.created_at).toLocaleString()}</p>
                  {review.findings && review.findings.length > 0 && (
                    <ul className="list-disc list-inside text-slate-400">
                      {review.findings.map((f, i) => <li key={i}>{f}</li>)}
                    </ul>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </SummaryCard>
    </div>
  );
}
