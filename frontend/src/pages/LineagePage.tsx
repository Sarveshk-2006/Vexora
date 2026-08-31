import React, { useMemo } from 'react';
import { ReactFlow, Background, Controls, Node, Edge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { GitBranch } from 'lucide-react';

export const LineagePage: React.FC = () => {
  const nodes: Node[] = useMemo(
    () => [
      {
        id: '1',
        position: { x: 50, y: 150 },
        data: { label: 'Fraud Genome\nSYN_GENOME_000001\nBEHAVIORAL_MIMICRY' },
        style: { background: '#0f172a', color: '#38bdf8', borderColor: '#0284c7', fontSize: 11, fontFamily: 'monospace' },
      },
      {
        id: '2',
        position: { x: 250, y: 150 },
        data: { label: 'Red Team Campaign\nCAMP_BEHAVIORAL_MIMICRY_01\nFidelity: 92.0%' },
        style: { background: '#0f172a', color: '#f59e0b', borderColor: '#d97706', fontSize: 11, fontFamily: 'monospace' },
      },
      {
        id: '3',
        position: { x: 450, y: 150 },
        data: { label: 'Affected Transaction\nTX_SYN_00000001\nAmount: ₹45,000' },
        style: { background: '#0f172a', color: '#f43f5e', borderColor: '#e11d48', fontSize: 11, fontFamily: 'monospace' },
      },
      {
        id: '4',
        position: { x: 650, y: 80 },
        data: { label: 'Blue Team Detection\nML Detector: 76.8/100\nDecision: BLOCK' },
        style: { background: '#0f172a', color: '#10b981', borderColor: '#059669', fontSize: 11, fontFamily: 'monospace' },
      },
      {
        id: '5',
        position: { x: 650, y: 220 },
        data: { label: 'Defense Gap\nGAP_EE3E17B80928\nMULTI_VECTOR_EVASION' },
        style: { background: '#0f172a', color: '#ef4444', borderColor: '#dc2626', fontSize: 11, fontFamily: 'monospace' },
      },
      {
        id: '6',
        position: { x: 850, y: 220 },
        data: { label: 'Hardening Run\nRUN_42_HARDENING_01\nAugmented: 8 Samples' },
        style: { background: '#0f172a', color: '#a855f7', borderColor: '#9333ea', fontSize: 11, fontFamily: 'monospace' },
      },
      {
        id: '7',
        position: { x: 1050, y: 220 },
        data: { label: 'Candidate Model\nv1.1.0-cand-42\nStatus: PROMOTED' },
        style: { background: '#0f172a', color: '#34d399', borderColor: '#10b981', fontSize: 11, fontFamily: 'monospace' },
      },
    ],
    []
  );

  const edges: Edge[] = useMemo(
    () => [
      { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#38bdf8' } },
      { id: 'e2-3', source: '2', target: '3', animated: true, style: { stroke: '#f59e0b' } },
      { id: 'e3-4', source: '3', target: '4', style: { stroke: '#10b981' } },
      { id: 'e3-5', source: '3', target: '5', style: { stroke: '#ef4444' } },
      { id: 'e5-6', source: '5', target: '6', animated: true, style: { stroke: '#a855f7' } },
      { id: 'e6-7', source: '6', target: '7', animated: true, style: { stroke: '#34d399' } },
    ],
    []
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <GitBranch className="w-5 h-5 text-emerald-400" />
            <span>Attack → Defense Provenance Lineage Graph</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Causal Provenance Lineage: Fraud Genome → Attack → Detection → Gap → Hardening Model Promotion
          </p>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg h-[500px]">
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background color="#334155" gap={16} />
          <Controls style={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
        </ReactFlow>
      </div>
    </div>
  );
};
