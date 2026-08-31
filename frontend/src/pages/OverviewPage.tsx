import React, { useEffect, useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import {
  Activity,
  Zap,
  ShieldCheck,
  AlertTriangle,
  Cpu,
  BarChart2,
  TrendingUp,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { getOverviewSummary } from '../api/overview';
import { OverviewSummary } from '../api/types';
import { DEMO_DATA } from '../api/client';

interface ContextType {
  overviewData: OverviewSummary | null;
  apiConnected: boolean;
}

export const OverviewPage: React.FC = () => {
  const { overviewData: initialData } = useOutletContext<ContextType>();
  const [data, setData] = useState<OverviewSummary | null>(initialData || DEMO_DATA.overview);
  const [loading, setLoading] = useState<boolean>(!initialData);

  useEffect(() => {
    getOverviewSummary()
      .then((res) => {
        if (res) setData(res);
        setLoading(false);
      })
      .catch(() => {
        setData(DEMO_DATA.overview);
        setLoading(false);
      });
  }, []);

  if (loading && !data) {
    return (
      <div className="space-y-6 font-sans">
        <div className="h-10 w-64 skeleton-shimmer rounded-xl"></div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-32 skeleton-shimmer rounded-xl"></div>
          ))}
        </div>
      </div>
    );
  }

  const activeData = data || DEMO_DATA.overview;
  const m = activeData.metrics;

  const detectionBreakdown = [
    { name: 'Attacks Detected', value: Math.round(m.attacks_generated * m.detection_rate), color: '#172554' },
    { name: 'Evasions (Defense Gap)', value: Math.round(m.attacks_generated * (1.0 - m.detection_rate)), color: '#FF8A00' },
  ];

  const layerPerformanceData = [
    { name: 'Rules Layer', score: 40.0 },
    { name: 'Transaction ML', score: 76.8 },
    { name: 'Behavioral Anomaly', score: 65.0 },
    { name: 'Graph Intelligence', score: 25.0 },
    { name: 'Adversarial Detector', score: 90.0 },
  ];

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-[#0F172A]">Security Overview</h2>
          <p className="text-base text-[#475569] mt-1 font-normal">
            Overview of synthetic transaction risk, detection metrics, and active model state
          </p>
        </div>
        <div className="text-xs font-mono bg-white border border-[#D9DEE8] text-[#0F172A] px-3.5 py-2 rounded-xl shadow-xs self-start sm:self-auto">
          SEED: <span className="text-[#172554] font-bold">{activeData.simulation_seed}</span> | ACTIVE MODEL: <span className="text-[#FF8A00] font-bold">{activeData.active_model_id}</span>
        </div>
      </div>

      {/* Primary Summary Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl shadow-xs card-hover">
          <div className="flex items-center justify-between text-[#475569] text-xs font-mono font-semibold">
            <span>TRANSACTIONS SIMULATED</span>
            <Activity className="w-4 h-4 text-[#172554]" />
          </div>
          <div className="text-3xl font-bold text-[#0F172A] mt-3 font-mono">
            {m.transactions_simulated.toLocaleString()}
          </div>
          <div className="text-xs text-[#64748B] mt-1 font-medium">
            {m.users_simulated} synthetic users | {m.accounts_simulated} accounts
          </div>
        </div>

        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl shadow-xs card-hover">
          <div className="flex items-center justify-between text-[#475569] text-xs font-mono font-semibold">
            <span>ATTACKS GENERATED</span>
            <Zap className="w-4 h-4 text-[#FF8A00]" />
          </div>
          <div className="text-3xl font-bold text-[#FF8A00] mt-3 font-mono">
            {m.attacks_generated}
          </div>
          <div className="text-xs text-[#64748B] mt-1 font-medium">
            Synthetic Evasion Campaigns
          </div>
        </div>

        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl shadow-xs card-hover">
          <div className="flex items-center justify-between text-[#475569] text-xs font-mono font-semibold">
            <span>DETECTION RECALL</span>
            <ShieldCheck className="w-4 h-4 text-[#10B981]" />
          </div>
          <div className="text-3xl font-bold text-[#10B981] mt-3 font-mono">
            {(m.detection_rate * 100).toFixed(1)}%
          </div>
          <div className="text-xs text-[#64748B] mt-1 font-medium">
            Hybrid Detection Recall
          </div>
        </div>

        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl shadow-xs card-hover">
          <div className="flex items-center justify-between text-[#475569] text-xs font-mono font-semibold">
            <span>FALSE POSITIVE RATE</span>
            <AlertTriangle className="w-4 h-4 text-[#EF4444]" />
          </div>
          <div className="text-3xl font-bold text-[#0F172A] mt-3 font-mono">
            {(m.false_positive_rate * 100).toFixed(1)}%
          </div>
          <div className="text-xs text-[#64748B] mt-1 font-medium">
            Benign Approval Rate: {(m.benign_approval_rate * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Secondary Status Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl shadow-xs card-hover">
          <div className="text-xs text-[#475569] font-mono font-semibold">ACTIVE MODEL VERSION</div>
          <div className="text-lg font-bold text-[#172554] mt-1 font-mono">{activeData.active_model_id}</div>
          <div className="text-xs text-[#64748B] mt-1 font-medium">ROC-AUC: {m.hybrid_roc_auc.toFixed(4)}</div>
        </div>

        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl shadow-xs card-hover">
          <div className="text-xs text-[#475569] font-mono font-semibold">DEFENSE GAPS</div>
          <div className="text-lg font-bold text-[#FF8A00] mt-1 font-mono">{m.defense_gaps_discovered} IDENTIFIED</div>
          <div className="text-xs text-[#64748B] mt-1 font-medium">MULTI_VECTOR_EVASION</div>
        </div>

        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl shadow-xs card-hover">
          <div className="text-xs text-[#475569] font-mono font-semibold">HARDENING RUNS</div>
          <div className="text-lg font-bold text-[#172554] mt-1 font-mono">{m.hardening_runs} EXECUTED</div>
          <div className="text-xs text-[#10B981] mt-1 font-semibold">Status: Promoted & Active</div>
        </div>

        <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl shadow-xs card-hover">
          <div className="text-xs text-[#475569] font-mono font-semibold">TARGETED GAP RECALL</div>
          <div className="text-lg font-bold text-[#10B981] mt-1 font-mono flex items-center space-x-1">
            <TrendingUp className="w-4 h-4" />
            <span>+{(m.targeted_gap_improvement_delta * 100).toFixed(0)}% PTS</span>
          </div>
          <div className="text-xs text-[#64748B] mt-1 font-medium">Gap Recall: 20% → 80%</div>
        </div>
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl shadow-xs">
          <div className="flex items-center justify-between mb-4 border-b border-[#D9DEE8] pb-3">
            <h3 className="text-base font-bold text-[#0F172A] flex items-center space-x-2 font-mono">
              <BarChart2 className="w-4 h-4 text-[#172554]" />
              <span>Detection Layer Breakdown</span>
            </h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={layerPerformanceData} layout="vertical" margin={{ left: 20, right: 20, top: 10, bottom: 10 }}>
                <XAxis type="number" domain={[0, 100]} stroke="#475569" tick={{ fontSize: 12, fill: '#475569' }} />
                <YAxis dataKey="name" type="category" stroke="#475569" tick={{ fontSize: 12, fill: '#0F172A' }} width={140} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#F8F7F4', borderColor: '#D9DEE8', borderRadius: '8px', fontSize: '12px', color: '#0F172A' }}
                />
                <Bar dataKey="score" fill="#172554" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white border border-[#D9DEE8] p-6 rounded-2xl shadow-xs">
          <div className="flex items-center justify-between mb-4 border-b border-[#D9DEE8] pb-3">
            <h3 className="text-base font-bold text-[#0F172A] flex items-center space-x-2 font-mono">
              <Cpu className="w-4 h-4 text-[#172554]" />
              <span>Evasion vs Detection Ratio</span>
            </h3>
          </div>
          <div className="h-64 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={detectionBreakdown} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                  {detectionBreakdown.map((entry, idx) => (
                    <Cell key={`cell-${idx}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#F8F7F4', borderColor: '#D9DEE8', borderRadius: '8px', fontSize: '12px', color: '#0F172A' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
