import { Outlet, useLocation } from "react-router-dom";
import { useState } from "react";
import type { AuthSession } from "../auth";
import { BottomTicker } from "./BottomTicker";
import { HermesFloatingChat } from "./hermes/HermesFloatingChat";
import { RightRail } from "./RightRail";
import type { RightRailVariant } from "./RightRail";
import { SideNav } from "./SideNav";
import { TopBar } from "./TopBar";

type AppShellProps = {
  session: AuthSession;
};

export function AppShell({ session }: AppShellProps) {
  const location = useLocation();
  const isDayanCanvas = location.pathname === "/dayan-ask";
  const isSettingsPage = location.pathname === "/settings";
  const usesCustomRail = isDayanCanvas || isSettingsPage;
  const [hermesChat, setHermesChat] = useState<{
    isOpen: boolean;
    pageId: RightRailVariant;
    question?: string;
  }>({ isOpen: false, pageId: "holdings" });
  const rightRailVariant: RightRailVariant =
    location.pathname === "/selection"
      ? "selection"
      : location.pathname === "/control-compass"
        ? "compass"
        : location.pathname === "/history"
          ? "history"
          : location.pathname === "/settings"
            ? "settings"
            : location.pathname === "/operator-profile"
              ? "profile"
              : "holdings";

  function openHermesChat(pageId: RightRailVariant, question?: string) {
    setHermesChat({
      isOpen: true,
      pageId,
      question
    });
  }

  return (
    <div className="cockpit-shell">
      <SideNav session={session} />
      <div className="cockpit-frame">
        {isSettingsPage ? null : <TopBar />}
        <div className={`cockpit-body${usesCustomRail ? " cockpit-body--full" : ""}`}>
          <Outlet context={{ openHermesChat }} />
          {usesCustomRail ? null : <RightRail variant={rightRailVariant} session={session} onOpenHermesChat={openHermesChat} />}
        </div>
        {!isDayanCanvas ? (
          <HermesFloatingChat
            session={session}
            pageId={hermesChat.pageId}
            isOpen={hermesChat.isOpen}
            initialQuestion={hermesChat.question}
            onClose={() => setHermesChat((current) => ({ ...current, isOpen: false }))}
          />
        ) : null}
        <BottomTicker />
      </div>
    </div>
  );
}
