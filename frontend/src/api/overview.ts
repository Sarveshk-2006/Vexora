import { fetchJson, DEMO_DATA } from './client';
import { OverviewSummary } from './types';

export async function getOverviewSummary(): Promise<OverviewSummary> {
  try {
    return await fetchJson<OverviewSummary>('/overview/summary');
  } catch (err) {
    console.warn('[VEXORA Sandbox API] Using fallback OverviewSummary demo data');
    return DEMO_DATA.overview;
  }
}
