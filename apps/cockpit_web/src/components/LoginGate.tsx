import { FormEvent, useState } from "react";
import { LockKeyhole, ShieldCheck } from "lucide-react";
import type { AuthSession } from "../auth";
import { createDemoSession } from "../auth";
import { StatusPill } from "./StatusPill";

type LoginGateProps = {
  onLogin: (session: AuthSession) => void;
};

export function LoginGate({ onLogin }: LoginGateProps) {
  const [email, setEmail] = useState("z-prime@example.com");

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onLogin(createDemoSession(email));
  }

  return (
    <main className="login-shell">
      <section className="login-card" aria-labelledby="login-title">
        <div className="login-brand">
          <span className="brand-mark">Z</span>
          <span>
            <strong>Z-MATRIX</strong>
            <small>Research Cockpit</small>
          </span>
        </div>
        <div className="login-copy">
          <h1 id="login-title">进入研究驾驶舱</h1>
          <p>单实例托管 · 独立 Workspace · 行级隔离</p>
        </div>
        <div className="login-locks">
          <StatusPill icon={ShieldCheck} label="Paper-only" />
          <StatusPill icon={LockKeyhole} label="Broker Blocked" tone="red" />
        </div>
        <form onSubmit={submit} className="login-form">
          <label htmlFor="email">邮箱</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.currentTarget.value)}
            autoComplete="email"
          />
          <label htmlFor="password">密码</label>
          <input id="password" type="password" value="paper-only-demo" readOnly />
          <button type="submit">登录驾驶舱</button>
        </form>
      </section>
    </main>
  );
}
