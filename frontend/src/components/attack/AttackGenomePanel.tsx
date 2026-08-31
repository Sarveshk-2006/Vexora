import React from 'react';
import { Dna } from 'lucide-react';

interface AttackGenomePanelProps {
  genome?: Record<string, any>;
}

export const AttackGenomePanel: React.FC<AttackGenomePanelProps> = ({
  genome = {
    objective: 'Autonomous orchestration closed-loop simulation',
    attack_type: 'BEHAVIORAL_MIMICRY',
    identity_state: 'NORMAL',
    device_strategy: 'DEVICE_MIMICRY',
    location_strategy: 'FAMILIAR',
    amount_pattern: 'FRAGMENTED',
    velocity_pattern: 'LOW_AND_SLOW',
    timing_pattern: 'RANDOMIZED',
    merchant_strategy: 'HOPPING',
    behavioral_similarity: 0.85,
    network_coordination: 'LOW',
    payment_rail: 'UPI',
    evasion_strategy: 'BEHAVIORAL_MIMICRY',
    novelty_rating: 0.7,
  },
}) => {
  const dimensions = [
    { label: 'ATTACK FAMILY', value: genome.attack_type },
    { label: 'IDENTITY STATE', value: genome.identity_state },
    { label: 'DEVICE STRATEGY', value: genome.device_strategy },
    { label: 'LOCATION STRATEGY', value: genome.location_strategy },
    { label: 'AMOUNT PATTERN', value: genome.amount_pattern },
    { label: 'VELOCITY PATTERN', value: genome.velocity_pattern },
    { label: 'TIMING PATTERN', value: genome.timing_pattern },
    { label: 'MERCHANT STRATEGY', value: genome.merchant_strategy },
    { label: 'PAYMENT RAIL', value: genome.payment_rail },
    { label: 'EVASION STRATEGY', value: genome.evasion_strategy },
    {
      label: 'SIMILARITY / NOVELTY',
      value: `${((genome.behavioral_similarity || 0.85) * 100).toFixed(0)}% / ${((genome.novelty_rating || 0.7) * 100).toFixed(0)}%`,
    },
  ];

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono flex items-center gap-2">
            <Dna className="w-4 h-4 text-purple-400" />
            Red Team Attack DNA (Fraud Genome Matrix)
          </h3>
          <p className="text-xs text-slate-400">
            Multi-dimensional threat vector specification driving target selection & behavior mutation
          </p>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-purple-950/80 text-purple-300 border border-purple-800/80 font-bold">
          11-GENOME DIMENSIONS
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {dimensions.map((dim) => (
          <div
            key={dim.label}
            className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex flex-col justify-between"
          >
            <span className="text-[10px] font-mono text-slate-500 font-semibold uppercase">
              {dim.label}
            </span>
            <span className="text-xs font-mono font-bold text-slate-200 mt-1 truncate">
              {String(dim.value || 'N/A')}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
