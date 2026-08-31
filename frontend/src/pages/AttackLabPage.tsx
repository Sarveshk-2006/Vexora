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
    Promise.all([getAttackCampaigns(), getSyntheticTransactions()])
      .then(([cRes, tRes]) => {
        setCampaigns(cRes);
        if (cRes.length > 0) setSelectedCampaign(cRes[0]);
        setTransactions(tRes);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  if (loading && !selectedCampaign) {
    return (
      <div className="space-y-6 font-sans">
        <div className="h-10 w-64 skeleton-shimmer rounded-xl"></div>
        <div className="h-48 skeleton-shimmer rounded-2xl"></div>
        <div className="h-64 skeleton-shimmer rounded-2xl"></div>
      </div>
    );
  }

  const activeCampaign = selectedCampaign || {
    campaign_id: 'CAMP_BEHAVIORAL_MIMICRY_01',
    scenario_id: 'SCEN_G0_BEHAVIORAL_MIMICRY_UPI',
    seed: 42,
    intensity: 0.85,
    behavioral_fidelity_score: 0.92,
    affected_transaction_count: 12,
    genome: {
      attack_type: 'BEHAVIORAL_MIMICRY',
      payment_rail: 'UPI',
      objective: 'EVADE_TRANSACTION_ML',
      target_population: 'HIGH_VALUE_USERS',
      campaign_stage: 'EXPLOITATION',
      novelty_rating: 0.78,
      identity_state: 'SYNTHETIC_CLEAN',
      device_strategy: 'KNOWN_DEVICE_EMULATION',
      location_strategy: 'GEO_CONSISTENT',
      amount_pattern: 'FRAGMENTED_MICRO_TRANSFERS',
      velocity_pattern: 'BURST_WITHIN_WINDOW',
      timing_pattern: 'OFF_PEAK_HOURS',
      merchant_strategy: 'P2P_MIXING',
      behavioral_similarity: 0.92,
      network_coordination: 'RING_TOPOLOGY',
      evasion_strategy: 'SHAP_FEATURE_PERTURBATION',
      intended_duration: '24_HOURS',
    },
  };

  const g = activeCampaign.genome;

  const genomeGroups = [
    { title: 'IDENTITY', key: 'identity_state', val: g.identity_state, color: 'border-[#172554]/30 text-[#172554]' },
    { title: 'DEVICE', key: 'device_strategy', val: g.device_strategy, color: 'border-[#172554]/30 text-[#172554]' },
    { title: 'LOCATION', key: 'location_strategy', val: g.location_strategy, color: 'border-[#172554]/30 text-[#172554]' },
    { title: 'AMOUNT', key: 'amount_pattern', val: g.amount_pattern, color: 'border-[#FF8A00]/40 text-[#FF8A00]' },
    { title: 'VELOCITY', key: 'velocity_pattern', val: g.velocity_pattern, color: 'border-[#FF8A00]/40 text-[#FF8A00]' },
    { title: 'TIMING', key: 'timing_pattern', val: g.timing_pattern, color: 'border-[#172554]/30 text-[#172554]' },
    { title: 'MERCHANT', key: 'merchant_strategy', val: g.merchant_strategy, color: 'border-[#172554]/30 text-[#172554]' },
    { title: 'BEHAVIOR', key: 'behavioral_similarity', val: `${(g.behavioral_similarity * 100).toFixed(0)}% Similarity`, color: 'border-[#FF8A00]/40 text-[#FF8A00]' },
    { title: 'NETWORK', key: 'network_coordination', val: g.network_coordination, color: 'border-[#172554]/30 text-[#172554]' },
    { title: 'RAIL', key: 'payment_rail', val: g.payment_rail, color: 'border-[#172554]/30 text-[#172554]' },
    { title: 'EVASION', key: 'evasion_strategy', val: g.evasion_strategy, color: 'border-[#FF8A00]/40 text-[#FF8A00]' },
  ];

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-[#0F172A] flex items-center space-x-2">
            <Zap className="w-7 h-7 text-[#FF8A00]" />
            <span>Attack Lab</span>
          </h2>
          <p className="text-base text-[#475569] mt-1 font-normal">
            Red Team attack campaign profile and behavioral mutation dimensions
          </p>
        </div>
        <div className="text-xs font-mono bg-white border border-[#D9DEE8] text-[#0F172A] px-3.5 py-2 rounded-xl shadow-xs self-start sm:self-auto">
          CAMPAIGN: <span className="text-[#FF8A00] font-bold">{activeCampaign.campaign_id}</span>
        </div>
      </div>

      {/* Campaign Selector Bar */}
      <div className="flex space-x-3 overflow-x-auto pb-2">
        {(campaigns.length > 0 ? campaigns : [activeCampaign]).map((c) => (
          <button
            key={c.campaign_id}
            onClick={() => setSelectedCampaign(c)}
            className={`px-4.5 py-3 rounded-2xl border text-xs font-mono font-medium transition-all text-left min-w-[250px] card-hover ${
              activeCampaign.campaign_id === c.campaign_id
                ? 'bg-[#EEF3FF] text-[#0F172A] border-[#172554] shadow-xs font-bold'
                : 'bg-white border-[#D9DEE8] text-[#475569] hover:border-[#172554]'
            }`}
          >
            <div className="font-bold text-[#0F172A] text-sm">{c.campaign_id}</div>
            <div className="text-[11px] opacity-80 mt-1">
              Family: {c.genome.attack_type} | Rail: {c.genome.payment_rail}
            </div>
          </button>
        ))}
      </div>

      {/* Metadata Inspector Card */}
      <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl space-y-4 shadow-xs">
        <div className="flex items-center justify-between border-b border-[#D9DEE8] pb-3">
          <div>
            <h3 className="text-lg font-bold text-[#0F172A] font-mono">{g.objective}</h3>
            <p className="text-xs text-[#475569] mt-1 font-mono">
              Target Population: <span className="text-[#0F172A] font-bold">{g.target_population}</span> | Stage: <span className="text-[#0F172A] font-bold">{g.campaign_stage}</span>
            </p>
          </div>
          <div className="text-right">
            <span className="bg-[#E8F8F2] border border-[#10B981]/30 text-[#10B981] text-xs px-3.5 py-1.5 rounded-full font-mono font-bold">
              FIDELITY: {(activeCampaign.behavioral_fidelity_score * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
          <div className="bg-[#F8F7F4] p-3.5 rounded-xl border border-[#D9DEE8]">
            <span className="text-[#475569] block">INTENSITY</span>
            <span className="text-[#FF8A00] font-bold text-sm">{activeCampaign.intensity.toFixed(1)}</span>
          </div>
          <div className="bg-[#F8F7F4] p-3.5 rounded-xl border border-[#D9DEE8]">
            <span className="text-[#475569] block">NOVELTY RATING</span>
            <span className="text-[#172554] font-bold text-sm">{g.novelty_rating.toFixed(2)}</span>
          </div>
          <div className="bg-[#F8F7F4] p-3.5 rounded-xl border border-[#D9DEE8]">
            <span className="text-[#475569] block">AFFECTED TXS</span>
            <span className="text-[#0F172A] font-bold text-sm">{activeCampaign.affected_transaction_count} TXs</span>
          </div>
          <div className="bg-[#F8F7F4] p-3.5 rounded-xl border border-[#D9DEE8]">
            <span className="text-[#475569] block">EVALUATION SEED</span>
            <span className="text-[#10B981] font-bold text-sm">{activeCampaign.seed}</span>
          </div>
        </div>
      </div>

      {/* Visual Fraud Genome 11-Group Matrix */}
      <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl shadow-xs">
        <h3 className="text-base font-bold text-[#0F172A] mb-4 flex items-center space-x-2 font-mono border-b border-[#D9DEE8] pb-3">
          <Cpu className="w-5 h-5 text-[#FF8A00]" />
          <span>Attack Genome Profile (11 Dimensions)</span>
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {genomeGroups.map((group) => (
            <div key={group.title} className={`bg-[#F8F7F4] p-3.5 rounded-xl border ${group.color}`}>
              <div className="text-[10px] font-mono font-bold tracking-wider uppercase opacity-75">
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
      <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl space-y-4 shadow-xs">
        <h3 className="text-base font-bold text-[#0F172A] flex items-center space-x-2 font-mono border-b border-[#D9DEE8] pb-3">
          <ShieldAlert className="w-5 h-5 text-[#FF8A00]" />
          <span>Affected Transactions ({transactions.length})</span>
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#F8F7F4] text-[#475569] uppercase text-[10px] border-b border-[#D9DEE8]">
              <tr>
                <th className="p-3">TRANSACTION ID</th>
                <th className="p-3">USER / ACCOUNT</th>
                <th className="p-3">AMOUNT</th>
                <th className="p-3">RAIL</th>
                <th className="p-3">RISK SCORE</th>
                <th className="p-3">DECISION</th>
                <th className="p-3 text-right">ACTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#D9DEE8] text-[#0F172A]">
              {transactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-[#F8F7F4] transition-colors">
                  <td className="p-3 font-bold text-[#FF8A00]">{tx.id}</td>
                  <td className="p-3 text-[#172554]">
                    {tx.user_id} <br />
                    <span className="text-[10px] text-[#64748B]">{tx.account_id}</span>
                  </td>
                  <td className="p-3 font-bold text-[#0F172A]">
                    ₹{tx.amount.toLocaleString()} <span className="text-[10px] text-[#64748B]">{tx.currency}</span>
                  </td>
                  <td className="p-3">{tx.payment_rail}</td>
                  <td className="p-3 font-bold text-[#FF8A00]">{tx.risk_score ?? 85.5} / 100</td>
                  <td className="p-3">
                    <span className="bg-rose-50 text-[#EF4444] border border-rose-200 px-2.5 py-1 rounded-full text-[10px] font-bold">
                      {tx.decision ?? 'BLOCK'}
                    </span>
                  </td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => navigate(`/investigator?tx=${tx.id}`)}
                      className="bg-[#172554] text-white hover:bg-[#0F172A] px-3.5 py-1.5 rounded-lg text-xs transition-colors inline-flex items-center space-x-1.5 font-mono font-bold active:scale-95 shadow-xs"
                    >
                      <span>INVESTIGATE</span>
                      <ArrowRight className="w-3.5 h-3.5" />
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
