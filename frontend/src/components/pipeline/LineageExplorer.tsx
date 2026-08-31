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
          background: '#0f172a',
          color: '#c084fc',
          border: '1px solid #a855f7',
          fontFamily: 'monospace',
          fontSize: '11px',
          padding: '10px',
          borderRadius: '8px',
        },
      },
      {
        id: '2',
        position: { x: 220, y: 100 },
        data: { label: `RED TEAM CAMPAIGN\n${scenarioId}` },
        style: {
          background: '#0f172a',
          color: '#fb7185',
          border: '1px solid #f43f5e',
          fontFamily: 'monospace',
          fontSize: '11px',
          padding: '10px',
          borderRadius: '8px',
        },
      },
      {
        id: '3',
        position: { x: 420, y: 100 },
        data: { label: `BLUE TEAM EVIDENCE\nTargeted Gap: 87.5` },
        style: {
          background: '#0f172a',
          color: '#60a5fa',
          border: '1px solid #3b82f6',
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
          background: '#0f172a',
          color: '#fbbf24',
          border: '1px solid #f59e0b',
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
          background: '#0f172a',
          color: '#34d399',
          border: '1px solid #10b981',
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
          background: '#0f172a',
          color: '#34d399',
          border: '2px solid #10b981',
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
      { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#a855f7' } },
      { id: 'e2-3', source: '2', target: '3', animated: true, style: { stroke: '#f43f5e' } },
      { id: 'e3-4', source: '3', target: '4', animated: true, style: { stroke: '#3b82f6' } },
      { id: 'e4-5', source: '4', target: '5', animated: true, style: { stroke: '#f59e0b' } },
      { id: 'e5-6', source: '5', target: '6', animated: true, style: { stroke: '#10b981' } },
    ],
    []
  );

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono flex items-center gap-2">
            <GitBranch className="w-4 h-4 text-emerald-400" />
            End-to-End Closed-Loop Provenance Lineage Explorer
          </h3>
          <p className="text-xs text-slate-400">
            Immutable lineage graph tracing Red Team attack origin to promoted candidate model version
          </p>
        </div>
        <span className="text-xs font-mono text-slate-400">RUN: {runId}</span>
      </div>

      <div className="h-[220px] rounded-lg overflow-hidden border border-slate-800 bg-slate-950">
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background color="#1e293b" gap={16} />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
};
