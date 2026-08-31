import { fetchJson, DEMO_DATA } from './client';
import { DefenseGap, HardeningRun } from './types';

export async function getDefenseGaps(): Promise<DefenseGap[]> {
  try {
    return await fetchJson<DefenseGap[]>('/hardening/analyze-gaps', { method: 'POST' });
  } catch (err) {
    console.warn('[VEXORA Sandbox API] Using fallback DefenseGaps demo data');
    return DEMO_DATA.gaps;
  }
}

export async function getHardeningRuns(): Promise<HardeningRun[]> {
  try {
    return await fetchJson<HardeningRun[]>('/hardening/runs');
  } catch (err) {
    console.warn('[VEXORA Sandbox API] Using fallback HardeningRuns demo data');
    return DEMO_DATA.hardeningRuns;
  }
}
