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
    explainTransaction(txQuery).then((res) => {
      setExp(res);
      setLoading(false);
    });
  }, [txQuery]);

  if (loading || !exp) {
    return (
      <div className="p-8 text-center text-slate-400 font-mono text-sm">
        Generating Phase 7A Explainability Evidence Bundle...
      </div>
    );
  }

  const p = exp.provenance;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            <span>Phase 7A Explainability Engine & Evidence Contract</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Auditable Evidence Extraction, Provenance Lineage & Ranked Signal Attribution
          </p>
        </div>
        <div className="text-xs font-mono bg-slate-900 border border-slate-800 text-slate-300 px-3 py-1.5 rounded">
          EXP ID: <span className="text-emerald-400 font-bold">{exp.explanation_id}</span>
        </div>
      </div>

      {/* Decision Summary Header */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg flex items-center justify-between">
        <div className="space-y-1">
          <div className="text-xs text-slate-500 font-mono">TRANSACTION ID: {p.transaction_id}</div>
          <div className="flex items-center space-x-3">
            <span className="text-2xl font-bold text-white font-mono">
              Composite Risk Score: <span className="text-rose-400">{exp.composite_risk_score.toFixed(1)} / 100</span>
            </span>
            <span className="bg-rose-500/10 text-rose-400 border border-rose-500/30 px-3 py-1 rounded text-xs font-mono font-bold">
              DECISION: {exp.primary_decision}
            </span>
          </div>
        </div>
        <div className="text-right font-mono text-xs text-slate-400 space-y-1">
          <div>MODEL: <span className="text-amber-400 font-bold">{p.model_version}</span></div>
          <div>SEED: <span className="text-emerald-400 font-bold">{p.random_seed}</span></div>
        </div>
      </div>

      {/* PRIMARY EVIDENCE PANEL: WHY WAS THIS FLAGGED? */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg space-y-4 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-bold text-white tracking-wider font-mono">WHY WAS THIS FLAGGED?</h3>
          </div>
          <span className="text-xs font-mono text-slate-400">
            Ranked Evidence Count: {exp.why_flagged_ranking.length}
          </span>
        </div>

        <div className="space-y-3">
          {exp.why_flagged_ranking.map((item: EvidenceItem, idx: number) => {
            const isSupporting = item.normalized_strength >= 0.50;
            return (
              <div
                key={item.evidence_id}
                className={`p-4 rounded-lg border font-mono text-xs transition-all ${
                  isSupporting
                    ? 'bg-slate-950 border-amber-500/30'
                    : 'bg-slate-950/60 border-slate-800'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center space-x-2">
                    <span className="text-slate-500 font-bold">#{idx + 1}</span>
                    <span className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded text-[10px] font-bold">
                      {item.category}
                    </span>
                    <span className="text-slate-400">[{item.source_subsystem}]</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        isSupporting
                          ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {isSupporting ? 'SUPPORTING EVIDENCE' : 'CONTEXTUAL EVIDENCE'}
                    </span>
                    <span className="text-emerald-400 font-bold">
                      STRENGTH: {(item.normalized_strength * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                <div className="text-white font-bold text-sm mb-1">{item.summary}</div>
                <div className="text-slate-400 text-xs">{item.relevance_explanation}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Feature Attribution Integrity Card (No Fabricated SHAP) */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg space-y-3">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-blue-400" />
          <span>ML Feature Attribution Transparency (Anti-Fabrication Check)</span>
        </h3>

        <div className="bg-blue-950/20 border border-blue-500/30 p-4 rounded-lg flex items-start space-x-3 text-xs">
          <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
          <div className="space-y-1 text-slate-300">
            <div className="font-bold text-blue-300 font-mono">
              OBSERVED EVIDENCE vs DERIVED INTERPRETATION
            </div>
            <p>
              Per-sample SHAP tree attribution is explicitly marked unavailable for lightweight RandomForest models to prevent metric fabrication. FRAUDOSCOPE never invents fake SHAP importance values.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {exp.feature_evidences.slice(0, 4).map((fe: FeatureEvidence) => (
            <div key={fe.feature_name} className="bg-slate-950 p-3 rounded border border-slate-800 font-mono text-xs space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-400">{fe.feature_name}</span>
                <span className="text-white font-bold">{fe.feature_value}</span>
              </div>
              <div className="text-[10px] text-amber-400">
                ATTRIBUTION: {fe.attribution_available ? 'AVAILABLE' : 'UNAVAILABLE'}
              </div>
              {!fe.attribution_available && (
                <div className="text-[10px] text-slate-500 italic">
                  "{fe.unavailability_reason}"
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Quick Actions */}
      <div className="flex space-x-4">
        <button
          onClick={() => navigate(`/waterfall?tx=${p.transaction_id}`)}
          className="flex-1 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 font-bold p-3 rounded-lg text-xs transition-colors flex items-center justify-center space-x-2"
        >
          <span>VIEW RISK WATERFALL</span>
          <ArrowRight className="w-4 h-4 text-emerald-400" />
        </button>

        <button
          onClick={() => navigate(`/counterfactual?tx=${p.transaction_id}`)}
          className="flex-1 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 font-bold p-3 rounded-lg text-xs transition-colors flex items-center justify-center space-x-2"
        >
          <span>OPEN COUNTERFACTUAL "WHAT IF?"</span>
          <ArrowRight className="w-4 h-4 text-amber-400" />
        </button>
      </div>
    </div>
  );
};
