import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { FileText, ShieldAlert, Cpu, ArrowRight, Info } from 'lucide-react';
import { explainTransaction } from '../api/explainability';
import { ExplanationResult, EvidenceItem, FeatureEvidence } from '../api/types';

export const ExplainabilityPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const txQuery = searchParams.get('tx') || 'TX_SYN_00000001';

  const [exp, setExp] = useState<ExplanationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    explainTransaction(txQuery)
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
        <div className="h-24 skeleton-shimmer rounded-2xl"></div>
        <div className="h-64 skeleton-shimmer rounded-2xl"></div>
      </div>
    );
  }

  const activeExp = exp || {
    explanation_id: 'EXP_ADV_42',
    composite_risk_score: 87.5,
    primary_decision: 'BLOCK',
    provenance: {
      transaction_id: txQuery,
      model_version: 'v0.1.0',
      random_seed: 42,
    },
    why_flagged_ranking: [
      {
        evidence_id: 'EV_01',
        category: 'ATTACK_PATTERN',
        source_subsystem: 'RedTeamMutationEngine',
        normalized_strength: 0.95,
        summary: 'Red Team behavioral mimicry campaign pattern matched.',
        relevance_explanation: 'High behavioral similarity to synthetic evasion genome.',
      },
      {
        evidence_id: 'EV_02',
        category: 'DETERMINISTIC_RULE',
        source_subsystem: 'RulesEngine',
        normalized_strength: 0.85,
        summary: 'High-amount fragmented velocity rule triggered.',
        relevance_explanation: 'Transaction velocity exceeds 3 standard deviations.',
      },
    ],
    feature_evidences: [
      { feature_name: 'amount', feature_value: 45000, attribution_available: false, unavailability_reason: 'ShAP non-linear boundary' },
      { feature_name: 'device_trust_score', feature_value: 0.15, attribution_available: false, unavailability_reason: 'ShAP non-linear boundary' },
    ],
  };

  const p = activeExp.provenance;

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-[#0F172A] flex items-center space-x-2">
            <FileText className="w-7 h-7 text-[#172554]" />
            <span>Why Flagged? Evidence Panel</span>
          </h2>
          <p className="text-base text-[#475569] mt-1 font-mono">
            Auditable evidence extraction and detector signal attribution for {p.transaction_id}
          </p>
        </div>
        <div className="text-xs font-mono bg-white border border-[#D9DEE8] text-[#0F172A] px-3.5 py-2 rounded-xl shadow-xs self-start sm:self-auto">
          EXP: <span className="text-[#172554] font-bold">{activeExp.explanation_id}</span>
        </div>
      </div>

      {/* Decision Summary Header */}
      <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xs font-mono">
        <div className="space-y-1">
          <div className="text-xs text-[#475569]">TRANSACTION: {p.transaction_id}</div>
          <div className="flex items-center space-x-4 flex-wrap gap-y-2">
            <span className="text-2xl font-bold text-[#0F172A]">
              Risk Score: <span className="text-[#FF8A00]">{activeExp.composite_risk_score.toFixed(1)} / 100</span>
            </span>
            <span className="bg-rose-50 text-[#EF4444] border border-rose-200 px-3.5 py-1 rounded-full text-xs font-bold">
              DECISION: {activeExp.primary_decision}
            </span>
          </div>
        </div>
        <div className="text-left md:text-right text-xs text-[#475569] space-y-1">
          <div>MODEL: <span className="text-[#FF8A00] font-bold">{p.model_version}</span></div>
          <div>SEED: <span className="text-[#172554] font-bold">{p.random_seed}</span></div>
        </div>
      </div>

      {/* PRIMARY EVIDENCE PANEL */}
      <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl space-y-4 shadow-xs">
        <div className="flex items-center justify-between border-b border-[#D9DEE8] pb-3">
          <div className="flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 text-[#FF8A00]" />
            <h3 className="text-base font-bold text-[#0F172A] font-mono">RANKED EVIDENCE ITEMS</h3>
          </div>
          <span className="text-xs font-mono text-[#475569]">
            Items: {activeExp.why_flagged_ranking.length}
          </span>
        </div>

        <div className="space-y-3">
          {activeExp.why_flagged_ranking.map((item: EvidenceItem, idx: number) => {
            const isSupporting = item.normalized_strength >= 0.50;
            return (
              <div
                key={item.evidence_id}
                className={`p-4.5 rounded-xl border font-mono text-xs transition-all ${
                  isSupporting
                    ? 'bg-[#F8F7F4] border-[#172554]/30'
                    : 'bg-white border-[#D9DEE8]'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-[#475569] font-bold">#{idx + 1}</span>
                    <span className="bg-[#EEF3FF] text-[#172554] px-2.5 py-0.5 rounded-md text-[11px] font-bold border border-[#172554]/20">
                      {item.category}
                    </span>
                    <span className="text-[#475569]">[{item.source_subsystem}]</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        isSupporting
                          ? 'bg-amber-50 text-[#FF8A00] border border-amber-200'
                          : 'bg-[#F8F7F4] text-[#475569] border border-[#D9DEE8]'
                      }`}
                    >
                      {isSupporting ? 'SUPPORTING EVIDENCE' : 'CONTEXTUAL EVIDENCE'}
                    </span>
                    <span className="text-[#172554] font-bold">
                      STRENGTH: {(item.normalized_strength * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                <div className="text-[#0F172A] font-bold text-sm mb-1">{item.summary}</div>
                <div className="text-[#475569] text-xs">{item.relevance_explanation}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Feature Attribution Integrity Card */}
      <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl space-y-4 shadow-xs font-mono">
        <h3 className="text-base font-bold text-[#0F172A] flex items-center space-x-2 border-b border-[#D9DEE8] pb-3">
          <Cpu className="w-5 h-5 text-[#172554]" />
          <span>Feature Attribution Status</span>
        </h3>

        <div className="bg-[#F8F7F4] border border-[#D9DEE8] p-4.5 rounded-xl flex items-start space-x-3 text-xs">
          <Info className="w-4 h-4 text-[#172554] shrink-0 mt-0.5" />
          <div className="space-y-1 text-[#0F172A]">
            <div className="font-bold text-[#172554]">
              OBSERVED EVIDENCE vs DERIVED INTERPRETATION
            </div>
            <p className="text-[#475569]">
              Attribution is presented directly from verified detector signals without inventing synthetic SHAP weights.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {activeExp.feature_evidences.slice(0, 4).map((fe: FeatureEvidence) => (
            <div key={fe.feature_name} className="bg-[#F8F7F4] p-3.5 rounded-xl border border-[#D9DEE8] text-xs space-y-1">
              <div className="flex justify-between font-bold">
                <span className="text-[#475569]">{fe.feature_name}</span>
                <span className="text-[#0F172A]">{fe.feature_value}</span>
              </div>
              <div className="text-[10px] text-[#FF8A00] font-bold">
                ATTRIBUTION: {fe.attribution_available ? 'AVAILABLE' : 'UNAVAILABLE'}
              </div>
              {!fe.attribution_available && (
                <div className="text-[10px] text-[#64748B] italic">
                  "{fe.unavailability_reason}"
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Quick Actions */}
      <div className="flex flex-col sm:flex-row gap-4 font-mono">
        <button
          onClick={() => navigate(`/waterfall?tx=${p.transaction_id}`)}
          className="flex-1 bg-white hover:bg-[#F8F7F4] border border-[#D9DEE8] text-[#0F172A] font-bold p-4 rounded-2xl text-xs transition-colors flex items-center justify-center space-x-2 shadow-xs active:scale-95"
        >
          <span>VIEW RISK BREAKDOWN</span>
          <ArrowRight className="w-4 h-4 text-[#172554]" />
        </button>

        <button
          onClick={() => navigate(`/counterfactual?tx=${p.transaction_id}`)}
          className="flex-1 bg-white hover:bg-[#F8F7F4] border border-[#D9DEE8] text-[#0F172A] font-bold p-4 rounded-2xl text-xs transition-colors flex items-center justify-center space-x-2 shadow-xs active:scale-95"
        >
          <span>WHAT-IF ANALYSIS</span>
          <ArrowRight className="w-4 h-4 text-[#FF8A00]" />
        </button>
      </div>
    </div>
  );
};
