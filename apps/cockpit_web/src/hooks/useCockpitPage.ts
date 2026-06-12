import { useQuery } from "@tanstack/react-query";
import type { AuthSession } from "../auth";
import type { CockpitRouteId } from "../data/cockpit";
import { getCockpitPagePacket } from "../services/mockApi";

export function useCockpitPage(session: AuthSession, pageId: CockpitRouteId) {
  return useQuery({
    queryKey: ["cockpit-page", session.workspaceId, pageId],
    queryFn: () => getCockpitPagePacket(session, pageId)
  });
}
