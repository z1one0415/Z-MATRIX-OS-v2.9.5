import { Bot, ChevronRight, MessageSquareText } from "lucide-react";
import type { HermesAdvisoryPacket } from "../../services/hermesAdvisoryApi";

type HermesAdvisoryPanelProps = {
  packet: HermesAdvisoryPacket;
  onOpenChat: (question?: string) => void;
};

export function HermesAdvisoryPanel({ packet, onOpenChat }: HermesAdvisoryPanelProps) {
  return (
    <section className="rail-panel hermes-advisory-panel" aria-label="童子谏言">
      <div className="hermes-rail-head">
        <div className="hermes-rail-avatar" aria-hidden="true">
          <Bot size={18} />
          <span />
        </div>
        <div>
          <strong>童子谏言</strong>
          <small>{packet.status} · {packet.riskPosture}</small>
        </div>
      </div>

      <p className="hermes-rail-summary">{packet.contextSummary}</p>

      <div className="hermes-rail-meta" aria-label="童子谏言待补信息">
        {packet.missingInputs.slice(0, 3).map((item) => (
          <span key={item}>{item}</span>
        ))}
      </div>

      <button className="hermes-ask-button" type="button" onClick={() => onOpenChat()}>
        <MessageSquareText size={16} aria-hidden="true" />
        问童子
        <ChevronRight size={15} aria-hidden="true" />
      </button>
    </section>
  );
}
