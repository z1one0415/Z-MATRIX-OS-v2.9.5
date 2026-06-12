import { useMutation, useQuery } from "@tanstack/react-query";
import type { AuthSession } from "../auth";
import {
  createHermesActionDraft,
  createHermesChatResponse,
  getHermesAdvisoryPacket
} from "../services/hermesAdvisoryApi";
import type { HermesActionRequest, HermesChatRequest, HermesPageId } from "../services/hermesAdvisoryApi";

export function useHermesAdvisory(session: AuthSession, pageId: HermesPageId) {
  return useQuery({
    queryKey: ["hermes-advisory", session.workspaceId, pageId],
    queryFn: () => getHermesAdvisoryPacket(session, pageId)
  });
}

export function useHermesChat(session: AuthSession) {
  return useMutation({
    mutationFn: (request: HermesChatRequest) => createHermesChatResponse(session, request)
  });
}

export function useHermesActionDraft(session: AuthSession) {
  return useMutation({
    mutationFn: (request: HermesActionRequest) => createHermesActionDraft(session, request)
  });
}
