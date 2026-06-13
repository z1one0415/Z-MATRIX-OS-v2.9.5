import { ClipboardCheck, FileText, Mic, NotebookPen, ShieldCheck, UserRoundCog, Landmark } from "lucide-react";
import { useMemo, useState } from "react";
import type { AuthSession } from "../auth";
import {
  AskAltarPanel,
  AskDuelChat,
  AskFormationPanel,
  AskSkillDrawer,
  AskSkillPanel,
  DayanSystemLine,
  HeavenlyAdvisoryPanel,
  HermesGuidancePanel,
  MethodForgePanel,
  MoveReviewPanel,
  MyMethodsPanel
} from "../components/dayan-ask/DayanAskPanels";
import { StatusPill } from "../components/StatusPill";
import { useDayanAction, useDayanAsk } from "../hooks/useDayanAsk";
import type { AskFormation, AskMessage, AskSkill, AskSkillCategory, DayanAction } from "../services/dayanAskApi";
import { useCockpitPreferences } from "../settings/CockpitPreferences";

type DayanAskPageProps = {
  session: AuthSession;
};

const safetyStates = [
  { label: "仅纸面", tooltip: "仅纸面研究", tone: "gold" as const, icon: ShieldCheck },
  { label: "人审", tooltip: "人审裁定", tone: "gold" as const, icon: UserRoundCog },
  { label: "券商阻断", tooltip: "券商通道已阻断", tone: "red" as const, icon: Landmark }
];

function hasSpeechRecognition() {
  if (typeof window === "undefined") return false;
  return "SpeechRecognition" in window || "webkitSpeechRecognition" in window;
}

export function DayanAskPage({ session }: DayanAskPageProps) {
  const { data, isLoading, isError } = useDayanAsk(session);
  const action = useDayanAction(session);
  const { copy } = useCockpitPreferences();
  const [drawerCategory, setDrawerCategory] = useState<AskSkillCategory | null>(null);
  const [inputText, setInputText] = useState("");
  const [selectedFragments, setSelectedFragments] = useState<string[]>([]);
  const [localMessages, setLocalMessages] = useState<AskMessage[]>([]);

  const voiceAvailable = useMemo(() => hasSpeechRecognition(), []);

  if (isLoading || !data) {
    return <main className="dayan-page">加载大衍天问数据</main>;
  }

  if (isError) {
    return <main className="dayan-page">当前大衍天问视图暂不可用</main>;
  }

  const pageData = data;
  const messages = [...pageData.currentConversation.messages, ...localMessages];
  const fragments = selectedFragments.length > 0 ? selectedFragments : pageData.currentConversation.selectedPromptFragments;

  function submitAction(actionName: DayanAction, payload: Record<string, unknown> = {}) {
    action.mutate({
      action: actionName,
      payload: {
        source: "dayan-ask-page",
        ...payload
      }
    });
  }

  function appendFragment(label: string, promptTemplate: string, payload: Record<string, unknown>) {
    setSelectedFragments((current) => Array.from(new Set([...current, label])));
    setInputText((current) => (current.trim() ? `${current.trim()}\n${promptTemplate}` : promptTemplate));
    submitAction("插入法门", payload);
  }

  function insertFormation(formation: AskFormation) {
    appendFragment(formation.name, formation.promptTemplate, { formationId: formation.id });
  }

  function insertSkill(skill: AskSkill) {
    appendFragment(skill.userVisibleName, skill.promptTemplate, { skillId: skill.id });
    setDrawerCategory(null);
  }

  function sendMessage() {
    const trimmed = inputText.trim();
    if (!trimmed) return;
    const now = "09:42";
    setLocalMessages((current) => [
      ...current,
      {
        id: `local-user-${Date.now()}`,
        role: "USER",
        label: "你",
        content: trimmed,
        createdAt: now
      },
      {
        id: `local-hermes-${Date.now()}`,
        role: "HERMES",
        label: "问天",
        content: "随侍童子已生成研究链路草案：先补齐输入约束，再调用已选法门，最后把结果送入落子复盘等待人审裁定。",
        createdAt: now
      }
    ]);
    submitAction("生成链路草案", {
      userInput: trimmed,
      selectedFragments: fragments
    });
    setInputText("");
  }

  function clearConversation() {
    setLocalMessages([]);
    setInputText("");
    setSelectedFragments([]);
    submitAction("清空对话", { conversationId: pageData.currentConversation.conversationId });
  }

  function handleVoiceClick() {
    submitAction("插入法门", {
      sourceControl: "voice",
      voiceAvailable
    });
    if (!voiceAvailable) {
      setInputText((current) => current || "当前浏览器未开放语音输入，请直接输入研究目标。");
    }
  }

  return (
    <main className="dayan-page" aria-labelledby="dayan-title">
      <section className="dayan-heading">
        <div className="heading-copy">
          <div className="heading-title-line">
            <h1 id="dayan-title">{copy("copy.dayan", "大衍天问")}</h1>
          </div>
          <p>问天问策 · 推演未来 · 知行合一</p>
        </div>
        <div className="dayan-heading-tools" aria-label="大衍天问页眉工具">
          <div className="dayan-status-icons" aria-label="全局安全状态">
            {safetyStates.map((state) => (
              <StatusPill
                key={state.label}
                compact
                icon={state.icon}
                label={state.label}
                tone={state.tone}
                tooltip={state.tooltip}
              />
            ))}
          </div>
          <span className="dayan-tool-separator" aria-hidden="true" />
          <div className="dayan-action-icons" aria-label="大衍天问动作">
            <button type="button" aria-label="生成链路草案" title="生成链路草案" onClick={() => sendMessage()}>
              <FileText size={19} aria-hidden="true" />
              <span className="tool-tooltip">生成链路草案</span>
            </button>
            <button type="button" aria-label="保存我的法门草案" title="保存我的法门草案" onClick={() => submitAction("保存我的法门草案", { fragments })}>
              <NotebookPen size={19} aria-hidden="true" />
              <span className="tool-tooltip">保存我的法门草案</span>
            </button>
            <button type="button" aria-label="语音输入" title={voiceAvailable ? "语音输入" : "当前浏览器未开放语音输入"} onClick={handleVoiceClick}>
              <Mic size={19} aria-hidden="true" />
              <span className="tool-tooltip">{voiceAvailable ? "语音输入" : "语音输入不可用"}</span>
            </button>
            <button type="button" aria-label="导出审计包" title="导出审计包" onClick={() => submitAction("导出审计包", { conversationId: pageData.currentConversation.conversationId })}>
              <ClipboardCheck size={19} aria-hidden="true" />
              <span className="tool-tooltip">导出审计包</span>
            </button>
          </div>
        </div>
      </section>

      <DayanSystemLine data={pageData} />

      <section className="dayan-nine-grid" aria-label="大衍天问九宫控制台">
        <AskAltarPanel data={pageData} />
        <AskFormationPanel formations={pageData.formations} onInsert={insertFormation} />
        <HermesGuidancePanel guidance={pageData.hermesGuidance} />
        <AskSkillPanel categories={pageData.skillCategories} onOpenCategory={setDrawerCategory} />
        <AskDuelChat
          topic={pageData.currentConversation.topic}
          messages={messages}
          fragments={fragments}
          inputValue={inputText}
          voiceAvailable={voiceAvailable}
          draftMessage={action.data?.answer ?? action.data?.userMessage}
          onInputChange={setInputText}
          onSend={sendMessage}
          onClear={clearConversation}
          onVoiceClick={handleVoiceClick}
        />
        <HeavenlyAdvisoryPanel groups={pageData.advisoryGroups} />
        <MyMethodsPanel methods={pageData.myMethods} />
        <MoveReviewPanel items={pageData.moveReview} />
        <MethodForgePanel candidates={pageData.forgeCandidates} onAction={submitAction} />
      </section>

      <AskSkillDrawer category={drawerCategory} onClose={() => setDrawerCategory(null)} onInsert={insertSkill} />
    </main>
  );
}
