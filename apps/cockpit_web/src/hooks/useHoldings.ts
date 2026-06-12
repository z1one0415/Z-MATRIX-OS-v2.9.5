import { useMutation, useQuery } from "@tanstack/react-query";
import type { AuthSession } from "../auth";
import { createHoldingActionDraft, getHoldingsPacket } from "../services/holdingsApi";
import type { HoldingReviewDraft } from "../services/holdingsApi";

export function useHoldings(session: AuthSession) {
  return useQuery({
    queryKey: ["holdings", session.workspaceId],
    queryFn: () => getHoldingsPacket(session)
  });
}

export function useHoldingAction(session: AuthSession) {
  return useMutation({
    mutationFn: ({
      action,
      payload
    }: {
      action: HoldingReviewDraft["action"];
      payload: Record<string, unknown>;
    }) => createHoldingActionDraft(session, action, payload)
  });
}
