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
    <div className="bg-white border border-[#D9DDE5] rounded-xl p-5 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4 card-hover">
      <div className="flex items-center gap-3.5">
        <div className="p-2.5 rounded-lg bg-[#F8F7F4] border border-[#D9DDE5] text-[#273A91]">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-base font-bold text-[#111827] font-mono tracking-wide">
            Defense Simulation Engine
          </h2>
          <p className="text-xs text-[#475569] font-sans">
            Attack → Detect → Gap Analysis → Hardening → Re-Attack Validation
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3 w-full md:w-auto">
        <div className="flex items-center gap-2 bg-[#F8F7F4] border border-[#D9DDE5] rounded-lg px-3 py-2 font-mono text-xs">
          <Sliders className="w-3.5 h-3.5 text-[#273A91]" />
          <span className="text-[#475569] font-semibold">SEED:</span>
          <input
            type="number"
            value={seedInput}
            onChange={(e) => setSeedInput(parseInt(e.target.value, 10) || 42)}
            disabled={isRunning}
            className="w-14 bg-transparent text-[#111827] font-bold focus:outline-none text-right"
          />
        </div>

        <button
          onClick={handleRun}
          disabled={isRunning}
          className={`flex-1 md:flex-none flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg font-mono text-xs font-bold transition-all duration-200 shadow-md ${
            isRunning
              ? 'bg-[#D9DDE5] text-[#64748B] cursor-not-allowed border border-[#D9DDE5]'
              : 'bg-[#F98513] hover:bg-[#F98513]/90 text-white border border-[#F98513] shadow-md hover:shadow-lg active:scale-95'
          }`}
        >
          {isRunning ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin text-white" />
              <span>RUNNING SIMULATION...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 fill-white text-white" />
              <span>RUN SIMULATION CYCLE</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};
