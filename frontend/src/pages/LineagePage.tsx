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
        style: { background: '#FFFFFF', color: '#172554', borderColor: '#172554', fontSize: 11, fontFamily: 'monospace', borderRadius: '12px', padding: '12px' },
      },
      {
        id: '2',
        position: { x: 250, y: 150 },
        data: { label: 'Red Team Campaign\nCAMP_BEHAVIORAL_MIMICRY_01\nFidelity: 92.0%' },
        style: { background: '#FFFFFF', color: '#FF8A00', borderColor: '#FF8A00', fontSize: 11, fontFamily: 'monospace', borderRadius: '12px', padding: '12px' },
      },
      {
        id: '3',
        position: { x: 450, y: 150 },
        data: { label: 'Affected Transaction\nTX_SYN_00000001\nAmount: ₹45,000' },
        style: { background: '#FFFFFF', color: '#EF4444', borderColor: '#EF4444', fontSize: 11, fontFamily: 'monospace', borderRadius: '12px', padding: '12px' },
      },
      {
        id: '4',
        position: { x: 650, y: 80 },
        data: { label: 'Blue Team Detection\nML Detector: 76.8/100\nDecision: BLOCK' },
        style: { background: '#FFFFFF', color: '#10B981', borderColor: '#10B981', fontSize: 11, fontFamily: 'monospace', borderRadius: '12px', padding: '12px' },
      },
      {
        id: '5',
        position: { x: 650, y: 220 },
        data: { label: 'Defense Gap\nGAP_EE3E17B80928\nMULTI_VECTOR_EVASION' },
        style: { background: '#FFFFFF', color: '#FF8A00', borderColor: '#FF8A00', fontSize: 11, fontFamily: 'monospace', borderRadius: '12px', padding: '12px' },
      },
      {
        id: '6',
        position: { x: 850, y: 220 },
        data: { label: 'Hardening Run\nRUN_42_HARDENING_01\nAugmented: 8 Samples' },
        style: { background: '#FFFFFF', color: '#172554', borderColor: '#172554', fontSize: 11, fontFamily: 'monospace', borderRadius: '12px', padding: '12px' },
      },
      {
        id: '7',
        position: { x: 1050, y: 220 },
        data: { label: 'Candidate Model\nv1.1.0-cand-42\nStatus: PROMOTED' },
        style: { background: '#FFFFFF', color: '#10B981', borderColor: '#10B981', fontSize: 11, fontFamily: 'monospace', borderRadius: '12px', padding: '12px' },
      },
    ],
    []
  );

  const edges: Edge[] = useMemo(
    () => [
      { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#172554', strokeWidth: 2 } },
      { id: 'e2-3', source: '2', target: '3', animated: true, style: { stroke: '#FF8A00', strokeWidth: 2 } },
      { id: 'e3-4', source: '3', target: '4', style: { stroke: '#10B981', strokeWidth: 2 } },
      { id: 'e3-5', source: '3', target: '5', style: { stroke: '#FF8A00', strokeWidth: 2 } },
      { id: 'e5-6', source: '5', target: '6', animated: true, style: { stroke: '#172554', strokeWidth: 2 } },
      { id: 'e6-7', source: '6', target: '7', animated: true, style: { stroke: '#10B981', strokeWidth: 2 } },
    ],
    []
  );

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-[#0F172A] flex items-center space-x-2">
            <GitBranch className="w-7 h-7 text-[#172554]" />
            <span>Attack Lineage</span>
          </h2>
          <p className="text-base text-[#475569] mt-1 font-mono">
            Attack → Detection → Gap → Hardening Model Promotion
          </p>
        </div>
      </div>

      <div className="bg-white border border-[#D9DEE8] p-5 rounded-2xl h-[520px] shadow-xs">
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background color="#D9DEE8" gap={16} />
          <Controls style={{ backgroundColor: '#F8F7F4', borderColor: '#D9DEE8', color: '#0F172A' }} />
        </ReactFlow>
      </div>
    </div>
  );
};
