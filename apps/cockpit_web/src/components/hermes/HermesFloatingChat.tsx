import { Bot, ChevronRight, Minus, Send, Sparkles, Trash2, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { AuthSession } from "../../auth";
import { useHermesAdvisory, useHermesChat } from "../../hooks/useHermesAdvisory";
import type { HermesPageId } from "../../services/hermesAdvisoryApi";

type HermesFloatingChatProps = {
  session: AuthSession;
  pageId: HermesPageId;
  isOpen: boolean;
  initialQuestion?: string;
  onClose: () => void;
};

type ChatMessage = {
  id: string;
  role: "USER" | "HERMES";
  label: "你" | "童子";
  content: string;
  createdAt: string;
};

function nowLabel() {
  return "09:42";
}

export function HermesFloatingChat({ session, pageId, isOpen, initialQuestion, onClose }: HermesFloatingChatProps) {
  const navigate = useNavigate();
  const { data: packet } = useHermesAdvisory(session, pageId);
  const chat = useHermesChat(session);
  const [isMinimized, setIsMinimized] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const listRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    if (!isOpen) return;
    setIsMinimized(false);
    if (initialQuestion) {
      setInput(initialQuestion);
    }
    window.requestAnimationFrame(() => inputRef.current?.focus());
  }, [initialQuestion, isOpen]);

  useEffect(() => {
    const list = listRef.current;
    if (!list) return;

    const frame = window.requestAnimationFrame(() => {
      list.scrollTop = list.scrollHeight;
    });

    return () => window.cancelAnimationFrame(frame);
  }, [messages.length, chat.isPending, isOpen, isMinimized]);

  if (!isOpen) return null;

  const promptSeeds = packet?.promptSeeds ?? [];
  const contextSummary = packet?.contextSummary ?? "童子正在读取当前页面上下文。";
  const pageSnapshot = packet?.pageContext.pageSnapshot;

  async function sendQuestion(questionOverride?: string) {
    const question = (questionOverride ?? input).trim();
    if (!question || !packet) return;
    const createdAt = nowLabel();

    setMessages((current) => [
      ...current,
      {
        id: `hermes-user-${Date.now()}`,
        role: "USER",
        label: "你",
        content: question,
        createdAt
      }
    ]);
    setInput("");

    try {
      const response = await chat.mutateAsync({
        pageId,
        question,
        pageSnapshot
      });
      setMessages((current) => [
        ...current,
        {
          id: response.responseId,
          role: "HERMES",
          label: "童子",
          content: response.answer,
          createdAt
        }
      ]);
    } catch {
      setMessages((current) => [
        ...current,
        {
          id: `hermes-error-${Date.now()}`,
          role: "HERMES",
          label: "童子",
          content: "当前问答草案未能生成，请稍后再试；安全锁保持开启。",
          createdAt
        }
      ]);
    }
  }

  if (isMinimized) {
    return (
      <button className="hermes-chat-minibar" type="button" onClick={() => setIsMinimized(false)}>
        <Bot size={17} aria-hidden="true" />
        童子谏言
        <ChevronRight size={15} aria-hidden="true" />
      </button>
    );
  }

  return (
    <aside className="hermes-floating-chat" aria-label="童子谏言悬浮问答">
      <div className="hermes-chat-head">
        <div>
          <span>
            <Bot size={17} aria-hidden="true" />
            童子谏言
          </span>
          <small>当前页答疑 · 草案先行 · 人审裁定</small>
        </div>
        <div className="hermes-chat-head-actions">
          <button type="button" aria-label="最小化童子谏言" onClick={() => setIsMinimized(true)}>
            <Minus size={16} aria-hidden="true" />
          </button>
          <button type="button" aria-label="关闭童子谏言" onClick={onClose}>
            <X size={16} aria-hidden="true" />
          </button>
        </div>
      </div>

      <div className="hermes-chat-context">
        <Sparkles size={15} aria-hidden="true" />
        <p>{contextSummary}</p>
      </div>

      <div className="hermes-chat-suggestions" aria-label="本页互动提示">
        {promptSeeds.slice(0, 4).map((question) => (
          <button type="button" key={question} onClick={() => void sendQuestion(question)}>
            {question}
          </button>
        ))}
      </div>

      <div className="hermes-chat-messages" ref={listRef}>
        {messages.length === 0 ? (
          <p className="hermes-chat-empty">可以直接提问，也可以点上方问题让童子先起一段。</p>
        ) : null}
        {messages.map((message) => (
          <article className={`hermes-chat-message hermes-chat-message--${message.role.toLowerCase()}`} key={message.id}>
            <strong>{message.label}</strong>
            <p>{message.content}</p>
            <small>{message.createdAt}</small>
          </article>
        ))}
        {chat.isPending ? <p className="hermes-chat-empty">童子正在生成待确认答复...</p> : null}
      </div>

      <div className="hermes-chat-footer">
        <button
          type="button"
          aria-label="清空童子谏言对话"
          onClick={() => {
            setMessages([]);
            setInput("");
          }}
        >
          <Trash2 size={16} aria-hidden="true" />
        </button>
        <textarea
          ref={inputRef}
          aria-label="问童子输入"
          value={input}
          placeholder="问童子当前页的问题，回车发送"
          rows={1}
          onChange={(event) => setInput(event.currentTarget.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              void sendQuestion();
            }
          }}
        />
        <button type="button" aria-label="发送给童子" onClick={() => void sendQuestion()}>
          <Send size={17} aria-hidden="true" />
        </button>
      </div>

      {pageId !== "dayan" ? (
        <button
          className="hermes-chat-handoff"
          type="button"
          onClick={() => navigate("/dayan-ask", { state: { from: pageId, question: input || promptSeeds[0] } })}
        >
          转入大衍天问
          <ChevronRight size={15} aria-hidden="true" />
        </button>
      ) : null}
    </aside>
  );
}
