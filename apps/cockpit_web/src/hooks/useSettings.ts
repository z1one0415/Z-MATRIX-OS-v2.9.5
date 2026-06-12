import { useMutation, useQuery } from "@tanstack/react-query";
import type { AuthSession } from "../auth";
import { createSettingsActionDraft, getSettingsPageData } from "../services/settingsApi";
import type { SettingsAction } from "../services/settingsApi";

export function useSettings(session: AuthSession) {
  return useQuery({
    queryKey: ["settings", session.workspaceId],
    queryFn: () => getSettingsPageData(session)
  });
}

export function useSettingsAction(session: AuthSession) {
  return useMutation({
    mutationFn: ({ action, payload }: { action: SettingsAction; payload?: Record<string, unknown> }) =>
      createSettingsActionDraft(session, action, payload ?? {})
  });
}
