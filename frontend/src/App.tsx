import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { CommandCenterPage } from './pages/CommandCenterPage';
import { OverviewPage } from './pages/OverviewPage';
import { AttackLabPage } from './pages/AttackLabPage';
import { TransactionInvestigatorPage } from './pages/TransactionInvestigatorPage';
import { ExplainabilityPage } from './pages/ExplainabilityPage';
import { RiskWaterfallPage } from './pages/RiskWaterfallPage';
import { LineagePage } from './pages/LineagePage';
import { DefenseGapsPage } from './pages/DefenseGapsPage';
import { HardeningPage } from './pages/HardeningPage';
import { CounterfactualExplorerPage } from './pages/CounterfactualExplorerPage';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<CommandCenterPage />} />
          <Route path="command-center" element={<CommandCenterPage />} />
          <Route path="overview" element={<OverviewPage />} />
          <Route path="attack-lab" element={<AttackLabPage />} />
          <Route path="investigator" element={<TransactionInvestigatorPage />} />
          <Route path="explainability" element={<ExplainabilityPage />} />
          <Route path="waterfall" element={<RiskWaterfallPage />} />
          <Route path="lineage" element={<LineagePage />} />
          <Route path="gaps" element={<DefenseGapsPage />} />
          <Route path="hardening" element={<HardeningPage />} />
          <Route path="counterfactual" element={<CounterfactualExplorerPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
