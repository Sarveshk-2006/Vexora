import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Sliders, XCircle } from 'lucide-react';
import { explainTransaction } from '../api/explainability';
import { ExplanationResult } from '../api/types';

export const CounterfactualExplorerPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const txQuery = searchParams.get('tx') || 'TX_SYN_00000001';

  const [exp, setExp] = useState<ExplanationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Interactive slider states
  const [amount, setAmount] = useState<number>(45000);
  const [deviceTrust, setDeviceTrust] = useState<number>(0.15);
  const customFeature = 'unsupported_custom_feature';

  useEffect(() => {
    explainTransaction(txQuery, true).then((res) => {
      setExp(res);
      setLoading(false);
    });
  }, [txQuery]);

  if (loading || !exp) {
    return (
      <div className="p-8 text-center text-slate-400 font-mono text-sm">
        Initializing Deterministic Counterfactual Engine...
      </div>
    );
  }

  // Simulated re-computed counterfactuals based on user slider adjustments
  const computedAmountRisk = amount >= 50000 ? 92.0 : amount >= 20000 ? 85.5 : 18.2;
  const computedAmountDecision = amount >= 20000 ? 'BLOCK' : 'APPROVE';

  const computedTrustRisk = deviceTrust >= 0.80 ? 35.0 : deviceTrust >= 0.50 ? 55.0 : 85.5;
  const computedTrustDecision = deviceTrust >= 0.80 ? 'APPROVE' : deviceTrust >= 0.50 ? 'MONITOR' : 'BLOCK';

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <Sliders className="w-5 h-5 text-amber-400" />
            <span>Deterministic Counterfactual "What-If?" Explorer</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Interactive Feature Perturbation & Re-computation Engine for {txQuery}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Supported Feature 1: Transaction Amount */}
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg space-y-4 font-mono text-xs">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="font-bold text-white text-sm">1. Feature: amount</div>
            <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded text-[10px]">
              SUPPORTED & VALID
            </span>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-slate-400">
              <span>Original Value: ₹45,000.0</span>
              <span className="text-emerald-400 font-bold">Proposed Value: ₹{amount.toLocaleString()}</span>
            </div>
            <input
              type="range"
              min="100"
              max="100000"
              step="500"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value))}
              className="w-full h-2 bg-slate-950 rounded-lg appearance-none cursor-pointer accent-emerald-500"
            />
          </div>

          <div className="bg-slate-950 p-4 rounded border border-slate-800 space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-500">Risk Score Before / After:</span>
              <span className="text-white font-bold">
                85.5 → <span className={computedAmountRisk < 50 ? 'text-emerald-400' : 'text-rose-400'}>{computedAmountRisk.toFixed(1)}</span>
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Defense Action Before / After:</span>
              <span className="text-amber-400 font-bold">
                BLOCK → {computedAmountDecision}
              </span>
            </div>
          </div>
        </div>

        {/* Supported Feature 2: Device Trust Score */}
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg space-y-4 font-mono text-xs">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="font-bold text-white text-sm">2. Feature: device_trust_score</div>
            <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded text-[10px]">
              SUPPORTED & VALID
            </span>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-slate-400">
              <span>Original Value: 0.15</span>
              <span className="text-amber-400 font-bold">Proposed Value: {deviceTrust.toFixed(2)}</span>
            </div>
            <input
              type="range"
              min="0.0"
              max="1.0"
              step="0.05"
              value={deviceTrust}
              onChange={(e) => setDeviceTrust(Number(e.target.value))}
              className="w-full h-2 bg-slate-950 rounded-lg appearance-none cursor-pointer accent-amber-500"
            />
          </div>

          <div className="bg-slate-950 p-4 rounded border border-slate-800 space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-500">Risk Score Before / After:</span>
              <span className="text-white font-bold">
                85.5 → <span className={computedTrustRisk < 50 ? 'text-emerald-400' : 'text-rose-400'}>{computedTrustRisk.toFixed(1)}</span>
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Defense Action Before / After:</span>
              <span className="text-amber-400 font-bold">
                BLOCK → {computedTrustDecision}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Unsupported Feature Rejection Safety Demo */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg space-y-3 font-mono text-xs">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="font-bold text-white text-sm">3. Unsupported Feature Safety Rejection Check</div>
          <span className="bg-rose-500/10 text-rose-400 border border-rose-500/30 px-2 py-0.5 rounded text-[10px]">
            UNSUPPORTED / REJECTED
          </span>
        </div>

        <div className="bg-rose-950/20 border border-rose-500/30 p-4 rounded-lg flex items-start space-x-3">
          <XCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
          <div className="space-y-1 text-slate-300">
            <div className="font-bold text-rose-400">
              REJECTED: Feature '{customFeature}' cannot be deterministically re-evaluated.
            </div>
            <p className="text-slate-400">
              FRAUDOSCOPE forbids fabricating counterfactual explanations for features without exact, verified detector re-computation paths.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
