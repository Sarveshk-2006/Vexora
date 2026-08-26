import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from './App';
import * as apiModule from './services/api';

describe('App Shell', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders title and project description correctly', () => {
    vi.spyOn(apiModule, 'fetchHealthStatus').mockImplementation(
      () => new Promise(() => {}) // never resolves
    );

    render(<App />);

    expect(screen.getByText('FRAUDOSCOPE')).toBeInTheDocument();
    expect(
      screen.getByText('Autonomous Adversarial Payment Security Lab')
    ).toBeInTheDocument();
    expect(screen.getByText('Backend status:')).toBeInTheDocument();
    expect(screen.getByText('Checking...')).toBeInTheDocument();
  });

  it('displays Online status when backend health check succeeds', async () => {
    vi.spyOn(apiModule, 'fetchHealthStatus').mockResolvedValue({
      status: 'ok',
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Online')).toBeInTheDocument();
    });
  });

  it('displays Offline status when backend health check fails', async () => {
    vi.spyOn(apiModule, 'fetchHealthStatus').mockRejectedValue(
      new Error('Network Error')
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Offline')).toBeInTheDocument();
    });
  });
});
