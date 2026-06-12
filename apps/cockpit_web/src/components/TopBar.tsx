import { Bell, Mail, Settings } from "lucide-react";

export function TopBar() {
  return (
    <header className="top-bar">
      <div className="top-actions" aria-label="全局工具">
        <button type="button" aria-label="提示" title="提示">
          <Bell size={18} />
          <span className="tool-tooltip">提示</span>
        </button>
        <button type="button" aria-label="信息" title="信息">
          <Mail size={18} />
          <span className="tool-tooltip">信息</span>
        </button>
        <button type="button" aria-label="设置" title="设置">
          <Settings size={18} />
          <span className="tool-tooltip">设置</span>
        </button>
      </div>
      <div className="clock-block" aria-label="系统时间">
        <strong>09:42:31</strong>
        <small>数据更新 09:35 · 2025-05-16</small>
      </div>
    </header>
  );
}
