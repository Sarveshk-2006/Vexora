import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap, ShieldAlert, Cpu, ArrowRight } from 'lucide-react';
import { getAttackCampaigns } from '../api/campaigns';
import { getSyntheticTransactions } from '../api/transactions';
import { AttackCampaign, SyntheticTransaction } from '../api/types';

export const AttackLabPage: React.FC = () => {
  const navigate = useNavigate();
  const [campaigns, setCampaigns] = useState<AttackCampaign[]>([]);
  const [selectedCampaign, setSelectedCampaign] = useState<AttackCampaign | null>(null);
  const [transactions, setTransactions] = useState<SyntheticTransaction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    Promise.all([getAttackCampaigns(), getSyntheticTransactions()]).then(([cRes, tRes]) => {
      setCampaigns(cRes);
      if (cRes.length > 0) setSelectedCampaign(cRes[0]);
      setTransactions(tRes);
      setLoading(false);
    });
  }, []);

  if (loading || !selectedCampaign) {
    return (
      <div className="p-8 text-center text-slate-400 font-mono text-sm">
        Loading Attack Lab Campaigns...
      </div>
    );
  }

  const g = selectedCampaign.genome;

  const genomeGroups = [
    { title: 'IDENTITY', key: 'identity_state', val: g.identity_state, color: 'border-blue-500/40 text-blue-400' },
    { title: 'DEVICE', key: 'device_strategy', val: g.device_strategy, color: 'border-purple-500/40 text-purple-400' },
    { title: 'LOCATION', key: 'location_strategy', val: g.location_strategy, color: 'border-cyan-500/40 text-cyan-400' },
    { title: 'AMOUNT', key: 'amount_pattern', val: g.amount_pattern, color: 'border-emerald-500/40 text-emerald-400' },
    { title: 'VELOCITY', key: 'velocity_pattern', val: g.velocity_pattern, color: 'border-amber-500/40 text-amber-400' },
    { title: 'TIMING', key: 'timing_pattern', val: g.timing_pattern, color: 'border-yellow-500/40 text-yellow-400' },
    { title: 'MERCHANT', key: 'merchant_strategy', val: g.merchant_strategy, color: 'border-indigo-500/40 text-indigo-400' },
    { title: 'BEHAVIOR', key: 'behavioral_similarity', val: `${(g.behavioral_similarity * 100).toFixed(0)}% Similarity`, color: 'border-rose-500/40 text-rose-400' },
    { title: 'NETWORK', key: 'network_coordination', val: g.network_coordination, color: 'border-pink-500/40 text-pink-400' },
    { title: 'RAIL', key: 'payment_rail', val: g.payment_rail, color: 'border-teal-500/40 text-teal-400' },
    { title: 'EVASION', key: 'evasion_strategy', val: g.evasion_strategy, color: 'border-orange-500/40 text-orange-400' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <Zap className="w-5 h-5 text-amber-400" />
            <span>Attack Lab & Fraud Genome Synthesis</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Red Team Adversarial Campaign Inspector & Mutation Matrix
          </p>
        </div>
        <div className="text-xs font-mono bg-slate-900 border border-slate-800 text-slate-300 px-3 py-1.5 rounded">
          CAMPAIGN ID: <span className="text-amber-400 font-bold">{selectedCampaign.campaign_id}</span>
        </div>
      </div>

      {/* Campaign Selector Bar */}
      <div className="flex space-x-3 overflow-x-auto pb-2">
        {campaigns.map((c) => (
          <button
            key={c.campaign_id}
            onClick={() => setSelectedCampaign(c)}
            className={`px-4 py-2.5 rounded-lg border text-xs font-mono font-medium transition-all text-left min-w-[240px] ${
              selectedCampaign.campaign_id === c.campaign_id
                ? 'bg-amber-500/10 border-amber-500/50 text-amber-300 shadow-md'
                : 'bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
            }`}
          >
            <div className="font-bold">{c.campaign_id}</div>
            <div className="text-[11px] text-slate-500 mt-1">
              Family: {c.genome.attack_type} | Rail: {c.genome.payment_rail}
            </div>
          </button>
        ))}
      </div>

      {/* Metadata Inspector Card */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-base font-bold text-white font-mono">{g.objective}</h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Target Population: <span className="text-slate-200">{g.target_population}</span> | Stage: <span className="text-slate-200">{g.campaign_stage}</span>
            </p>
          </div>
          <div className="text-right">
            <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs px-2.5 py-1 rounded font-mono font-bold">
              FIDELITY SCORE: {(selectedCampaign.behavioral_fidelity_score * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
          <div className="bg-slate-950 p-2.5 rounded border border-slate-800">
            <span className="text-slate-500 block">INTENSITY</span>
            <span className="text-amber-400 font-bold">{selectedCampaign.intensity.toFixed(1)}</span>
          </div>
          <div className="bg-slate-950 p-2.5 rounded border border-slate-800">
            <span className="text-slate-500 block">NOVELTY RATING</span>
            <span className="text-purple-400 font-bold">{g.novelty_rating.toFixed(2)}</span>
          </div>
          <div className="bg-slate-950 p-2.5 rounded border border-slate-800">
            <span className="text-slate-500 block">AFFECTED TRANSACTIONS</span>
            <span className="text-blue-400 font-bold">{selectedCampaign.affected_transaction_count} TXs</span>
          </div>
          <div className="bg-slate-950 p-2.5 rounded border border-slate-800">
            <span className="text-slate-500 block">REPRODUCIBILITY SEED</span>
            <span className="text-emerald-400 font-bold">{selectedCampaign.seed}</span>
          </div>
        </div>
      </div>

      {/* Visual Fraud Genome 11-Group Matrix */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg">
        <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-amber-400" />
          <span>Synthetic Fraud Genome Matrix (11 Dimensions)</span>
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {genomeGroups.map((group) => (
            <div key={group.title} className={`bg-slate-950 p-3 rounded border ${group.color}`}>
              <div className="text-[10px] font-mono font-bold tracking-wider uppercase opacity-70">
                {group.title}
              </div>
              <div className="text-xs font-mono font-bold mt-1 truncate" title={String(group.val)}>
                {String(group.val)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Campaign Affected Transactions Table */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg space-y-3">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center space-x-2">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          <span>Campaign Affected Transactions ({transactions.length})</span>
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[10px]">
              <tr>
                <th className="p-2.5">TRANSACTION ID</th>
                <th className="p-2.5">USER / ACCOUNT</th>
                <th className="p-2.5">AMOUNT</th>
                <th className="p-2.5">RAIL</th>
                <th className="p-2.5">RISK SCORE</th>
                <th className="p-2.5">DECISION</th>
                <th className="p-2.5 text-right">ACTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {transactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-slate-800/40">
                  <td className="p-2.5 font-bold text-amber-400">{tx.id}</td>
                  <td className="p-2.5 text-slate-400">
                    {tx.user_id} <br />
                    <span className="text-[10px] text-slate-500">{tx.account_id}</span>
                  </td>
                  <td className="p-2.5 font-bold text-white">
                    ₹{tx.amount.toLocaleString()} <span className="text-[10px] text-slate-500">{tx.currency}</span>
                  </td>
                  <td className="p-2.5">{tx.payment_rail}</td>
                  <td className="p-2.5 font-bold text-rose-400">{tx.risk_score ?? 85.5} / 100</td>
                  <td className="p-2.5">
                    <span className="bg-rose-500/10 text-rose-400 border border-rose-500/30 px-2 py-0.5 rounded text-[10px] font-bold">
                      {tx.decision ?? 'BLOCK'}
                    </span>
                  </td>
                  <td className="p-2.5 text-right">
                    <button
                      onClick={() => navigate(`/investigator?tx=${tx.id}`)}
                      className="bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/30 px-3 py-1 rounded text-xs transition-colors inline-flex items-center space-x-1"
                    >
                      <span>INVESTIGATE</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
