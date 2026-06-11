import { useQuery } from '@tanstack/react-query';
import { fetchResearchReport } from '../api/endpoints';
import { MOCK_RESEARCH_REPORT } from '../api/mockClient';
import { SummaryCard } from '../components/cards/SummaryCard';
import { StatusBadge } from '../components/status/StatusBadge';
import { SafetyBadge } from '../components/status/SafetyBadge';
import { EmptyState } from '../components/empty/EmptyState';

export function ResearchReportNode() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['research-report'],
    queryFn: fetchResearchReport,
    placeholderData: MOCK_RESEARCH_REPORT,
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
        <h2 className="text-lg font-bold text-red-300 mb-2">{'\u{274C}'} Failed to load research reports</h2>
        <p className="text-sm text-slate-400">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <EmptyState
        title="No Research Reports"
        message="No research reports available. Report generation is disabled by default."
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100">Research Report Node</h2>
          <p className="text-sm text-slate-500">Z2 report sections preview — generation disabled by default</p>
        </div>
        <div className="flex gap-2">
          <SafetyBadge label="readonly" />
          <SafetyBadge label="disabled-default" />
        </div>
      </div>

      {/* Status */}
      <div className="grid grid-cols-3 gap-4">
        <SummaryCard title="Report Status" icon={'\u{1F4C4}'}>
          <StatusBadge status={data.report_status.toUpperCase()} />
        </SummaryCard>
        <SummaryCard title="Generation" icon={'\u{2699}\u{FE0F}'}>
          <StatusBadge status={data.generation_enabled ? 'ENABLED' : 'DISABLED'} />
        </SummaryCard>
        <SummaryCard title="Reports Available" icon={'\u{1F4E6}'}>
          <p className="text-2xl font-bold text-slate-100">{data.recent_reports.length}</p>
        </SummaryCard>
      </div>

      {/* Reports list */}
      <SummaryCard title="Recent Reports" icon={'\u{1F4C4}'}>
        {data.recent_reports.length === 0 ? (
          <EmptyState
            icon={'\u{1F4C4}'}
            title="No Reports"
            message="No research reports have been generated. Report generation is disabled by default."
          />
        ) : (
          <div className="space-y-3">
            {data.recent_reports.map((report) => (
              <div key={report.id} className="card p-4 border-slate-700/30">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-slate-200">{report.title}</span>
                  <StatusBadge status={report.status.toUpperCase()} />
                </div>
                <div className="flex items-center gap-3 text-xs text-slate-500">
                  <span>ID: {report.id}</span>
                  <span>Created: {new Date(report.created_at).toLocaleString()}</span>
                  {report.confidence !== undefined && (
                    <span>Confidence: {(report.confidence * 100).toFixed(0)}%</span>
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
