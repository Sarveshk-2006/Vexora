export interface HealthResponse {
  status: string;
}

export type BackendHealthState = 'Checking...' | 'Online' | 'Offline';
