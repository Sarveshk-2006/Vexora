import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('FRAUDOSCOPE Command Center Frontend', () => {
  it('renders application shell header cleanly', async () => {
    render(<App />);
    const titleElements = await screen.findAllByText(/FRAUDOSCOPE/i);
    expect(titleElements.length).toBeGreaterThan(0);
  });

  it('renders navigation commands in sidebar', async () => {
    render(<App />);
    const cmdElements = await screen.findAllByText(/Command Center/i);
    expect(cmdElements.length).toBeGreaterThan(0);
    const invElements = await screen.findAllByText(/Transaction Investigator/i);
    expect(invElements.length).toBeGreaterThan(0);
    const whyElements = await screen.findAllByText(/Why Flagged\?/i);
    expect(whyElements.length).toBeGreaterThan(0);
    const gapElements = await screen.findAllByText(/Defense Gaps/i);
    expect(gapElements.length).toBeGreaterThan(0);
    const hardElements = await screen.findAllByText(/Hardening & Models/i);
    expect(hardElements.length).toBeGreaterThan(0);
  });

  it('renders closed-loop simulation run button', async () => {
    render(<App />);
    const runButtons = await screen.findAllByText(/RUN CLOSED-LOOP SIMULATION/i);
    expect(runButtons.length).toBeGreaterThan(0);
  });

  it('renders closed-loop pipeline execution state machine title', async () => {
    render(<App />);
    const pipelineTitles = await screen.findAllByText(/Closed-Loop Pipeline Execution State Machine/i);
    expect(pipelineTitles.length).toBeGreaterThan(0);
  });

  it('renders 5-gate promotion gate audit panel', async () => {
    render(<App />);
    const gateTitles = await screen.findAllByText(/Autonomous Hardening Promotion Gate Audit/i);
    expect(gateTitles.length).toBeGreaterThan(0);
  });

  it('renders why flagged structured evidence title', async () => {
    render(<App />);
    const whyTitles = await screen.findAllByText(/WHY WAS THIS TRANSACTION FLAGGED\?/i);
    expect(whyTitles.length).toBeGreaterThan(0);
  });
});
