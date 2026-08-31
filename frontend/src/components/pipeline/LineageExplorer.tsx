import React, { useMemo } from 'react';
import { ReactFlow, Background, Controls, Node, Edge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { GitBranch } from 'lucide-react';

interface LineageExplorerProps {
  runId?: string;
  genomeHash?: string;
  scenarioId?: string;
  hardeningRunId?: string;
  candidateModelId?: string;
}

export const LineageExplorer: React.FC<LineageExplorerProps> = ({
  runId = 'RUN_LOOP_42',
  genomeHash = '3fcc41a4',
  scenarioId = 'SCEN_BEHAVIORAL_01',
  hardeningRunId = 'RUN_42_HARDENING_01',
  candidateModelId = 'v1.1.0-cand-42',
}) => {
  const nodes: Node[] = useMemo(
    () => [
      {
        id: '1',
        position: { x: 50, y: 100 },
        data: { label: `FRAUD GENOME\nHash: ${genomeHash}` },
        style: {
          background: '#FFFFFF',
          color: '#172554',
          border: '1px solid #9BACD8',
          fontFamily: 'monospace',
          fontSize: '11px',
          padding: '10px',
          borderRadius: '8px',
        },
      },
      {
        id: '2',
        position: { x: 220, y: 100 },
        data: { label: `RED TEAM ATTACK\n${scenarioId}` },
        style: {
          background: '#FFFFFF',
          color: '#F98513',
          border: '1px solid #F98513',
          fontFamily: 'monospace',
          fontSize: '11px',
          padding: '10px',
          borderRadius: '8px',
        },
      },
      {
        id: '3',
        position: { x: 420, y: 100 },
        data: { label: `DETECTOR EVIDENCE\nTargeted Gap: 87.5` },
        style: {
          background: '#FFFFFF',
          color: '#172554',
          border: '1px solid #273A91',
          fontFamily: 'monospace',
          fontSize: '11px',
          padding: '10px',
          borderRadius: '8px',
        },
      },
      {
        id: '4',
        position: { x: 620, y: 100 },
        data: { label: `DEFENSE GAP\nMULTI_VECTOR_EVASION` },
        style: {
          background: '#FFFFFF',
          color: '#F98513',
          border: '1px solid #F98513',
          fontFamily: 'monospace',
          fontSize: '11px',
          padding: '10px',
          borderRadius: '8px',
        },
      },
      {
        id: '5',
        position: { x: 820, y: 100 },
        data: { label: `HARDENING RUN\n${hardeningRunId}` },
        style: {
          background: '#FFFFFF',
          color: '#16A36F',
          border: '1px solid #16A36F',
          fontFamily: 'monospace',
          fontSize: '11px',
          padding: '10px',
          borderRadius: '8px',
        },
      },
      {
        id: '6',
        position: { x: 1020, y: 100 },
        data: { label: `PROMOTED MODEL\n${candidateModelId}` },
        style: {
          background: '#FFFFFF',
          color: '#16A36F',
          border: '1px solid #16A36F',
          fontFamily: 'monospace',
          fontSize: '11px',
          padding: '10px',
          borderRadius: '8px',
        },
      },
    ],
    [genomeHash, scenarioId, hardeningRunId, candidateModelId]
  );

  const edges: Edge[] = useMemo(
    () => [
      { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#9BACD8', strokeWidth: 2 } },
      { id: 'e2-3', source: '2', target: '3', animated: true, style: { stroke: '#F98513', strokeWidth: 2 } },
      { id: 'e3-4', source: '3', target: '4', animated: true, style: { stroke: '#273A91', strokeWidth: 2 } },
      { id: 'e4-5', source: '4', target: '5', animated: true, style: { stroke: '#F98513', strokeWidth: 2 } },
      { id: 'e5-6', source: '5', target: '6', animated: true, style: { stroke: '#16A36F', strokeWidth: 2 } },
    ],
    []
  );

  return (
    <div className="bg-white border border-[#D9DDE5] rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-[#111827] tracking-wide font-mono flex items-center gap-2">
            <GitBranch className="w-4 h-4 text-[#273A91]" />
            Attack Lineage Explorer
          </h3>
          <p className="text-xs text-[#475569] font-sans">
            Provenance tracing attack origin to promoted model version
          </p>
        </div>
        <span className="text-xs font-mono text-[#475569]">RUN: {runId}</span>
      </div>

      <div className="h-[220px] rounded-lg overflow-hidden border border-[#D9DDE5] bg-[#F8F7F4]">
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background color="#D9DDE5" gap={16} />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
};
