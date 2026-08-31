import React, { useState } from 'react';
import { Sliders, CheckCircle2 } from 'lucide-react';

export const CounterfactualPanel: React.FC = () => {
  const [amount, setAmount] = useState<number>(45000);
  const [deviceTrust, setDeviceTrust] = useState<number>(0.15);
  const [velocityDev, setVelocityDev] = useState<number>(0.8);

  const calculateRisk = () => {
    let score = 20.0;
    if (amount > 30000) score += 30.0;
    if (deviceTrust < 0.3) score += 35.0;
    if (velocityDev > 0.5) score += 10.0;
    return Math.min(100.0, score);
  };

  const currentRisk = calculateRisk();

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-400" />
            Interactive Counterfactual "WHAT-IF?" Explorer
          </h3>
          <p className="text-xs text-slate-400">
            Re-evaluate Blue Team risk scoring under real-time feature perturbations
          </p>
        </div>
        <span className="text-xs font-mono px-3 py-1 rounded bg-slate-950 text-slate-300 border border-slate-800 font-bold">
          SAFE PERTURBATION ENGINE
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div>
          <div className="flex justify-between text-xs font-mono text-slate-300 mb-2">
            <span>TRANSACTION AMOUNT (₹)</span>
            <span className="font-bold text-emerald-400">₹{amount.toLocaleString()}</span>
          </div>
          <input
            type="range"
            min="1000"
            max="100000"
            step="1000"
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono text-slate-300 mb-2">
            <span>DEVICE TRUST SCORE</span>
            <span className="font-bold text-emerald-400">{deviceTrust.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0.0"
            max="1.0"
            step="0.05"
            value={deviceTrust}
            onChange={(e) => setDeviceTrust(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono text-slate-300 mb-2">
            <span>VELOCITY DEVIATION</span>
            <span className="font-bold text-emerald-400">{velocityDev.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0.0"
            max="1.0"
            step="0.05"
            value={velocityDev}
            onChange={(e) => setVelocityDev(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
          />
        </div>
      </div>

      <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between font-mono text-xs">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span className="text-slate-300">COUNTERFACTUAL RE-EVALUATED RISK SCORE:</span>
        </div>
        <span
          className={`text-base font-bold ${
            currentRisk >= 60.0 ? 'text-rose-400' : 'text-emerald-400'
          }`}
        >
          {currentRisk.toFixed(1)} / 100 [{currentRisk >= 60.0 ? 'FLAGGED' : 'APPROVED'}]
        </span>
      </div>
    </div>
  );
};
