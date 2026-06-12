import { useMutation, useQuery } from "@tanstack/react-query";
import type { AuthSession } from "../auth";
import { createControlCompassActionDraft, getControlCompassPageData } from "../services/controlCompassApi";
import type { ControlCompassActionDraft } from "../services/controlCompassApi";

export function useControlCompass(session: AuthSession) {
  return useQuery({
    queryKey: ["control-compass", session.workspaceId],
    queryFn: () => getControlCompassPageData(session)
  });
}

export function useControlCompassAction(session: AuthSession) {
  return useMutation({
    mutationFn: ({
      action,
      payload
    }: {
      action: ControlCompassActionDraft["action"];
      payload: Record<string, unknown>;
    }) => createControlCompassActionDraft(session, action, payload)
  });
}
