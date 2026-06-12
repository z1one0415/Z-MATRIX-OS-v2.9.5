import { useMutation, useQuery } from "@tanstack/react-query";
import type { AuthSession } from "../auth";
import { createDayanActionDraft, getDayanAskPageData } from "../services/dayanAskApi";
import type { DayanAction } from "../services/dayanAskApi";

export function useDayanAsk(session: AuthSession) {
  return useQuery({
    queryKey: ["dayan-ask", session.workspaceId],
    queryFn: () => getDayanAskPageData(session)
  });
}

export function useDayanAction(session: AuthSession) {
  return useMutation({
    mutationFn: ({ action, payload }: { action: DayanAction; payload: Record<string, unknown> }) =>
      createDayanActionDraft(session, action, payload)
  });
}
