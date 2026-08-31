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
  RefreshCw,
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

interface ContextType {
  overviewData: OverviewSummary | null;
  apiConnected: boolean;
}

export const OverviewPage: React.FC = () => {
  const { overviewData: initialData } = useOutletContext<ContextType>();
  const [data, setData] = useState<OverviewSummary | null>(initialData);
  const [loading, setLoading] = useState<boolean>(!initialData);

  useEffect(() => {
    if (!data) {
      getOverviewSummary().then((res) => {
        setData(res);
        setLoading(false);
      });
    }
  }, [data]);

  if (loading || !data) {
    return (
      <div className="p-8 text-center text-slate-400 font-mono text-sm flex items-center justify-center space-x-2">
        <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />
        <span>Loading FRAUDOSCOPE Security Overview...</span>
      </div>
    );
  }

  const m = data.metrics;

  const detectionBreakdown = [
    { name: 'Adversarial Attacks Flagged', value: Math.round(m.attacks_generated * m.detection_rate), color: '#10b981' },
    { name: 'Adversarial Evasions (Gaps)', value: Math.round(m.attacks_generated * (1.0 - m.detection_rate)), color: '#ef4444' },
  ];

  const layerPerformanceData = [
    { name: 'Rule Engine', score: 40.0 },
    { name: 'Transaction ML', score: 76.8 },
    { name: 'Behavioral Anomaly', score: 65.0 },
    { name: 'Graph Intelligence', score: 25.0 },
    { name: 'Adversarial Detector', score: 90.0 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">Security Command Center Overview</h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Autonomous Adversarial Digital Twin Sandbox Intelligence Metrics
          </p>
        </div>
        <div className="text-xs font-mono bg-slate-900 border border-slate-800 text-slate-300 px-3 py-1.5 rounded">
          SEED: <span className="text-emerald-400 font-bold">{data.simulation_seed}</span> | MODEL: <span className="text-amber-400 font-bold">{data.active_model_id}</span>
        </div>
      </div>

      {/* Primary KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>TRANSACTIONS SIMULATED</span>
            <Activity className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2 font-mono">
            {m.transactions_simulated.toLocaleString()}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            {m.users_simulated} users | {m.accounts_simulated} accounts
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>ATTACKS GENERATED</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400 mt-2 font-mono">
            {m.attacks_generated}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            Gen-0 Red Team Evasion Campaigns
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>DETECTION RECALL</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 mt-2 font-mono">
            {(m.detection_rate * 100).toFixed(1)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            Hybrid Blue Team Evasion Detection
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>FALSE POSITIVE RATE</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-slate-200 mt-2 font-mono">
            {(m.false_positive_rate * 100).toFixed(1)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            Benign Approval: {(m.benign_approval_rate * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Secondary Intelligence Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-lg">
          <div className="text-xs text-slate-400 font-mono">ACTIVE DEFENSE MODEL</div>
          <div className="text-base font-bold text-emerald-400 mt-1 font-mono">{data.active_model_id}</div>
          <div className="text-[11px] text-slate-500 mt-1">ROC-AUC: {m.hybrid_roc_auc.toFixed(4)}</div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-lg">
          <div className="text-xs text-slate-400 font-mono">DEFENSE GAPS DISCOVERED</div>
          <div className="text-base font-bold text-rose-400 mt-1 font-mono">{m.defense_gaps_discovered} GAP</div>
          <div className="text-[11px] text-slate-500 mt-1">Category: MULTI_VECTOR_EVASION</div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-lg">
          <div className="text-xs text-slate-400 font-mono">HARDENING RUNS</div>
          <div className="text-base font-bold text-blue-400 mt-1 font-mono">{m.hardening_runs} CLOSED LOOP</div>
          <div className="text-[11px] text-slate-500 mt-1">Status: PROMOTED & ACTIVE</div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-lg">
          <div className="text-xs text-slate-400 font-mono">GAP RECALL IMPROVEMENT</div>
          <div className="text-base font-bold text-emerald-400 mt-1 font-mono flex items-center space-x-1">
            <TrendingUp className="w-4 h-4" />
            <span>+{(m.targeted_gap_improvement_delta * 100).toFixed(0)}%</span>
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Targeted Gap Recall: 20% → 80%</div>
        </div>
      </div>

      {/* Visual Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center space-x-2">
              <BarChart2 className="w-4 h-4 text-emerald-400" />
              <span>Blue Team Detector Layer Risk Contribution</span>
            </h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={layerPerformanceData} layout="vertical" margin={{ left: 20, right: 20, top: 10, bottom: 10 }}>
                <XAxis type="number" domain={[0, 100]} stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" tick={{ fontSize: 11 }} width={140} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '6px', fontSize: '12px' }}
                />
                <Bar dataKey="score" fill="#10b981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center space-x-2">
              <Cpu className="w-4 h-4 text-blue-400" />
              <span>Adversarial Campaign Evasion vs Detection</span>
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
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '6px', fontSize: '12px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
