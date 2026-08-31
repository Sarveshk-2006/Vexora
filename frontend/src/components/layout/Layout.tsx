import React, { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { getOverviewSummary } from '../../api/overview';
import { OverviewSummary } from '../../api/types';

export const Layout: React.FC = () => {
  const [overviewData, setOverviewData] = useState<OverviewSummary | null>(null);
  const [apiConnected, setApiConnected] = useState<boolean>(true);
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

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
    <div className="min-h-screen bg-[#F7F5F0] text-[#0F172A] flex flex-col font-sans antialiased">
      <Header
        overviewData={overviewData}
        apiConnected={apiConnected}
        onToggleSidebar={() => setIsSidebarOpen((prev) => !prev)}
      />
      <div className="flex flex-1 overflow-hidden relative">
        <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 bg-[#F7F5F0]">
          <div className="max-w-7xl mx-auto space-y-6">
            <Outlet context={{ overviewData, apiConnected }} />
          </div>
        </main>
      </div>
    </div>
  );
};
