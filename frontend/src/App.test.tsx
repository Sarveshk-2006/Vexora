import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('VEXORA Command Center Frontend', () => {
  it('renders application shell header cleanly', async () => {
    render(<App />);
    const titleElements = await screen.findAllByText(/VEXORA/i);
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

  it('renders simulation run button', async () => {
    render(<App />);
    const runButtons = await screen.findAllByText(/RUN SIMULATION/i);
    expect(runButtons.length).toBeGreaterThan(0);
  });

  it('renders pipeline execution state title', async () => {
    render(<App />);
    const pipelineTitles = await screen.findAllByText(/Pipeline Execution State/i);
    expect(pipelineTitles.length).toBeGreaterThan(0);
  });

  it('renders 5-gate promotion gate audit panel', async () => {
    render(<App />);
    const gateTitles = await screen.findAllByText(/Hardening Promotion Gate Audit/i);
    expect(gateTitles.length).toBeGreaterThan(0);
  });

  it('renders why flagged structured evidence title', async () => {
    render(<App />);
    const whyTitles = await screen.findAllByText(/Why Flagged\?/i);
    expect(whyTitles.length).toBeGreaterThan(0);
  });
});
