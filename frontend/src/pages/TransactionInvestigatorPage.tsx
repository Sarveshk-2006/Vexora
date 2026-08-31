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
    getSyntheticTransactions()
      .then((res) => {
        setTransactions(res);
        if (txQuery) {
          const found = res.find((t) => t.id === txQuery);
          if (found) setSelectedTx(found);
          else if (res.length > 0) setSelectedTx(res[0]);
        } else if (res.length > 0) {
          setSelectedTx(res[0]);
        }
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, [txQuery]);

  if (loading && !selectedTx) {
    return (
      <div className="space-y-6 font-sans">
        <div className="h-10 w-64 skeleton-shimmer rounded-xl"></div>
        <div className="h-20 skeleton-shimmer rounded-2xl"></div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-48 skeleton-shimmer rounded-2xl"></div>
          ))}
        </div>
      </div>
    );
  }

  const activeTx = selectedTx || {
    id: 'TX_SYN_00000001',
    user_id: 'USER_SYN_0001',
    account_id: 'ACC_SYN_0001',
    merchant_id: 'MERCHANT_P2P_001',
    device_id: 'DEV_SYN_0001_EMULATED',
    amount: 45000,
    currency: 'INR',
    payment_rail: 'UPI',
    timestamp: new Date().toISOString(),
    risk_score: 85.5,
    decision: 'BLOCK',
    campaign_id: 'CAMP_BEHAVIORAL_MIMICRY_01',
  };

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-[#0F172A] flex items-center space-x-2">
            <Search className="w-7 h-7 text-[#172554]" />
            <span>Transaction Investigator</span>
          </h2>
          <p className="text-base text-[#475569] mt-1 font-normal">
            Transaction details, risk score, and attack attribution context
          </p>
        </div>
        <div className="text-xs font-mono bg-white border border-[#D9DEE8] text-[#0F172A] px-3.5 py-2 rounded-xl shadow-xs self-start sm:self-auto">
          TX: <span className="text-[#172554] font-bold">{activeTx.id}</span>
        </div>
      </div>

      {/* Transaction Selector Bar */}
      <div className="bg-white border border-[#D9DEE8] p-4.5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xs">
        <label className="text-xs text-[#475569] font-mono font-semibold flex items-center space-x-2">
          <Search className="w-4 h-4 text-[#172554]" />
          <span>SELECT TRANSACTION TO INSPECT:</span>
        </label>
        <select
          value={activeTx.id}
          onChange={(e) => {
            const found = transactions.find((t) => t.id === e.target.value);
            if (found) setSelectedTx(found);
          }}
          className="bg-[#F8F7F4] border border-[#D9DEE8] text-[#0F172A] font-mono text-xs px-4 py-2.5 rounded-xl focus:outline-none focus:border-[#172554] w-full md:w-auto min-w-[320px]"
        >
          {(transactions.length > 0 ? transactions : [activeTx]).map((t) => (
            <option key={t.id} value={t.id}>
              {t.id} — ₹{t.amount.toLocaleString()} ({t.payment_rail}) — {t.decision || 'BLOCK'}
            </option>
          ))}
        </select>
      </div>

      {/* 4 Primary Category Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* IDENTITY */}
        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl space-y-3 font-mono text-xs shadow-xs card-hover">
          <div className="flex items-center space-x-2 text-[#172554] font-bold border-b border-[#D9DEE8] pb-2 text-sm">
            <User className="w-4 h-4 text-[#172554]" />
            <span>IDENTITY</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">USER ID</span>
            <span className="text-[#0F172A] font-bold text-sm">{activeTx.user_id}</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">ACCOUNT REFERENCE</span>
            <span className="text-[#172554] font-semibold">{activeTx.account_id}</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">DEVICE ID</span>
            <span className="text-[#64748B] text-[11px] truncate block">{activeTx.device_id}</span>
          </div>
        </div>

        {/* TRANSACTION */}
        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl space-y-3 font-mono text-xs shadow-xs card-hover">
          <div className="flex items-center space-x-2 text-[#172554] font-bold border-b border-[#D9DEE8] pb-2 text-sm">
            <CreditCard className="w-4 h-4 text-[#172554]" />
            <span>TRANSACTION</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">AMOUNT & CURRENCY</span>
            <span className="text-[#0F172A] font-bold text-lg">₹{activeTx.amount.toLocaleString()} {activeTx.currency}</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">PAYMENT RAIL / TIMESTAMP</span>
            <span className="text-[#0F172A] font-medium">{activeTx.payment_rail} | {activeTx.timestamp.split('T')[0]}</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">MERCHANT ID</span>
            <span className="text-[#64748B] text-[11px]">{activeTx.merchant_id}</span>
          </div>
        </div>

        {/* RISK */}
        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl space-y-3 font-mono text-xs shadow-xs card-hover">
          <div className="flex items-center space-x-2 text-[#FF8A00] font-bold border-b border-[#D9DEE8] pb-2 text-sm">
            <ShieldAlert className="w-4 h-4 text-[#FF8A00]" />
            <span>RISK</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">COMPOSITE RISK SCORE</span>
            <span className="text-[#FF8A00] font-bold text-lg">{activeTx.risk_score ?? 85.5} / 100</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">DEFENSE DECISION</span>
            <span className="bg-rose-50 text-[#EF4444] border border-rose-200 px-3 py-1 rounded-full text-[11px] font-bold">
              {activeTx.decision ?? 'BLOCK'}
            </span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">SEVERITY STATE</span>
            <span className="text-[#FF8A00] font-bold">HIGH_RISK</span>
          </div>
        </div>

        {/* ATTACK */}
        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl space-y-3 font-mono text-xs shadow-xs card-hover">
          <div className="flex items-center space-x-2 text-[#172554] font-bold border-b border-[#D9DEE8] pb-2 text-sm">
            <Smartphone className="w-4 h-4 text-[#172554]" />
            <span>ATTACK</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">CAMPAIGN ID</span>
            <span className="text-[#172554] font-bold text-sm">{activeTx.campaign_id ?? 'CAMP_BEHAVIORAL_MIMICRY_01'}</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">GENOME VERSION</span>
            <span className="text-[#0F172A] font-medium">SYN_GENOME_000001 (v1.0.0)</span>
          </div>
          <div>
            <span className="text-[#475569] block text-[10px]">ATTACK FAMILY</span>
            <span className="text-[#FF8A00] font-bold">BEHAVIORAL_MIMICRY</span>
          </div>
        </div>
      </div>

      {/* Action Banner */}
      <div className="bg-white text-[#0F172A] border border-[#D9DEE8] p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm">
        <div>
          <h3 className="text-lg font-bold font-mono text-[#0F172A]">Investigate Explainability Evidence</h3>
          <p className="text-sm text-[#475569] mt-1 font-sans">
            Inspect ranked evidence, risk breakdown, and counterfactuals for {activeTx.id}.
          </p>
        </div>
        <button
          onClick={() => navigate(`/explainability?tx=${activeTx.id}`)}
          className="bg-[#FF8A00] hover:bg-[#FF8A00]/90 text-white font-mono font-bold px-6 py-3 rounded-xl text-xs transition-all inline-flex items-center justify-center space-x-2 shadow-md active:scale-95 shrink-0"
        >
          <span>INVESTIGATE EXPLAINABILITY</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
