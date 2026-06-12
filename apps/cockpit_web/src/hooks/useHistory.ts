import { useMutation, useQuery } from "@tanstack/react-query";
import type { AuthSession } from "../auth";
import { createHistoryActionDraft, getHistoryPageData } from "../services/historyApi";
import type { HistoryActionDraft } from "../services/historyApi";

export function useHistory(session: AuthSession) {
  return useQuery({
    queryKey: ["history", session.workspaceId],
    queryFn: () => getHistoryPageData(session)
  });
}

export function useHistoryAction(session: AuthSession) {
  return useMutation({
    mutationFn: ({
      action,
      payload
    }: {
      action: HistoryActionDraft["action"];
      payload: Record<string, unknown>;
    }) => createHistoryActionDraft(session, action, payload)
  });
}
