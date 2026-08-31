import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Search, ShieldAlert, User, CreditCard, Smartphone, ArrowRight } from 'lucide-react';
import { getSyntheticTransactions } from '../api/transactions';
import { SyntheticTransaction } from '../api/types';

export const TransactionInvestigatorPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const txQuery = searchParams.get('tx');

  const [transactions, setTransactions] = useState<SyntheticTransaction[]>([]);
  const [selectedTx, setSelectedTx] = useState<SyntheticTransaction | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getSyntheticTransactions().then((res) => {
      setTransactions(res);
      if (txQuery) {
        const found = res.find((t) => t.id === txQuery);
        if (found) setSelectedTx(found);
        else if (res.length > 0) setSelectedTx(res[0]);
      } else if (res.length > 0) {
        setSelectedTx(res[0]);
      }
      setLoading(false);
    });
  }, [txQuery]);

  if (loading || !selectedTx) {
    return (
      <div className="p-8 text-center text-slate-400 font-mono text-sm">
        Loading Synthetic Transaction Investigator...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <Search className="w-5 h-5 text-emerald-400" />
            <span>Synthetic Transaction Investigator</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Transaction Inspection & Subsystem Risk Attribution
          </p>
        </div>
        <div className="text-xs font-mono bg-slate-900 border border-slate-800 text-slate-300 px-3 py-1.5 rounded">
          SELECTED TX: <span className="text-emerald-400 font-bold">{selectedTx.id}</span>
        </div>
      </div>

      {/* Transaction Selector Dropdown / Bar */}
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg flex items-center justify-between">
        <label className="text-xs text-slate-400 font-mono font-medium flex items-center space-x-2">
          <span>SELECT TRANSACTION TO INSPECT:</span>
        </label>
        <select
          value={selectedTx.id}
          onChange={(e) => {
            const found = transactions.find((t) => t.id === e.target.value);
            if (found) setSelectedTx(found);
          }}
          className="bg-slate-950 border border-slate-700 text-white font-mono text-xs px-3 py-1.5 rounded focus:outline-none focus:border-emerald-500 min-w-[300px]"
        >
          {transactions.map((t) => (
            <option key={t.id} value={t.id}>
              {t.id} — ₹{t.amount.toLocaleString()} ({t.payment_rail}) — {t.decision || 'BLOCK'}
            </option>
          ))}
        </select>
      </div>

      {/* 4 Primary Category Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* IDENTITY */}
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg space-y-2 font-mono text-xs">
          <div className="flex items-center space-x-2 text-slate-400 font-bold border-b border-slate-800 pb-2">
            <User className="w-4 h-4 text-blue-400" />
            <span>IDENTITY</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">USER ID</span>
            <span className="text-white font-bold">{selectedTx.user_id}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">ACCOUNT REFERENCE</span>
            <span className="text-slate-300">{selectedTx.account_id}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">DEVICE ID</span>
            <span className="text-slate-400 text-[11px] truncate block">{selectedTx.device_id}</span>
          </div>
        </div>

        {/* TRANSACTION */}
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg space-y-2 font-mono text-xs">
          <div className="flex items-center space-x-2 text-slate-400 font-bold border-b border-slate-800 pb-2">
            <CreditCard className="w-4 h-4 text-emerald-400" />
            <span>TRANSACTION</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">AMOUNT & CURRENCY</span>
            <span className="text-emerald-400 font-bold text-base">₹{selectedTx.amount.toLocaleString()} {selectedTx.currency}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">PAYMENT RAIL / TIMESTAMP</span>
            <span className="text-slate-300">{selectedTx.payment_rail} | {selectedTx.timestamp}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">MERCHANT ID</span>
            <span className="text-slate-400 text-[11px]">{selectedTx.merchant_id}</span>
          </div>
        </div>

        {/* RISK */}
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg space-y-2 font-mono text-xs">
          <div className="flex items-center space-x-2 text-slate-400 font-bold border-b border-slate-800 pb-2">
            <ShieldAlert className="w-4 h-4 text-rose-400" />
            <span>RISK</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">COMPOSITE RISK SCORE</span>
            <span className="text-rose-400 font-bold text-base">{selectedTx.risk_score ?? 85.5} / 100</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">DEFENSE DECISION</span>
            <span className="bg-rose-500/10 text-rose-400 border border-rose-500/30 px-2 py-0.5 rounded text-[10px] font-bold">
              {selectedTx.decision ?? 'BLOCK'}
            </span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">SEVERITY STATE</span>
            <span className="text-amber-400 font-bold">HIGH_RISK</span>
          </div>
        </div>

        {/* ATTACK */}
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg space-y-2 font-mono text-xs">
          <div className="flex items-center space-x-2 text-slate-400 font-bold border-b border-slate-800 pb-2">
            <Smartphone className="w-4 h-4 text-purple-400" />
            <span>ATTACK</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">CAMPAIGN ID</span>
            <span className="text-purple-300 font-bold">{selectedTx.campaign_id ?? 'CAMP_BEHAVIORAL_MIMICRY_01'}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">GENOME VERSION</span>
            <span className="text-slate-300">SYN_GENOME_000001 (v1.0.0)</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">ATTACK FAMILY</span>
            <span className="text-amber-400">BEHAVIORAL_MIMICRY</span>
          </div>
        </div>
      </div>

      {/* Action Banner */}
      <div className="bg-emerald-950/30 border border-emerald-500/30 p-5 rounded-lg flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-emerald-300">Ready for Deep Explainability Audit?</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Inspect ranked evidence, risk decision waterfall, attack lineage, and counterfactuals for {selectedTx.id}.
          </p>
        </div>
        <button
          onClick={() => navigate(`/explainability?tx=${selectedTx.id}`)}
          className="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-5 py-2.5 rounded-lg text-xs transition-colors inline-flex items-center space-x-2 shadow-lg"
        >
          <span>INVESTIGATE EXPLAINABILITY</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
