export type AuthSession = {
  userId: string;
  email: string;
  displayName: string;
  workspaceId: string;
  workspaceName: string;
  role: "OWNER";
};

export const demoSession: AuthSession = {
  userId: "usr_z_prime",
  email: "z-prime@example.com",
  displayName: "Z-Prime",
  workspaceId: "ws_personal_z_prime",
  workspaceName: "Z-Prime Personal Workspace",
  role: "OWNER"
};

export function createDemoSession(email: string): AuthSession {
  const safeEmail = email.trim().toLowerCase() || demoSession.email;
  const name = safeEmail.split("@", 1)[0] || demoSession.displayName;
  return {
    ...demoSession,
    email: safeEmail,
    displayName: name === "z-prime" ? "Z-Prime" : name,
    userId: `usr_${name.replace(/[^a-z0-9]/gi, "_")}`,
    workspaceId: `ws_${name.replace(/[^a-z0-9]/gi, "_")}_personal`
  };
}
