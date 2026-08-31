import React, { useState } from 'react';
import { Play, RefreshCw, Sliders, ShieldCheck } from 'lucide-react';

interface RunControlPanelProps {
  onRunSimulation: (seed: number) => Promise<void>;
  isRunning: boolean;
  activeSeed: number;
}

export const RunControlPanel: React.FC<RunControlPanelProps> = ({
  onRunSimulation,
  isRunning,
  activeSeed,
}) => {
  const [seedInput, setSeedInput] = useState<number>(activeSeed);

  const handleRun = async () => {
    if (isRunning) return;
    await onRunSimulation(seedInput);
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-4">
      <div className="flex items-center gap-4">
        <div className="p-3 rounded-lg bg-emerald-950/60 border border-emerald-800/80 text-emerald-400">
          <ShieldCheck className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-base font-bold text-slate-100 font-mono tracking-wide">
            CLOSED-LOOP DEFENSE HARDENING ENGINE
          </h2>
          <p className="text-xs text-slate-400">
            Deterministic digital-twin simulation (Attack → Detect → Harden → Re-Attack)
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3 w-full md:w-auto">
        <div className="flex items-center gap-2 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 font-mono text-xs">
          <Sliders className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-400">SEED:</span>
          <input
            type="number"
            value={seedInput}
            onChange={(e) => setSeedInput(parseInt(e.target.value, 10) || 42)}
            disabled={isRunning}
            className="w-16 bg-transparent text-emerald-400 font-bold focus:outline-none text-right"
          />
        </div>

        <button
          onClick={handleRun}
          disabled={isRunning}
          className={`flex-1 md:flex-none flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg font-mono text-xs font-bold transition-all duration-200 shadow-lg ${
            isRunning
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
              : 'bg-emerald-500 hover:bg-emerald-400 text-slate-950 border border-emerald-400 shadow-emerald-950/60 hover:shadow-emerald-500/20'
          }`}
        >
          {isRunning ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />
              <span>RUNNING SIMULATION...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 fill-slate-950" />
              <span>RUN CLOSED-LOOP SIMULATION</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};
