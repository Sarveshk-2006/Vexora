import { fetchJson, DEMO_DATA } from './client';
import { AttackCampaign } from './types';

export async function getAttackCampaigns(): Promise<AttackCampaign[]> {
  try {
    return await fetchJson<AttackCampaign[]>('/red-team/campaigns');
  } catch (err) {
    console.warn('[FRAUDOSCOPE Sandbox API] Using fallback AttackCampaigns demo data');
    return DEMO_DATA.campaigns;
  }
}
