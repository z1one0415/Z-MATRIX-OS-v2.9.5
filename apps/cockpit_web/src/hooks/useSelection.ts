import { useMutation, useQuery } from "@tanstack/react-query";
import type { AuthSession } from "../auth";
import { createSelectionActionDraft, getSelectionDashboardPacket } from "../services/selectionApi";
import type { SelectionActionDraft } from "../services/selectionApi";

export function useSelection(session: AuthSession) {
  return useQuery({
    queryKey: ["selection", session.workspaceId],
    queryFn: () => getSelectionDashboardPacket(session)
  });
}

export function useSelectionAction(session: AuthSession) {
  return useMutation({
    mutationFn: ({
      action,
      payload
    }: {
      action: SelectionActionDraft["action"];
      payload: Record<string, unknown>;
    }) => createSelectionActionDraft(session, action, payload)
  });
}
