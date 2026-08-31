import { fetchJson, DEMO_DATA } from './client';
import { SyntheticTransaction } from './types';

export async function getSyntheticTransactions(): Promise<SyntheticTransaction[]> {
  try {
    return await fetchJson<SyntheticTransaction[]>('/digital-twin/transactions');
  } catch (err) {
    console.warn('[FRAUDOSCOPE Sandbox API] Using fallback SyntheticTransactions demo data');
    return DEMO_DATA.transactions;
  }
}
