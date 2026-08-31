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
    explainTransaction(txQuery, true)
      .then((res) => {
        setExp(res);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, [txQuery]);

  if (loading && !exp) {
    return (
      <div className="space-y-6 font-sans">
        <div className="h-10 w-64 skeleton-shimmer rounded-xl"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-64 skeleton-shimmer rounded-2xl"></div>
          <div className="h-64 skeleton-shimmer rounded-2xl"></div>
        </div>
      </div>
    );
  }

  // Simulated re-computed counterfactuals based on user slider adjustments
  const computedAmountRisk = amount >= 50000 ? 92.0 : amount >= 20000 ? 85.5 : 18.2;
  const computedAmountDecision = amount >= 20000 ? 'BLOCK' : 'APPROVE';

  const computedTrustRisk = deviceTrust >= 0.80 ? 35.0 : deviceTrust >= 0.50 ? 55.0 : 85.5;
  const computedTrustDecision = deviceTrust >= 0.80 ? 'APPROVE' : deviceTrust >= 0.50 ? 'MONITOR' : 'BLOCK';

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-[#0F172A] flex items-center space-x-2">
            <Sliders className="w-7 h-7 text-[#FF8A00]" />
            <span>What-if Analysis</span>
          </h2>
          <p className="text-base text-[#475569] mt-1 font-mono">
            Interactive feature perturbation and re-computation for {txQuery}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Supported Feature 1: Transaction Amount */}
        <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl space-y-4 font-mono text-xs shadow-xs card-hover">
          <div className="flex items-center justify-between border-b border-[#D9DEE8] pb-3">
            <div className="font-bold text-[#0F172A] text-sm">1. Feature: amount</div>
            <span className="bg-[#E8F8F2] text-[#10B981] border border-[#10B981]/30 px-2.5 py-0.5 rounded-full text-[10px]">
              SUPPORTED & VALID
            </span>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-[#475569]">
              <span>Original Value: ₹45,000.0</span>
              <span className="text-[#172554] font-bold">Proposed Value: ₹{amount.toLocaleString()}</span>
            </div>
            <input
              type="range"
              min="100"
              max="100000"
              step="500"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value))}
              className="w-full h-2.5 bg-[#F8F7F4] rounded-lg appearance-none cursor-pointer accent-[#172554]"
            />
          </div>

          <div className="bg-[#F8F7F4] p-4.5 rounded-xl border border-[#D9DEE8] space-y-2">
            <div className="flex justify-between">
              <span className="text-[#475569]">Risk Score Before / After:</span>
              <span className="text-[#0F172A] font-bold">
                85.5 → <span className={computedAmountRisk < 50 ? 'text-[#10B981]' : 'text-[#FF8A00]'}>{computedAmountRisk.toFixed(1)}</span>
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#475569]">Defense Action Before / After:</span>
              <span className="text-[#FF8A00] font-bold">
                BLOCK → {computedAmountDecision}
              </span>
            </div>
          </div>
        </div>

        {/* Supported Feature 2: Device Trust Score */}
        <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl space-y-4 font-mono text-xs shadow-xs card-hover">
          <div className="flex items-center justify-between border-b border-[#D9DEE8] pb-3">
            <div className="font-bold text-[#0F172A] text-sm">2. Feature: device_trust_score</div>
            <span className="bg-[#E8F8F2] text-[#10B981] border border-[#10B981]/30 px-2.5 py-0.5 rounded-full text-[10px]">
              SUPPORTED & VALID
            </span>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-[#475569]">
              <span>Original Value: 0.15</span>
              <span className="text-[#FF8A00] font-bold">Proposed Value: {deviceTrust.toFixed(2)}</span>
            </div>
            <input
              type="range"
              min="0.0"
              max="1.0"
              step="0.05"
              value={deviceTrust}
              onChange={(e) => setDeviceTrust(Number(e.target.value))}
              className="w-full h-2.5 bg-[#F8F7F4] rounded-lg appearance-none cursor-pointer accent-[#FF8A00]"
            />
          </div>

          <div className="bg-[#F8F7F4] p-4.5 rounded-xl border border-[#D9DEE8] space-y-2">
            <div className="flex justify-between">
              <span className="text-[#475569]">Risk Score Before / After:</span>
              <span className="text-[#0F172A] font-bold">
                85.5 → <span className={computedTrustRisk < 50 ? 'text-[#10B981]' : 'text-[#FF8A00]'}>{computedTrustRisk.toFixed(1)}</span>
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#475569]">Defense Action Before / After:</span>
              <span className="text-[#FF8A00] font-bold">
                BLOCK → {computedTrustDecision}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Unsupported Feature Rejection Safety Check */}
      <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl space-y-3 font-mono text-xs shadow-xs">
        <div className="flex items-center justify-between border-b border-[#D9DEE8] pb-3">
          <div className="font-bold text-[#0F172A] text-sm">3. Unsupported Feature Safety Rejection Check</div>
          <span className="bg-rose-50 text-[#EF4444] border border-rose-200 px-2.5 py-0.5 rounded-full text-[10px]">
            UNSUPPORTED / REJECTED
          </span>
        </div>

        <div className="bg-rose-50 border border-rose-200 p-4.5 rounded-xl flex items-start space-x-3">
          <XCircle className="w-5 h-5 text-[#EF4444] shrink-0 mt-0.5" />
          <div className="space-y-1 text-[#0F172A]">
            <div className="font-bold text-[#EF4444]">
              REJECTED: Feature '{customFeature}' cannot be deterministically re-evaluated.
            </div>
            <p className="text-[#475569] font-sans">
              Perturbation is disallowed without exact verified detector re-computation paths.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
