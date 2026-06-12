import { ClipboardCheck, FileSearch, FileText, RotateCcw } from "lucide-react";
import { useMemo, useState } from "react";
import type { AuthSession } from "../auth";
import { StatusPill } from "../components/StatusPill";
import {
  CompassKpiStrip,
  DerivationRulingCard,
  DerivationSandboxPanel,
  SevenLayerCompassMap
} from "../components/control-compass/ControlCompassPanels";
import { securityStates } from "../data/cockpit";
import { useControlCompass, useControlCompassAction } from "../hooks/useControlCompass";
import type { ControlCompassActionDraft, GovernanceDomainId } from "../services/controlCompassApi";
import { useCockpitPreferences } from "../settings/CockpitPreferences";

type ControlCompassPageProps = {
  session: AuthSession;
};

const securityTooltips: Record<string, string> = {
  "Paper-only": "仅纸面校准，不触发生产变更",
  "Human Review": "参数草案必须人工复核",
  "Broker Blocked": "券商与实盘通道已阻断"
};

export function ControlCompassPage({ session }: ControlCompassPageProps) {
  const { data, isLoading, isError } = useControlCompass(session);
  const action = useControlCompassAction(session);
  const { copy } = useCockpitPreferences();
  const latestDraft = action.data;
  const [selectedDomainId, setSelectedDomainId] = useState<GovernanceDomainId>("CATALYST_CYCLE");

  const selectedDomain = useMemo(() => {
    if (!data?.governanceDomains.length) {
      return undefined;
    }
    return data.governanceDomains.find((domain) => domain.domainId === selectedDomainId) ?? data.governanceDomains[2] ?? data.governanceDomains[0];
  }, [data, selectedDomainId]);

  const selectedFamily = useMemo(() => {
    if (!data?.parameterFamilies.length || !selectedDomain) {
      return undefined;
    }
    return data.parameterFamilies.find((family) => family.domainId === selectedDomain.domainId) ?? data.parameterFamilies[0];
  }, [data, selectedDomain]);

  if (isLoading || !data) {
    return <main className="holdings-page control-compass-page">加载天机罗盘数据</main>;
  }

  if (isError || !selectedDomain) {
    return <main className="holdings-page control-compass-page">当前天机罗盘视图暂不可用</main>;
  }

  function submitAction(actionName: ControlCompassActionDraft["action"], payload: Record<string, unknown> = {}) {
    action.mutate({
      action: actionName,
      payload: {
        source: "control-compass-page",
        ...payload
      }
    });
  }

  return (
    <main className="holdings-page control-compass-page" aria-labelledby="control-compass-title">
      <section className="holdings-heading control-compass-heading">
        <div className="heading-copy">
          <div className="heading-title-line">
            <h1 id="control-compass-title">{copy("copy.compass", "天机罗盘")}</h1>
          </div>
          <p>量化参数 · 成功率复盘 · 快照保护</p>
          <div className="heading-status" aria-label="全局安全状态">
            {securityStates.map((state) => (
              <StatusPill
                key={state.label}
                compact
                icon={state.icon}
                label={state.label}
                tone={state.tone}
                tooltip={securityTooltips[state.label]}
              />
            ))}
          </div>
        </div>
        <div className="heading-control">
          <div className="heading-actions">
            <button
              type="button"
              className="button button--primary"
              aria-label="查看参数族详情"
              title="查看参数族详情"
              onClick={() => submitAction("查看参数族详情", { domainId: selectedDomain.domainId, familyId: selectedFamily?.familyId })}
            >
              <FileSearch size={18} aria-hidden="true" />
              <span className="button__label">查看参数族详情</span>
              <span className="tool-tooltip">查看参数族详情</span>
            </button>
            <button
              type="button"
              className="button"
              aria-label="创建校准草案"
              title="创建校准草案"
              onClick={() => submitAction("创建校准草案", { draftId: data.sandbox.draft.draftId, snapshotId: data.optimizationSummary.snapshotId })}
            >
              <FileText size={18} aria-hidden="true" />
              <span className="button__label">创建校准草案</span>
              <span className="tool-tooltip">创建校准草案</span>
            </button>
            <button
              type="button"
              className="button"
              aria-label="恢复系统自优化结果"
              title="恢复系统自优化结果"
              onClick={() => submitAction("恢复系统自优化结果", { draftId: data.ruling.draftId, snapshotId: data.optimizationSummary.snapshotId })}
            >
              <RotateCcw size={18} aria-hidden="true" />
              <span className="button__label">恢复系统建议</span>
              <span className="tool-tooltip">恢复系统自优化结果</span>
            </button>
            <button
              type="button"
              className="button button--ghost"
              aria-label="导出审计包"
              title="导出审计包"
              onClick={() => submitAction("导出审计包", { draftId: data.ruling.draftId })}
            >
              <ClipboardCheck size={18} aria-hidden="true" />
              <span className="button__label">导出审计包</span>
              <span className="tool-tooltip">导出审计包</span>
            </button>
          </div>
          <small className="heading-action-note" aria-live="polite">
            {latestDraft ? latestDraft.userMessage : "所有参数校准先备份自优化快照，再进入人审与审计。"}
          </small>
        </div>
      </section>

      <CompassKpiStrip data={data} />
      <section className="control-compass-main-grid" aria-label="天机罗盘主工作区">
        <SevenLayerCompassMap
          domains={data.governanceDomains}
          family={selectedFamily}
          selectedDomainId={selectedDomain.domainId}
          onSelect={(domain) => setSelectedDomainId(domain.domainId)}
          onAction={submitAction}
        />
      </section>
      <section className="control-compass-bottom-grid" aria-label="天机罗盘推衍与裁定">
        <DerivationSandboxPanel data={data} onAction={submitAction} />
        <DerivationRulingCard data={data} onAction={submitAction} />
      </section>
    </main>
  );
}
