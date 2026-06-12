import { useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import type { AuthSession } from "./auth";
import { demoSession } from "./auth";
import { AppShell } from "./components/AppShell";
import { LoginGate } from "./components/LoginGate";
import { ControlCompassPage } from "./pages/ControlCompassPage";
import { DayanAskPage } from "./pages/DayanAskPage";
import { HistoryPage } from "./pages/HistoryPage";
import { HoldingsPage } from "./pages/HoldingsPage";
import { SelectionPage } from "./pages/SelectionPage";
import { SettingsPage } from "./pages/SettingsPage";
import { WorkbenchPage } from "./pages/WorkbenchPage";
import { CockpitPreferencesProvider } from "./settings/CockpitPreferences";

export function App() {
  const [session, setSession] = useState<AuthSession | null>(demoSession);

  if (!session) {
    return (
      <CockpitPreferencesProvider>
        <LoginGate onLogin={setSession} />
      </CockpitPreferencesProvider>
    );
  }

  return (
    <CockpitPreferencesProvider>
      <Routes>
        <Route element={<AppShell session={session} />}>
          <Route index element={<Navigate to="/holdings" replace />} />
          <Route path="/holdings" element={<HoldingsPage session={session} />} />
          <Route path="/selection" element={<SelectionPage session={session} />} />
          <Route path="/dayan-ask" element={<DayanAskPage session={session} />} />
          <Route path="/control-compass" element={<ControlCompassPage session={session} />} />
          <Route path="/history" element={<HistoryPage session={session} />} />
          <Route path="/settings" element={<SettingsPage session={session} />} />
          <Route path="/operator-profile" element={<WorkbenchPage session={session} pageId="profile" />} />
          <Route path="*" element={<Navigate to="/holdings" replace />} />
        </Route>
      </Routes>
    </CockpitPreferencesProvider>
  );
}
