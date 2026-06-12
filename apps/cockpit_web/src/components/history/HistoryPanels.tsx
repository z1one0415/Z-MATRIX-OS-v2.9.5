import {
  Archive,
  Brain,
  CheckCircle2,
  ClipboardCheck,
  FileText,
  GitPullRequestArrow,
  History,
  NotebookText,
  ShieldCheck,
  Sparkles
} from "lucide-react";
import type {
  HistoryActionDraft,
  HistoryEvent,
  HistoryKpi,
  HistoryLibraryItem,
  HistoryPageData,
  LearningPipelineNode
} from "../../services/historyApi";

type HistoryAction = HistoryActionDraft["action"];
type ActionHandler = (action: HistoryAction, payload?: Record<string, unknown>) => void;

const pipelineIcons = [FileText, Archive, Brain, GitPullRequestArrow, ShieldCheck] as const;

const statusTone: Record<string, "green" | "gold" | "red" | "muted"> = {
  已验证: "green",
  已证伪: "red",
  部分验证: "gold",
  待验证: "gold",
  数据不足: "muted",
  已沉淀: "green",
  时效性记忆: "gold",
  待清理: "red",
  未入记忆: "muted",
  规则候选: "gold",
  优质规则: "green",
  次优规则: "gold",
  观察中: "muted",
  无: "muted",
  证据完整: "green",
  缺证据: "red",
  待人审: "gold",
  审计包: "green",
  已复核: "green",
  待复核: "gold",
  候选: "gold",
  观察: "muted"
};

function compactNumber(value: number) {
  return value.toLocaleString("zh-CN");
}

function toneClass(tone: string) {
  return `history-status history-status--${statusTone[tone] ?? "muted"}`;
}

export function HistoryKpiStrip({ kpis }: { kpis: HistoryKpi[] }) {
  return (
    <section className="holdings-kpi-strip history-kpi-strip" aria-label="时空回溯概览">
      {kpis.map((kpi) => (
        <article className={`kpi-card history-kpi-card history-kpi-card--${kpi.tone}`} key={kpi.label}>
          <span>{kpi.label}</span>
          <strong>{kpi.value}</strong>
          <small>{kpi.note}</small>
          <em>{kpi.delta}</em>
          <i className="history-kpi-spark" aria-hidden="true" />
        </article>
      ))}
    </section>
  );
}

export function LearningPipelinePanel({ data }: { data: HistoryPageData }) {
  return (
    <section className="history-learning panel-shell" aria-label="学习流水线">
      <div className="panel-title">
        <span>学习流水线 / 历史成长轨迹</span>
        <small>报告到规则的沉淀链路</small>
      </div>
      <div className="history-learning__grid">
        <div className="history-pipeline" aria-label="历史成长轨迹">
          {data.learningPipeline.map((node, index) => (
            <PipelineNode key={node.nodeId} node={node} index={index} />
          ))}
        </div>
        <aside className="history-monthly" aria-label="本月统计">
          <strong>本月统计</strong>
          <dl>
            <div>
              <dt>本月新增</dt>
              <dd>{compactNumber(data.monthlyStats.newItems)}</dd>
            </div>
            <div>
              <dt>已验证</dt>
              <dd className="is-positive">{compactNumber(data.monthlyStats.verified)}</dd>
            </div>
            <div>
              <dt>已证伪</dt>
              <dd className="is-negative">{compactNumber(data.monthlyStats.falsified)}</dd>
            </div>
            <div>
              <dt>已沉淀</dt>
              <dd className="is-positive">{compactNumber(data.monthlyStats.crystallized)}</dd>
            </div>
            <div>
              <dt>可晋级</dt>
              <dd>{compactNumber(data.monthlyStats.promotable)}</dd>
            </div>
          </dl>
        </aside>
      </div>
    </section>
  );
}

function PipelineNode({ node, index }: { node: LearningPipelineNode; index: number }) {
  const Icon = pipelineIcons[index] ?? Sparkles;
  return (
    <article className={`history-pipeline-node history-pipeline-node--${node.status.toLowerCase()}`}>
      <span className="history-pipeline-node__icon">
        <Icon size={28} aria-hidden="true" />
      </span>
      <strong>{node.displayName}</strong>
      <em>{compactNumber(node.count)}</em>
      <small>+{compactNumber(node.monthlyDelta)}</small>
    </article>
  );
}

export function HistoryEventTimeline({ events, onAction }: { events: HistoryEvent[]; onAction: ActionHandler }) {
  return (
    <section className="history-events panel-shell" aria-label="历史事件流">
      <div className="panel-title">
        <span>历史事件流 / 复盘时间轴</span>
        <small>可信历史 · 证据链留痕</small>
      </div>
      <div className="history-event-table" role="table" aria-label="历史事件流 / 复盘时间轴">
        <div role="row" className="history-event-row history-event-row--head">
          <span role="columnheader">日期</span>
          <span role="columnheader">对象</span>
          <span role="columnheader">类型</span>
          <span role="columnheader">结论</span>
          <span role="columnheader">验证状态</span>
          <span role="columnheader">记忆状态</span>
          <span role="columnheader">规则状态</span>
          <span role="columnheader">证据链</span>
          <span role="columnheader">操作</span>
        </div>
        {events.length > 0 ? (
          events.map((event) => (
            <button
              type="button"
              role="row"
              className="history-event-row history-event-row--button"
              key={event.eventId}
              onClick={() => onAction("查看详情", { eventId: event.eventId, targetId: event.targetCode })}
            >
              <span role="cell">{event.date}</span>
              <span role="cell">
                <strong>{event.targetName}</strong>
                <small>{event.targetCode}</small>
              </span>
              <span role="cell">{event.eventType}</span>
              <span role="cell">{event.conclusion}</span>
              <span role="cell">
                <em className={toneClass(event.outcomeStatus)}>{event.outcomeStatus}</em>
              </span>
              <span role="cell">
                <em className={toneClass(event.memoryStatus)}>{event.memoryStatus}</em>
              </span>
              <span role="cell">
                <em className={toneClass(event.ruleStatus)}>{event.ruleStatus}</em>
              </span>
              <span role="cell">
                <em className={toneClass(event.evidenceStatus)}>{event.evidenceStatus}</em>
              </span>
              <span role="cell">
                <b>查看</b>
              </span>
            </button>
          ))
        ) : (
          <div role="row" className="history-event-row history-event-row--empty">
            <span role="cell">等待历史资产索引导入</span>
          </div>
        )}
      </div>
    </section>
  );
}

export function HistoryLibraryCards({
  reports,
  cases,
  data,
  onAction
}: {
  reports: HistoryLibraryItem[];
  cases: HistoryLibraryItem[];
  data: HistoryPageData;
  onAction: ActionHandler;
}) {
  return (
    <section className="history-library-grid" aria-label="历史三库汇总">
      <HistoryLibraryCard
        title="分析报告库"
        subtitle="最近 3 条"
        icon={NotebookText}
        items={reports}
        actionLabel="查看全部报告"
        onAction={() => onAction("查看全部报告", { targetId: "REPORT_LIBRARY" })}
      />
      <HistoryLibraryCard
        title="实盘案例库"
        subtitle="只读复盘"
        icon={Archive}
        items={cases}
        actionLabel="查看全部案例"
        onAction={() => onAction("查看详情", { targetId: "CASE_LIBRARY" })}
      />
      <article className="history-library-card panel-shell" aria-label="系统记忆 / 规则候选">
        <div className="history-library-card__title">
          <div>
            <Brain size={18} aria-hidden="true" />
            <strong>系统记忆 / 规则候选</strong>
          </div>
          <small>沉淀与晋级</small>
        </div>
        <div className="memory-rule-grid">
          <div>
            <strong>系统记忆</strong>
            {data.memoryRuleSummary.memories.map((item) => (
              <span key={item.label}>
                {item.label}
                <em>{compactNumber(item.count)}</em>
              </span>
            ))}
          </div>
          <div>
            <strong>规则候选</strong>
            {data.memoryRuleSummary.rules.map((item) => (
              <span key={item.label}>
                {item.label}
                <em>{compactNumber(item.count)}</em>
              </span>
            ))}
          </div>
        </div>
        <button type="button" onClick={() => onAction("生成规则候选草案", { targetId: "RULE_CANDIDATE_SUMMARY" })}>
          查看沉淀详情
        </button>
      </article>
    </section>
  );
}

function HistoryLibraryCard({
  title,
  subtitle,
  icon: Icon,
  items,
  actionLabel,
  onAction
}: {
  title: string;
  subtitle: string;
  icon: typeof FileText;
  items: HistoryLibraryItem[];
  actionLabel: string;
  onAction: () => void;
}) {
  return (
    <article className="history-library-card panel-shell" aria-label={title}>
      <div className="history-library-card__title">
        <div>
          <Icon size={18} aria-hidden="true" />
          <strong>{title}</strong>
        </div>
        <small>{subtitle}</small>
      </div>
      <ul>
        {items.length > 0 ? (
          items.map((item) => (
            <li key={item.itemId}>
              <time>{item.date}</time>
              <span>{item.title}</span>
              <em className={toneClass(item.status)}>{item.status}</em>
            </li>
          ))
        ) : (
          <li>
            <time>--</time>
            <span>等待索引导入</span>
            <em className="history-status history-status--muted">待处理</em>
          </li>
        )}
      </ul>
      <button type="button" onClick={onAction}>
        {actionLabel}
      </button>
    </article>
  );
}

export function HistoryEvidenceBand({ data }: { data: HistoryPageData }) {
  return (
    <section className="history-evidence-band" aria-label="审计证据链状态">
      <CheckCircle2 size={16} aria-hidden="true" />
      <span>证据链可追溯</span>
      <small>报告库 {data.systemStatus.reportIndex} · 审计包 {data.systemStatus.auditPack} · 研究库 {data.systemStatus.researchDb}</small>
      <ClipboardCheck size={16} aria-hidden="true" />
    </section>
  );
}
