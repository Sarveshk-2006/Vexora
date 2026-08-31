import React, { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { getOverviewSummary } from '../../api/overview';
import { OverviewSummary } from '../../api/types';

export const Layout: React.FC = () => {
  const [overviewData, setOverviewData] = useState<OverviewSummary | null>(null);
  const [apiConnected, setApiConnected] = useState<boolean>(true);

  useEffect(() => {
    getOverviewSummary()
      .then((data) => {
        setOverviewData(data);
        setApiConnected(true);
      })
      .catch(() => {
        setApiConnected(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans antialiased selection:bg-emerald-500 selection:text-slate-950">
      <Header overviewData={overviewData} apiConnected={apiConnected} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 bg-slate-950">
          <Outlet context={{ overviewData, apiConnected }} />
        </main>
      </div>
    </div>
  );
};
