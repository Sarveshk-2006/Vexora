import React, { useEffect, useState } from 'react';
import { fetchHealthStatus } from './services/api';
import { BackendHealthState } from './types/health';
import { Activity, ShieldAlert, CheckCircle, AlertCircle } from 'lucide-react';

export const App: React.FC = () => {
  const [status, setStatus] = useState<BackendHealthState>('Checking...');

  useEffect(() => {
    let isMounted = true;

    async function checkHealth() {
      try {
        const res = await fetchHealthStatus();
        if (isMounted) {
          if (res.status === 'ok') {
            setStatus('Online');
          } else {
            setStatus('Offline');
          }
        }
      } catch (err) {
        if (isMounted) {
          setStatus('Offline');
        }
      }
    }

    checkHealth();
    const interval = setInterval(checkHealth, 10000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 flex flex-col justify-between p-6">
      {/* Header Bar */}
      <header className="border-b border-gray-800 pb-4 mb-8">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-indigo-900/40 border border-indigo-500/30 rounded-lg">
              <ShieldAlert className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white">FRAUDOSCOPE</h1>
              <p className="text-xs text-indigo-300 font-medium">
                Autonomous Adversarial Payment Security Lab
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 bg-gray-900/80 border border-gray-800 px-4 py-2 rounded-full">
            <Activity className="w-4 h-4 text-gray-400" />
            <span className="text-xs font-semibold text-gray-400">Backend status:</span>
            {status === 'Checking...' && (
              <span className="text-xs font-bold text-yellow-400 flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-yellow-400 animate-pulse"></span>
                Checking...
              </span>
            )}
            {status === 'Online' && (
              <span className="text-xs font-bold text-emerald-400 flex items-center gap-1">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                Online
              </span>
            )}
            {status === 'Offline' && (
              <span className="text-xs font-bold text-rose-400 flex items-center gap-1">
                <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
                Offline
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto w-full flex-grow flex items-center justify-center">
        <div className="bg-gray-900/50 border border-gray-800/80 rounded-2xl p-10 text-center max-w-2xl shadow-xl backdrop-blur-sm">
          <div className="inline-flex p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl mb-4">
            <ShieldAlert className="w-10 h-10 text-indigo-400" />
          </div>
          <h2 className="text-3xl font-extrabold text-white mb-3">
            FRAUDOSCOPE Repository Shell Initialized
          </h2>
          <p className="text-gray-400 text-sm leading-relaxed mb-6">
            Phase 1 repository architecture and environment foundation established successfully.
            Ready for Phase 2 domain entity implementations.
          </p>

          <div className="grid grid-cols-2 gap-4 text-left border-t border-gray-800 pt-6 mt-6">
            <div className="bg-gray-950/60 p-4 rounded-xl border border-gray-800/60">
              <span className="text-xs text-gray-500 uppercase font-semibold">Active Architecture</span>
              <p className="text-sm font-medium text-gray-200 mt-1">Modular Monolith Core</p>
            </div>
            <div className="bg-gray-950/60 p-4 rounded-xl border border-gray-800/60">
              <span className="text-xs text-gray-500 uppercase font-semibold">Current Phase</span>
              <p className="text-sm font-medium text-emerald-400 mt-1">Phase 1 Complete</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800/60 pt-4 mt-8 text-center">
        <p className="text-xs text-gray-500">
          FRAUDOSCOPE Security Research Sandbox &bull; Synthetic Data Only &bull; 2026
        </p>
      </footer>
    </div>
  );
};

export default App;
