import { HealthResponse } from '../types/health';
import {
  ClosedLoopRunRequest,
  ClosedLoopRunResult,
} from '../types/orchestration';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function fetchHealthStatus(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`);
  }
  return response.json();
}

export async function runClosedLoopSimulation(
  request: ClosedLoopRunRequest = { seed: 42 }
): Promise<ClosedLoopRunResult> {
  const response = await fetch(`${API_BASE_URL}/api/v1/orchestration/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error(`Closed-loop simulation failed with status ${response.status}`);
  }
  return response.json();
}

export async function listClosedLoopRuns(): Promise<ClosedLoopRunResult[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/orchestration/runs`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`List runs failed with status ${response.status}`);
  }
  return response.json();
}

export async function getClosedLoopRun(
  runId: string
): Promise<ClosedLoopRunResult> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/orchestration/runs/${runId}`,
    {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    }
  );
  if (!response.ok) {
    throw new Error(`Get run failed with status ${response.status}`);
  }
  return response.json();
}

export async function getClosedLoopRunStages(
  runId: string
): Promise<any[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/orchestration/runs/${runId}/stages`,
    {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    }
  );
  if (!response.ok) {
    throw new Error(`Get run stages failed with status ${response.status}`);
  }
  return response.json();
}

export async function getClosedLoopRunVerdict(
  runId: string
): Promise<any> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/orchestration/runs/${runId}/verdict`,
    {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    }
  );
  if (!response.ok) {
    throw new Error(`Get run verdict failed with status ${response.status}`);
  }
  return response.json();
}
