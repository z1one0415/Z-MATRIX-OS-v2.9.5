import { Routes, Route } from 'react-router-dom';
import { MainLayout } from './layout';
import { HomeDashboard } from '../pages/HomeDashboard';
import { CapabilityInvocationOS } from '../pages/CapabilityInvocationOS';
import { FactorLibrary } from '../pages/FactorLibrary';
import { CompositionGraph } from '../pages/CompositionGraph';
import { ResearchReportNode } from '../pages/ResearchReportNode';
import { Z9ReviewNode } from '../pages/Z9ReviewNode';
import { EvidenceChain } from '../pages/EvidenceChain';
import { RunStateRegistry } from '../pages/RunStateRegistry';
import { GateStateRegistry } from '../pages/GateStateRegistry';
import { AuditTrail } from '../pages/AuditTrail';
import { SafetyBoundary } from '../pages/SafetyBoundary';

export function AppRouter() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        {/* Overview */}
        <Route index element={<HomeDashboard />} />

        {/* Capabilities */}
        <Route path="capabilities" element={<CapabilityInvocationOS />} />
        <Route path="factor-library" element={<FactorLibrary />} />
        <Route path="composition-graph" element={<CompositionGraph />} />

        {/* Research & Review */}
        <Route path="research-report" element={<ResearchReportNode />} />
        <Route path="z9-review" element={<Z9ReviewNode />} />

        {/* Evidence & State */}
        <Route path="evidence-chain" element={<EvidenceChain />} />
        <Route path="run-state" element={<RunStateRegistry />} />
        <Route path="gate-state" element={<GateStateRegistry />} />
        <Route path="audit-trail" element={<AuditTrail />} />

        {/* System */}
        <Route path="settings" element={<SafetyBoundary />} />

        {/* Catch-all */}
        <Route path="*" element={<HomeDashboard />} />
      </Route>
    </Routes>
  );
}
